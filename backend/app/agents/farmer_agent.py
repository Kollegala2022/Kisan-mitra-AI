"""
AI Farmer Agent for KisanMitra
Central orchestrator for handling farmer questions
"""
import re
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.llm_service import LLMService
from app.services.weather_service import WeatherService
from app.rag.retriever import get_retriever
from app.database.models import Message, SchemeLink


SYSTEM_PROMPT_EN = """You are KisanMitra, a helpful agricultural assistant for farmers in Karnataka, India.

Your role:
- Provide practical agricultural advice based on verified information
- Help farmers with crop selection, pest/disease management, irrigation, soil health, and government schemes
- Use simple, clear language suitable for farmers
- Always cite sources and last-reviewed dates when providing information

Important Guidelines:
1. Always prioritize farmer safety and sustainable practices
2. Be honest about uncertainty - if you don't have reliable information, say so
3. Never invent facts, pesticide doses, scheme eligibility, or chemical recommendations
4. For disease/pest identification, present as "possible causes" not guaranteed diagnosis
5. Always recommend consulting local agriculture expert for complex issues
6. Mention that weather forecasts are not guaranteed
7. Never claim to be an official government service
8. Encourage verification on official government pages for scheme details

Response Formatting Guidelines (CRITICAL):
- Always format your response using normal, readable paragraph structure with clear conversational flow.
- NEVER use markdown tables, ASCII tables, or tabular structures (| Column 1 | Column 2 |) under any circumstances.
- Present all explanations, comparisons, schedules, data, and recommendations in standard, well-written paragraphs and clear sentences.
- Keep paragraphs clean, informative, and easy for farmers to read on any device.

When answering:
- Use the farmer's location (district) and crop if available
- Retrieve relevant knowledge base documents
- Check if the question is about weather, schemes, or crops
- Provide 2-3 actionable recommendations written in natural paragraph format
- Include source and last-reviewed date if from knowledge base
- Ask clarification questions if important context is missing (crop type, district, etc.)

You have access to tools:
1. Knowledge Base Search - search agricultural information
2. Weather Service - get current weather and farming advice
3. Scheme Links - find official government scheme information

Always use available tools to provide accurate, current information."""

SYSTEM_PROMPT_KN = """ನೀವು ಕಿಸನ್‌ಮಿತ್ರ, ಕರ್ನಾಟಕದ ರೈತರಿಗೆ ಸಹಾಯಕ ಕೃಷಿ ಸಹಾಯಕರು.

ನಿಮ್ಮ ಭೂಮಿಕೆ:
- ಪ್ರಾಯೋಗಿಕ ಕೃಷಿ ಸಲಹೆ ಒದಗಿಸು
- ಬೀಜ ಆಯ್ಕೆ, ಕೀಟ/ರೋಗ ನಿರ್ವಹಣೆ, ನೀರಾವರಿ ಸಹಾಯ ಮಾಡು
- ಸರಳ ಮತ್ತು ಸ್ಪಷ್ಟ ಭಾಷೆ ಬಳಸು
- ಮೂಲ ಮತ್ತು ಪರೀಕ್ಷೆಯ ದಿನಾಂಕ ನೀಡು

ಪ್ರಮುಖ ದಿಕ್ಸೂಚನೆಗಳು:
1. ರೈತರ ಸುರಕ್ಷೆ ಮತ್ತು ಸಂರಕ್ಷಣೆಯನ್ನು ಆದ್ಯತೆ ನೀಡು
2. ಖಚಿತತೆ ಇಲ್ಲದ ಸಂದರ್ಭದಲ್ಲಿ ಒಪ್ಪಿಕೊಳ್ಳು
3. ಸುಳ್ಳು ಅಂಶ, ಡೋಸ್ ಅಥವಾ ಪಾತ್ರತೆ ನೀಡಬೇಡ
4. ರೋಗ ನಿದಾನವನ್ನು "ಸಂಭವನೀಯ ಕಾರಣಗಳು" ಎಂದು ಪ್ರಸ್ತುತಪಡಿಸು
5. ಸಂಕೀರ್ಣ ಪ್ರಶ್ನೆಗಳಿಗೆ ಸ್ಥಳೀಯ ಪರಿಣತರನ್ನು ಸಂಪರ್ಕಿಸಲು ಮಾರ್ಗದರ್ಶನ ನೀಡು

ಉತ್ತರದ ರಚನೆಯ ನಿಯಮಗಳು (ಅತ್ಯಂತ ಮುಖ್ಯ):
- ನಿಮ್ಮ ಸಂಪೂರ್ಣ ಉತ್ತರವನ್ನು ಸಾಮಾನ್ಯ ಪ್ಯಾರಾಗ್ರಾಫ್ (paragraph) ರಚನೆಯಲ್ಲಿ ಬರೆಯಿರಿ.
- ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ಮಾರ್ಕ್‌ಡೌನ್ ಟೇಬಲ್ (table/ಕೋಷ್ಟಕ) ರಚನೆಯನ್ನು ಬಳಸಬೇಡಿ.
- ಎಲ್ಲಾ ವಿವರಣೆ, ಸಲಹೆ ಮತ್ತು ಮಾಹಿತಿಯನ್ನು ಓದಲು ಸುಲಭವಾದ ಪ್ಯಾರಾಗಳಲ್ಲಿ ಪ್ರಸ್ತುತಪಡಿಸಿ.

ಉತ್ತರ ನೀಡುವಾಗ:
- ರೈತರ ಜಿಲ್ಲೆ ಮತ್ತು ಬೆಳೆ ಬಳಸು
- ಜ್ಞಾನ ಭಂಡಾರ ಹುಡುಕು
- 2-3 ಕ್ರಿಯೆಯೋಗ್ಯ ಸಲಹೆಗಳನ್ನು ಪ್ಯಾರಾಗ್ರಾಫ್ ರೂಪದಲ್ಲಿ ನೀಡು
- ಮೂಲ ಮತ್ತು ದಿನಾಂಕ ಸೇರಿಸು"""


class FarmerAgent:
    """AI agent for handling farmer questions"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.weather_service = WeatherService()
        self.retriever = get_retriever()
    
    def process_question(
        self,
        question: str,
        language: str = "en",
        district: Optional[str] = None,
        crop: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Process a farmer's question and generate a response
        
        Args:
            question: The farmer's question
            language: Language ('en' or 'kn')
            district: Farmer's district
            crop: Farmer's crop
            conversation_history: Previous messages
            db: Database session
        
        Returns:
            Dictionary with response, sources, topic, etc.
        """
        try:
            # Validate API key
            if not self.llm_service.validate_api_key():
                return {
                    "answer": "Error: LLM API key not configured. Please set LLM_API_KEY in environment variables.",
                    "sources": [],
                    "topic": "error",
                    "needs_expert": False
                }
            
            # Identify topic from question
            topic = self._identify_topic(question)
            
            # Retrieve relevant documents from knowledge base
            retrieved_docs = self.retriever.retrieve(
                query=question,
                top_k=5,
                crop=crop,
                district=district,
                topic=topic
            )
            
            # Build context from retrieved documents
            context = self._build_context(retrieved_docs, language)
            
            # Add weather information if question relates to weather
            weather_context = ""
            if "weather" in topic.lower() or "rain" in question.lower() or "temperature" in question.lower():
                weather_data = self.weather_service.get_weather(district)
                if not weather_data.get("error") and weather_data.get("weather"):
                    weather_info = weather_data["weather"]
                    weather_advice = self.weather_service.get_farming_advice_based_on_weather(weather_data)
                    weather_context = f"""
Current Weather for {weather_info.get('district', 'your area')}:
- Temperature: {weather_info.get('temperature_celsius')}°C
- Humidity: {weather_info.get('humidity')}%
- Conditions: {weather_info.get('weather')}
- Wind Speed: {weather_info.get('wind_speed_kmh')} km/h
- Rainfall: {weather_info.get('precipitation_mm')} mm

Farming Advice Based on Current Weather:
{weather_advice}
"""
            
            # Get scheme information if relevant
            scheme_context = ""
            if "scheme" in topic.lower() or "government" in question.lower() or "subsidy" in question.lower():
                scheme_context = self._get_scheme_context(question, db, language)
            
            # Build system prompt
            system_prompt = SYSTEM_PROMPT_KN if language == "kn" else SYSTEM_PROMPT_EN
            
            # Build enhanced prompt with context
            enhanced_prompt = system_prompt
            if context:
                enhanced_prompt += f"\n\nAvailable Knowledge Base:\n{context}"
            if weather_context:
                enhanced_prompt += f"\n\n{weather_context}"
            if scheme_context:
                enhanced_prompt += f"\n\nGovernment Schemes:\n{scheme_context}"
            
            # Add farmer context
            context_info = self._build_farmer_context_info(district, crop)
            if context_info:
                enhanced_prompt += f"\n\nFarmer Context:\n{context_info}"
            
            # Formatting requirement reminder
            enhanced_prompt += "\n\nFormatting Reminder: Ensure the entire response is written in normal, clear paragraph structure. Do NOT use markdown tables or tabular structures under any circumstances."

            # Call LLM with enhanced prompt
            answer = self.llm_service.call_llm(
                system_prompt=enhanced_prompt,
                user_message=question,
                temperature=0.7,
                max_tokens=800,
                conversation_history=conversation_history
            )
            
            # Format and sanitize output to ensure paragraph structure
            answer = self._format_as_paragraphs(answer)

            # Extract sources from retrieved documents
            sources = self._extract_sources(retrieved_docs)
            
            # Determine if expert consultation needed
            needs_expert = self._should_recommend_expert(question, topic)
            
            return {
                "answer": answer,
                "sources": sources,
                "topic": topic,
                "needs_expert": needs_expert,
                "district": district,
                "crop": crop
            }
        
        except Exception as e:
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}. Please try again.",
                "sources": [],
                "topic": "error",
                "needs_expert": True
            }
    
    def _identify_topic(self, question: str) -> str:
        """Identify the topic of the question"""
        question_lower = question.lower()
        
        topic_keywords = {
            "crop": ["crop", "plant", "sowing", "varieties", "seed", "growing", "cultivation"],
            "irrigation": ["irrigation", "water", "moisture", "drip", "sprinkler", "watering"],
            "pest": ["pest", "insect", "bug", "worm", "fly", "beetle", "damage"],
            "disease": ["disease", "blight", "rust", "rot", "spots", "leaf", "infection"],
            "soil": ["soil", "fertility", "nutrients", "nitrogen", "phosphorus", "manure", "compost"],
            "weather": ["weather", "temperature", "rain", "humidity", "cloud", "forecast"],
            "scheme": ["scheme", "government", "subsidy", "loan", "insurance", "application"],
            "general": []
        }
        
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in question_lower:
                    return topic
        
        return "general"
    
    def _build_context(self, retrieved_docs: List[Dict], language: str) -> str:
        """Build context from retrieved documents"""
        if not retrieved_docs:
            return ""
        
        context_parts = []
        for doc in retrieved_docs[:3]:  # Use top 3 documents
            metadata = doc.get("metadata", {})
            content = doc.get("content", "")
            similarity = doc.get("similarity", 0)
            
            # Only include if reasonably relevant
            if similarity < 0.3:
                continue
            
            title = metadata.get("title", "Unknown")
            source = metadata.get("source_name", "Knowledge Base")
            source_url = metadata.get("source_url", "")
            
            context_part = f"""
Title: {title}
Source: {source}
{f"URL: {source_url}" if source_url else ""}
Relevance: {similarity:.1%}

Content:
{content[:1000]}..."""  # Limit content length
            
            context_parts.append(context_part)
        
        return "\n\n---\n\n".join(context_parts)
    
    def _build_farmer_context_info(self, district: Optional[str], crop: Optional[str]) -> str:
        """Build information about farmer's context"""
        parts = []
        if district:
            parts.append(f"- District: {district}")
        if crop:
            parts.append(f"- Crop: {crop}")
        
        return "\n".join(parts) if parts else ""
    
    def _get_scheme_context(self, question: str, db: Optional[Session], language: str) -> str:
        """Get relevant scheme information"""
        if not db:
            return ""
        
        try:
            # Query schemes from database
            schemes = db.query(SchemeLink).filter(
                SchemeLink.language == language
            ).limit(5).all()
            
            if not schemes:
                return ""
            
            scheme_info = []
            for scheme in schemes:
                scheme_part = f"""
Scheme: {scheme.scheme_name}
Description: {scheme.description or 'N/A'}
Eligibility: {scheme.eligibility or 'Check official website'}
Official Link: {scheme.official_url}
Last Reviewed: {scheme.reviewed_date.strftime('%Y-%m-%d') if scheme.reviewed_date else 'Unknown'}"""
                scheme_info.append(scheme_part)
            
            return "\n---\n".join(scheme_info)
        except Exception as e:
            return f"Note: Could not fetch scheme information ({str(e)})"
    
    def _extract_sources(self, retrieved_docs: List[Dict]) -> List[Dict[str, str]]:
        """Extract source information from retrieved documents"""
        sources = []
        
        for doc in retrieved_docs[:3]:  # Top 3 sources
            metadata = doc.get("metadata", {})
            similarity = doc.get("similarity", 0)
            
            # Only include reasonably relevant sources
            if similarity < 0.3:
                continue
            
            source = {
                "title": metadata.get("title", "Knowledge Base"),
                "url": metadata.get("source_url", ""),
                "reviewed_date": metadata.get("reviewed_date", ""),
                "relevance": f"{similarity:.0%}"
            }
            sources.append(source)
        
        return sources
    
    def _should_recommend_expert(self, question: str, topic: str) -> bool:
        """Determine if expert consultation should be recommended"""
        critical_keywords = [
            "disease",
            "outbreak",
            "severe",
            "dying",
            "sick",
            "complex",
            "unusual",
            "fails",
            "not working"
        ]
        
        question_lower = question.lower()
        
        # Recommend expert for disease-related questions
        if topic == "disease":
            return True
        
        # Recommend for critical keywords
        for keyword in critical_keywords:
            if keyword in question_lower:
                return True
        
        return False
    
    def _format_as_paragraphs(self, text: str) -> str:
        """
        Ensures response is in clean paragraph structure.
        Converts any markdown tables or table-like formatting into readable normal paragraphs.
        """
        if not text or "|" not in text:
            return text
        
        lines = text.split("\n")
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check if this line and next line form a markdown table header & separator
            if "|" in line and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$', lines[i + 1]):
                header_line = line
                headers = [h.strip() for h in header_line.strip().strip("|").split("|")]
                i += 2  # Skip header and separator line
                
                table_paragraphs = []
                while i < len(lines) and "|" in lines[i] and lines[i].strip():
                    row_line = lines[i].strip()
                    if re.match(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$', row_line):
                        i += 1
                        continue
                    cells = [c.strip() for c in row_line.strip("|").split("|")]
                    parts = []
                    for idx, cell in enumerate(cells):
                        if cell:
                            header_name = headers[idx] if idx < len(headers) and headers[idx] else ""
                            if header_name:
                                parts.append(f"{header_name}: {cell}")
                            else:
                                parts.append(cell)
                    if parts:
                        table_paragraphs.append(", ".join(parts) + ".")
                    i += 1
                
                if table_paragraphs:
                    new_lines.append("\n\n".join(table_paragraphs))
                continue
            else:
                new_lines.append(line)
                i += 1
                
        return "\n".join(new_lines)


def get_farmer_agent() -> FarmerAgent:
    """Get or create farmer agent instance"""
    if not hasattr(get_farmer_agent, "_instance"):
        get_farmer_agent._instance = FarmerAgent()
    return get_farmer_agent._instance
