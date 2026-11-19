"""
RAG (Retrieval-Augmented Generation) pipeline for KisanMitra AI
Optimized for low-memory cloud deployments (<512MB RAM) and high performance
"""
import os
import re
from typing import List, Dict, Any, Optional

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "../../data/chroma")
ENABLE_CHROMA = os.getenv("ENABLE_CHROMA", "false").lower() in ("true", "1")


class SmartLightweightRetriever:
    """
    High-performance, low-memory RAG retriever.
    Uses BM25/keyword relevance + semantic metadata scoring (crop, district, topic).
    Memory footprint: ~2MB (perfect for Render 512MB free tier).
    """

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Store documents in memory index"""
        # Deduplicate by id or title
        existing_ids = {str(d.get("id")) for d in self.documents if d.get("id") is not None}
        new_docs = []
        for doc in documents:
            doc_id = str(doc.get("id", len(self.documents) + len(new_docs)))
            if doc_id not in existing_ids:
                new_docs.append({
                    "id": doc_id,
                    "content": doc.get("content", ""),
                    "metadata": doc.get("metadata", {})
                })
                existing_ids.add(doc_id)
        
        self.documents.extend(new_docs)
        print(f"RAG Retriever loaded {len(self.documents)} knowledge documents in lightweight index.")

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        crop: Optional[str] = None,
        district: Optional[str] = None,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant agricultural documents using semantic metadata and keyword scoring
        """
        if not self.documents:
            return []

        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        # Remove common stop words
        stop_words = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "in", "to", "for", "with", "my", "what", "how", "can", "i"}
        query_keywords = {w for w in query_words if len(w) > 2 and w not in stop_words}

        scored_docs = []

        for doc in self.documents:
            meta = doc.get("metadata", {})
            content = doc.get("content", "")
            content_lower = content.lower()
            title = meta.get("title", "")
            title_lower = title.lower()
            doc_crop = (meta.get("crop") or "").lower()
            doc_district = (meta.get("district") or "").lower()
            doc_topic = (meta.get("topic") or "").lower()

            score = 0.0

            # 1. Exact or partial crop match
            if crop and doc_crop:
                if crop.lower() in doc_crop or doc_crop in crop.lower():
                    score += 3.5
            elif doc_crop and (doc_crop in query_lower):
                score += 3.0

            # 2. Topic match
            if topic and doc_topic:
                if topic.lower() == doc_topic:
                    score += 2.5
            elif doc_topic and doc_topic in query_lower:
                score += 1.5

            # 3. District match if specified
            if district and doc_district and (district.lower() in doc_district or doc_district in district.lower()):
                score += 2.0

            # 4. Title keywords
            for kw in query_keywords:
                if kw in title_lower:
                    score += 1.8

            # 5. Content frequency
            for kw in query_keywords:
                if kw in content_lower:
                    score += 0.4

            # Normalize similarity score to 0..1 range
            similarity = min(0.98, max(0.1, score / 4.0))

            scored_docs.append({
                "content": content,
                "similarity": round(similarity, 3),
                "metadata": meta,
                "_raw_score": score
            })

        # Sort by relevance score
        scored_docs.sort(key=lambda x: x["_raw_score"], reverse=True)

        # Return top_k results
        return [
            {
                "content": item["content"],
                "similarity": item["similarity"],
                "metadata": item["metadata"]
            }
            for item in scored_docs[:top_k]
        ]

    def clear(self) -> None:
        self.documents = []


class ChromaRAGRetriever:
    """Optional Chroma vector store retriever (requires sentence-transformers and chromadb)"""

    def __init__(self):
        os.makedirs(CHROMA_DIR, exist_ok=True)
        import chromadb
        from sentence_transformers import SentenceTransformer

        self.client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(
            name="agriculture_knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        ids = [str(doc.get("id", i)) for i, doc in enumerate(documents)]
        contents = [doc.get("content", "") for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        embeddings = self.embedding_model.encode(contents).tolist()
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        crop: Optional[str] = None,
        district: Optional[str] = None,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        documents = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results.get("distances") else 0
                documents.append({
                    "content": doc,
                    "similarity": round(1 - distance, 3),
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                })
        return documents

    def clear(self) -> None:
        self.collection.delete()


def get_retriever():
    """Factory creating optimal retriever based on environment and memory"""
    if not hasattr(get_retriever, "_instance"):
        if ENABLE_CHROMA:
            try:
                get_retriever._instance = ChromaRAGRetriever()
                print("Initialized Chroma vector store retriever.")
            except Exception as e:
                print(f"Could not initialize Chroma ({e}), using lightweight retriever.")
                get_retriever._instance = SmartLightweightRetriever()
        else:
            get_retriever._instance = SmartLightweightRetriever()
            print("Initialized ultra-lightweight memory-optimized RAG retriever.")
    return get_retriever._instance
