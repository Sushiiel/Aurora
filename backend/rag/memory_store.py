"""
RAG Memory Store - Vector database for system memory
Stores and retrieves past experiments, decisions, and system states
"""
from typing import List, Dict, Any, Optional
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryStore:
    """
    Vector-based memory store for AURORA system
    Uses sentence transformers for embeddings and FAISS for similarity search
    """
    
    def __init__(self, use_pinecone: bool = False):
        """
        Initialize memory store
        
        Args:
            use_pinecone: If True, use Pinecone; otherwise use FAISS (local)
        """
        self.use_pinecone = use_pinecone
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2
        
        if use_pinecone:
            self._init_pinecone()
        else:
            self._init_faiss()
        
        self.memory_cache = []
    
    def _init_pinecone(self):
        """Initialize Pinecone vector database"""
        try:
            import pinecone
            from backend.config import settings
            
            pinecone.init(
                api_key=settings.pinecone_api_key,
                environment=settings.pinecone_environment
            )
            
            # Create or connect to index
            if settings.pinecone_index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    settings.pinecone_index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
            
            self.index = pinecone.Index(settings.pinecone_index_name)
            logger.info("Pinecone initialized successfully")
            
        except Exception as e:
            logger.warning(f"Pinecone initialization failed: {e}. Falling back to FAISS.")
            self.use_pinecone = False
            self._init_faiss()
    
    def _init_faiss(self):
        """Initialize FAISS vector database (local)"""
        try:
            import faiss
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.id_to_metadata = {}
            self.next_id = 0
            
            logger.info("FAISS initialized successfully")
            
        except Exception as e:
            logger.error(f"FAISS initialization failed: {e}")
            raise
    
    async def store(
        self, 
        text: str, 
        metadata: Dict[str, Any],
        doc_id: Optional[str] = None
    ) -> str:
        """
        Store a memory with its embedding
        
        Args:
            text: Text to embed and store
            metadata: Associated metadata
            doc_id: Optional document ID
            
        Returns:
            Document ID
        """
        try:
            # Generate embedding
            embedding = self.encoder.encode(text)
            
            # Generate ID if not provided
            if doc_id is None:
                doc_id = f"mem_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{self.next_id}"
                self.next_id += 1
            
            # Store based on backend
            if self.use_pinecone:
                self.index.upsert([(doc_id, embedding.tolist(), metadata)])
            else:
                # FAISS storage
                self.index.add(np.array([embedding]))
                self.id_to_metadata[self.next_id - 1] = {
                    "id": doc_id,
                    "text": text,
                    "metadata": metadata
                }
            
            # Cache locally
            self.memory_cache.append({
                "id": doc_id,
                "text": text,
                "metadata": metadata,
                "timestamp": datetime.utcnow()
            })
            
            logger.info(f"Stored memory: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            raise
    
    async def search(
        self, 
        query: str, 
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar memories
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of similar memories with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.encoder.encode(query)
            
            if self.use_pinecone:
                # Pinecone search
                results = self.index.query(
                    query_embedding.tolist(),
                    top_k=top_k,
                    include_metadata=True,
                    filter=filter_metadata
                )
                
                return [
                    {
                        "id": match.id,
                        "score": match.score,
                        "metadata": match.metadata
                    }
                    for match in results.matches
                ]
            
            else:
                # FAISS search
                distances, indices = self.index.search(
                    np.array([query_embedding]), 
                    min(top_k, len(self.id_to_metadata))
                )
                
                results = []
                for idx, distance in zip(indices[0], distances[0]):
                    if idx in self.id_to_metadata:
                        memory = self.id_to_metadata[idx]
                        results.append({
                            "id": memory["id"],
                            "text": memory["text"],
                            "score": float(1 / (1 + distance)),  # Convert distance to similarity
                            "metadata": memory["metadata"]
                        })
                
                return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def store_experiment(
        self,
        experiment_type: str,
        description: str,
        results: Dict[str, Any],
        success: bool
    ) -> str:
        """Store an experiment result for future retrieval"""
        
        text = f"{experiment_type}: {description}. Results: {results.get('summary', '')}"
        
        metadata = {
            "type": "experiment",
            "experiment_type": experiment_type,
            "success": success,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return await self.store(text, metadata)
    
    async def store_decision(
        self,
        decision_type: str,
        reasoning: str,
        outcome: Dict[str, Any]
    ) -> str:
        """Store an agent decision for future learning"""
        
        text = f"Decision: {decision_type}. Reasoning: {reasoning}"
        
        metadata = {
            "type": "decision",
            "decision_type": decision_type,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return await self.store(text, metadata)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory store statistics"""
        return {
            "backend": "pinecone" if self.use_pinecone else "faiss",
            "total_memories": len(self.memory_cache),
            "dimension": self.dimension
        }
