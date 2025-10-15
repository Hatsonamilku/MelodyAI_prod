# brain/memory_systems/semantic_memory.py
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import datetime
import asyncio
import logging
from typing import List, Dict, Any

logger = logging.getLogger("MelodyBotCore")

class SemanticMemorySystem:
    def __init__(self, db_path='melody_memory.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dim = 384
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            self.memory_map = {}
            self._setup_semantic_tables()
            self._load_existing_memories()
            print("✅ FAISS Semantic Memory initialized!")
        except Exception as e:
            print(f"❌ FAISS initialization failed: {e}")
            self.index = None

    # ---------- INTERNAL UTILITIES ----------
    async def _encode_async(self, text: str) -> np.ndarray:
        """Run embedding generation in a background thread (non-blocking)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.model.encode([text])[0])

    async def _search_async(self, vector: np.ndarray, top_k: int):
        """Run FAISS search in a background thread."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.index.search(vector, top_k))

    # ---------- DATABASE SETUP ----------
    def _setup_semantic_tables(self):
        """Create tables for semantic memory."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semantic_memories (
                user_id TEXT,
                memory_id INTEGER,
                user_message TEXT,
                bot_response TEXT,
                conversation_context TEXT,
                embedding BLOB,
                timestamp TEXT,
                importance_score REAL DEFAULT 1.0,
                PRIMARY KEY (user_id, memory_id)
            )
        ''')
        self.conn.commit()

    def _load_existing_memories(self):
        """Load existing memories into FAISS index."""
        if self.index is None:
            return
            
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id, memory_id, user_message, bot_response, embedding FROM semantic_memories')
        memories = cursor.fetchall()
        
        embeddings_list = []
        self.memory_map.clear()
        
        for idx, (user_id, memory_id, user_msg, bot_resp, embedding_blob) in enumerate(memories):
            if embedding_blob:
                embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                embeddings_list.append(embedding)
                self.memory_map[idx] = {
                    'user_id': user_id,
                    'memory_id': memory_id, 
                    'user_message': user_msg,
                    'bot_response': bot_resp
                }
                
        if embeddings_list:
            embedding_matrix = np.array(embeddings_list).astype('float32')
            # CRITICAL FIX: Normalize embeddings before adding to FAISS
            faiss.normalize_L2(embedding_matrix)
            self.index.add(embedding_matrix)
            print(f"✅ Loaded {len(embeddings_list)} memories into FAISS")

    # ---------- CORE FUNCTIONS ----------
    async def store_conversation(self, user_id: str, user_message: str, bot_response: str, importance: float = 1.0):
        """Store a new user/bot exchange asynchronously."""
        if self.index is None:
            return
            
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT COALESCE(MAX(memory_id), 0) + 1 FROM semantic_memories WHERE user_id = ?',
            (user_id,)
        )
        memory_id = cursor.fetchone()[0]
        
        conversation_text = f"User: {user_message} Bot: {bot_response}"
        embedding = await self._encode_async(conversation_text)
        embedding_blob = embedding.tobytes()
        
        cursor.execute('''
            INSERT INTO semantic_memories 
            (user_id, memory_id, user_message, bot_response, embedding, timestamp, importance_score)
            VALUES (?, ?, ?, ?, ?, datetime('now'), ?)
        ''', (user_id, memory_id, user_message, bot_response, embedding_blob, importance))
        self.conn.commit()
        
        embedding_np = np.array(embedding, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(embedding_np)
        self.index.add(embedding_np)
        
        new_index = self.index.ntotal - 1
        self.memory_map[new_index] = {
            'user_id': user_id,
            'memory_id': memory_id,
            'user_message': user_message,
            'bot_response': bot_response
        }

    async def search_relevant_memories(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Async semantic similarity search."""
        if self.index is None or self.index.ntotal == 0:
            return []
            
        try:
            query_embedding = await self._encode_async(query)
            query_np = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
            faiss.normalize_L2(query_np)
            
            k = min(top_k, self.index.ntotal)
            similarities, indices = await self._search_async(query_np, k)
            
            relevant_memories = []
            for similarity, idx in zip(similarities[0], indices[0]):
                if idx in self.memory_map and self.memory_map[idx]['user_id'] == user_id:
                    memory_data = self.memory_map[idx]
                    relevant_memories.append({
                        'user_message': memory_data['user_message'],
                        'bot_response': memory_data['bot_response'],
                        'similarity_score': float(similarity),
                        'memory_id': memory_data['memory_id']
                    })
                    
            relevant_memories.sort(key=lambda x: x['similarity_score'], reverse=True)
            return relevant_memories[:top_k]
            
        except Exception as e:
            logger.error(f"❌ Semantic search error: {e}")
            return []

    async def get_conversation_context(self, user_id: str, current_message: str) -> str:
        """Return recent relevant memory context for AI prompt."""
        relevant_memories = await self.search_relevant_memories(user_id, current_message, top_k=3)
        if not relevant_memories:
            return ""
            
        context_parts = ["🎭 RELEVANT PAST CONVERSATIONS:"]
        for i, memory in enumerate(relevant_memories, 1):
            context_parts.append(f"{i}. User: {memory['user_message']}")
            context_parts.append(f"   Bot: {memory['bot_response']}")
            context_parts.append(f"   [Relevance: {memory['similarity_score']:.3f}]")
            context_parts.append("")
            
        return "\n".join(context_parts)

    def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Quick stats about stored semantic memories."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM semantic_memories WHERE user_id = ?', (user_id,))
        memory_count = cursor.fetchone()[0]
        
        return {
            'semantic_memories': memory_count,
            'faiss_index_size': self.index.ntotal if self.index else 0,
            'semantic_search_enabled': self.index is not None
        }

# Global instance
semantic_memory = SemanticMemorySystem()