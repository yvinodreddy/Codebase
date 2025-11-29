"""Embedding cache for semantic search performance."""
import sqlite3
import numpy as np
import pickle
from typing import Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class EmbeddingCache:
    """Fast embedding cache using SQLite."""

    def __init__(self, cache_path: str = "~/.ultrathink/embeddings.db"):
        self.cache_path = Path(cache_path).expanduser()
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"EmbeddingCache initialized: {self.cache_path}")

    def _init_database(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(str(self.cache_path))
        conn.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                message_id TEXT PRIMARY KEY,
                embedding BLOB NOT NULL,
                model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_model ON embeddings(model)')
        conn.commit()
        conn.close()

    def get(self, message_id: str, model: str = "all-MiniLM-L6-v2") -> Optional[np.ndarray]:
        """Retrieve embedding from cache."""
        try:
            conn = sqlite3.connect(str(self.cache_path))

            # Update access count
            conn.execute(
                "UPDATE embeddings SET access_count = access_count + 1 WHERE message_id = ? AND model = ?",
                (message_id, model)
            )

            # Get embedding
            cursor = conn.execute(
                "SELECT embedding FROM embeddings WHERE message_id = ? AND model = ?",
                (message_id, model)
            )
            row = cursor.fetchone()
            conn.commit()
            conn.close()

            if row:
                logger.debug(f"Cache HIT: {message_id}")
                return pickle.loads(row[0])
            else:
                logger.debug(f"Cache MISS: {message_id}")
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, message_id: str, embedding: np.ndarray, model: str = "all-MiniLM-L6-v2"):
        """Store embedding in cache."""
        try:
            conn = sqlite3.connect(str(self.cache_path))
            conn.execute(
                "INSERT OR REPLACE INTO embeddings (message_id, embedding, model, access_count) VALUES (?, ?, ?, 0)",
                (message_id, pickle.dumps(embedding), model)
            )
            conn.commit()
            conn.close()
            logger.debug(f"Cache SET: {message_id}")
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def clear(self):
        """Clear all cached embeddings."""
        try:
            conn = sqlite3.connect(str(self.cache_path))
            conn.execute("DELETE FROM embeddings")
            conn.commit()
            conn.close()
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Cache clear error: {e}")

    def stats(self):
        """Get cache statistics."""
        try:
            conn = sqlite3.connect(str(self.cache_path))
            cursor = conn.execute("SELECT COUNT(*), SUM(access_count) FROM embeddings")
            total, accesses = cursor.fetchone()
            conn.close()
            return {
                'total_embeddings': total or 0,
                'total_accesses': accesses or 0,
                'hit_rate': (accesses or 0) / max(total or 1, 1)
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {'total_embeddings': 0, 'total_accesses': 0, 'hit_rate': 0.0}
