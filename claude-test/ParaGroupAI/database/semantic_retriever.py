"""Semantic search using sentence transformers."""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from database.embedding_cache import EmbeddingCache
import time
import logging

logger = logging.getLogger(__name__)

class SemanticRetriever:
    """Semantic search using sentence transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Initializing SemanticRetriever with model: {model_name}")
        # Force CPU usage to avoid CUDA compatibility issues
        self.model = SentenceTransformer(model_name, device='cpu')
        self.cache = EmbeddingCache()
        self.model_name = model_name

    def retrieve(self, query: str, messages: List[Dict], k: int = 10) -> List[Dict]:
        """Retrieve top-k most semantically similar messages."""
        start_time = time.time()

        if not messages:
            logger.warning("No messages to search")
            return []

        # Get query embedding
        query_embedding = self.model.encode(query)

        # Get message embeddings (with caching)
        message_embeddings = []
        for msg in messages:
            msg_id = str(msg.get('id', hash(str(msg.get('content', '')))))

            # Try cache first
            cached = self.cache.get(msg_id, self.model_name)
            if cached is not None:
                embedding = cached
            else:
                # Generate and cache
                content = msg.get('content', '')
                embedding = self.model.encode(content)
                self.cache.set(msg_id, embedding, self.model_name)

            message_embeddings.append(embedding)

        # Calculate cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity([query_embedding], message_embeddings)[0]

        # Get top-k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]

        # Build results
        retrieval_time = time.time() - start_time
        results = []
        for idx in top_k_indices:
            results.append({
                'message': messages[idx],
                'score': float(similarities[idx]),
                'method': 'semantic',
                'retrieval_time': retrieval_time
            })

        logger.info(f"Retrieved {len(results)} results in {retrieval_time:.3f}s")
        return results
