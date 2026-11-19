"""
Chat API route
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User, Conversation, Message, FarmerContext
from app.agents.farmer_agent import get_farmer_agent
from app.rag.ingest import add_knowledge_documents_to_rag
from app.routes.auth import get_current_user_from_token

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    district: Optional[str] = None
    crop: Optional[str] = None
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list
    topic: str
    needs_expert: bool
    conversation_id: int
    message_id: int


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: str
    message_count: int


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str
    sources: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Handle a chat message from user
    """
    # Validate input
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    if len(request.message) > 5000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is too long (max 5000 characters)"
        )
    
    if request.language not in ["en", "kn"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language must be 'en' or 'kn'"
        )
    
    try:
        # Determine user: authenticated user or guest user
        if current_user:
            user = current_user
            user.language = request.language
            if request.district:
                user.district = request.district
        else:
            # Look for existing guest user or create one
            user = db.query(User).filter(User.username == None).first()
            if not user:
                user = User(language=request.language, district=request.district)
                db.add(user)
                db.flush()
            else:
                user.language = request.language
                if request.district:
                    user.district = request.district
        
        # Get or create conversation
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user.id
            ).first()
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        else:
            # Create new conversation
            conversation = Conversation(user_id=user.id, title=request.message[:50])
            db.add(conversation)
            db.flush()
            
            # Create farmer context
            farmer_context = FarmerContext(
                conversation_id=conversation.id,
                district=request.district,
                crop=request.crop
            )
            db.add(farmer_context)
        
        # Update farmer context if provided
        if conversation.farmer_context:
            if request.crop:
                conversation.farmer_context.crop = request.crop
            if request.district:
                conversation.farmer_context.district = request.district
        
        # Get conversation history
        previous_messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at).all()
        
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in previous_messages[-6:]  # Last 6 messages for context
        ]
        
        # Add user message to database
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.flush()
        
        # Get AI response
        agent = get_farmer_agent()
        ai_response = agent.process_question(
            question=request.message,
            language=request.language,
            district=request.district,
            crop=request.crop,
            conversation_history=conversation_history,
            db=db
        )
        
        # Add assistant message to database
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response["answer"],
            sources=str(ai_response.get("sources", []))
        )
        db.add(assistant_message)
        
        # Update conversation title if it's new
        if not conversation.title or conversation.title == request.message[:50]:
            conversation.title = request.message[:100]
        
        db.commit()
        
        return ChatResponse(
            answer=ai_response["answer"],
            sources=ai_response.get("sources", []),
            topic=ai_response.get("topic", "general"),
            needs_expert=ai_response.get("needs_expert", False),
            conversation_id=conversation.id,
            message_id=assistant_message.id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: Optional[User] = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user"""
    try:
        # If not logged in, return empty list (login to view and save conversation history)
        if not current_user:
            return []
        
        conversations = db.query(Conversation).filter(
            Conversation.user_id == current_user.id
        ).order_by(Conversation.updated_at.desc(), Conversation.created_at.desc()).all()
        
        return [
            ConversationResponse(
                id=conv.id,
                title=conv.title or "Untitled",
                created_at=conv.created_at.isoformat(),
                message_count=len(conv.messages)
            )
            for conv in conversations
        ]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
async def get_conversation_messages(
    conversation_id: int,
    current_user: Optional[User] = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    try:
        query = db.query(Conversation).filter(Conversation.id == conversation_id)
        if current_user:
            query = query.filter(Conversation.user_id == current_user.id)
            
        conversation = query.first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "sources": msg.sources
                }
                for msg in messages
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching messages: {str(e)}"
        )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: Optional[User] = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    try:
        query = db.query(Conversation).filter(Conversation.id == conversation_id)
        if current_user:
            query = query.filter(Conversation.user_id == current_user.id)
            
        conversation = query.first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        db.delete(conversation)
        db.commit()
        
        return {"status": "success", "message": "Conversation deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )
