# melody_ai_v2/services/discord_adapter.py
from typing import List, Dict, Optional
import asyncio
import discord
from datetime import datetime
import logging

# ✅ Absolute imports
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from brain.personality.emotional_core import EmotionalCore
from brain.memory_systems.permanent_facts import permanent_facts

logger = logging.getLogger(__name__)

class DiscordMelodyAdapter:
    def __init__(self):
        self.emotional_core = EmotionalCore()
        self.active_conversations: Dict[int, List[Dict]] = {}  # channel_id -> messages
        self.user_last_active: Dict[int, Dict[str, datetime]] = {}  # channel_id -> {user_id: last_active}
        self.summary_threshold = 10  # summarize every 10 messages

    async def process_discord_message(self, message: discord.Message, ai_provider=None, respond: bool = True) -> Optional[str]:
        if message.author.bot or not message.content:
            return None

        user_id = str(message.author.id)
        channel_id = message.channel.id
        user_message = message.content

        # Track conversation
        self.active_conversations.setdefault(channel_id, []).append({
            "user_id": user_id,
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        })
        self.user_last_active.setdefault(channel_id, {})[user_id] = datetime.now()

        if len(self.active_conversations[channel_id]) >= self.summary_threshold:
            await self._summarize_conversation(channel_id, ai_provider)

        if respond:
            user_context = permanent_facts.get_user_context(user_id)
            conversation_summary = permanent_facts.storage.data["users"].get(user_id, {}).get("conversation_summary", "")
            if conversation_summary:
                user_context += f"\n\n📝 Previous chat summary:\n{conversation_summary}"

            if user_context:
                user_message = f"{user_context}\n\nUser says: {user_message}"

            try:
                response = await intelligence_orchestrator.generate_response(
                    user_id=user_id,
                    user_message=user_message,
                    ai_provider=ai_provider
                )
                return response

            except Exception as e:
                logger.error(f"❌ Error processing message: {e}")
                return "Oops! My brain glitched for a sec 💫 Try again?"
        
        return None

    async def _summarize_conversation(self, channel_id: int, ai_provider=None):
        messages = self.active_conversations.get(channel_id, [])
        if not messages:
            return

        summaries = {}
        for msg in messages:
            uid = msg["user_id"]
            summaries.setdefault(uid, "")
            summaries[uid] += f"{msg['message']} "

        for uid, full_text in summaries.items():
            try:
                summary_prompt = f"Summarize this conversation concisely for memory storage:\n{full_text}"
                summary_text = await intelligence_orchestrator.generate_response(
                    user_id=uid,
                    user_message=summary_prompt,
                    ai_provider=ai_provider
                )
                permanent_facts.store_facts(uid, [{
                    "key": "conversation_summary", 
                    "value": summary_text,
                    "category": "general",
                    "confidence": 3
                }])
            except Exception as e:
                logger.error(f"❌ Error summarizing conversation for user {uid}: {e}")

        self.active_conversations[channel_id] = []

    async def handle_mention(self, message: discord.Message, ai_provider=None) -> str:
        user_id = str(message.author.id)
        user_message = message.content.replace(f"<@{message.client.user.id}>", "").strip()
        if not user_message:
            return "Hey! You mentioned me? 💫 What's up?"
        return await self.process_discord_message(message, ai_provider, respond=True)

    def get_user_emotional_state(self, user_id: str) -> Dict[str, any]:
        return self.emotional_core.get_emotional_state(user_id)

    def get_user_facts(self, user_id: str) -> str:
        return permanent_facts.get_user_context(user_id)
