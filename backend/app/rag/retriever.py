"""
RAG (Retrieval-Augmented Generation) pipeline using Chroma
"""
import os
import json
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from sqlalchemy.orm import Session

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "../../data/chroma")


class RAGRetriever:
    def __init__(self):
        """Initialize the RAG retriever with Chroma vector store"""
        # Create Chroma directory if it doesn't exist
        os.makedirs(CHROMA_DIR, exist_ok=True)
        
        # Initialize Chroma client with new API
        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="agriculture_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector store
        
        Args:
            documents: List of dicts with keys: id, content, metadata (title, topic, crop, etc.)
        """
        try:
            ids = [str(doc.get("id", i)) for i, doc in enumerate(documents)]
            contents = [doc.get("content", "") for doc in documents]
            metadatas = [doc.get("metadata", {}) for doc in documents]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # Add to collection
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=contents,
                metadatas=metadatas
            )
            print(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"Error adding documents: {e}")
            raise
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = 5,
        crop: Optional[str] = None,
        district: Optional[str] = None,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on query and context
        
        Args:
            query: The search query
            top_k: Number of results to return
            crop: Filter by crop (optional)
            district: Filter by district (optional)
            topic: Filter by topic (optional)
        
        Returns:
            List of relevant documents with scores
        """
        try:
            # Build where filter according to ChromaDB specifications
            filter_conditions = []
            if crop:
                filter_conditions.append({"crop": crop})
            if district:
                filter_conditions.append({"district": district})
            if topic and topic != "general":
                filter_conditions.append({"topic": topic})

            where_filter = None
            if len(filter_conditions) == 1:
                where_filter = filter_conditions[0]
            elif len(filter_conditions) > 1:
                where_filter = {"$or": filter_conditions}

            results = None
            if where_filter:
                try:
                    results = self.collection.query(
                        query_texts=[query],
                        n_results=top_k,
                        where=where_filter,
                        include=["documents", "metadatas", "distances"]
                    )
                except Exception as e:
                    print(f"Filtered query failed ({e}), falling back to standard semantic query.")
                    results = None

            # If filtered query returned no results or was skipped, run semantic search
            if not results or not results.get("documents") or len(results["documents"][0]) == 0:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )

            # Format results
            documents = []
            if results and results.get("documents") and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i] if results.get("distances") else 0
                    similarity = 1 - distance

                    doc_result = {
                        "content": doc,
                        "similarity": similarity,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                    }
                    documents.append(doc_result)

            return documents
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def clear(self) -> None:
        """Clear all documents from the collection"""
        try:
            self.collection.delete()
            print("Cleared all documents from vector store")
        except Exception as e:
            print(f"Error clearing collection: {e}")


def get_retriever() -> RAGRetriever:
    """Get or create a RAG retriever instance"""
    if not hasattr(get_retriever, "_instance"):
        get_retriever._instance = RAGRetriever()
    return get_retriever._instance
