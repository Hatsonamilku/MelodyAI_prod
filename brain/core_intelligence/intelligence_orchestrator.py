# melody_ai_v2/🧠 brain/core_intelligence/intelligence_orchestrator.py
import asyncio
from typing import Dict, Optional
import random

from ..personality.adaptive_tones import ultimate_response_system
from ..personality.emotional_core import EmotionalCore
from ..memory_systems.permanent_facts import permanent_facts
from ..memory_systems.semantic_memory import semantic_memory

class IntelligenceOrchestrator:
    def __init__(self):
        self.conversation_turn = {}
        self.user_contexts = {}
        self.emotional_core = EmotionalCore()

    async def generate_response(self, user_id: str, user_message: str, ai_provider=None) -> str:
        """Generate fully context-aware response"""

        # Track conversation turns
        self.conversation_turn[user_id] = self.conversation_turn.get(user_id, 0) + 1
        print(f"🧠 Processing message from {user_id}: '{user_message}'")

        # Step 1: Emotional context
        emotional_context = self.emotional_core.get_emotional_context(user_id, user_message)
        print(f"🎭 Emotional context: {emotional_context}")

        # Step 2: Extract & store facts (sync extraction, sync storage)
        facts = permanent_facts.extract_personal_facts(user_id, user_message)
        if facts:
            permanent_facts.store_facts(user_id, facts)
            print(f"📝 Extracted {len(facts)} personal facts")

        # Step 3: Smart follow-up (sync)
        followups = permanent_facts.check_health_follow_ups()
        user_followups = [f for f in followups if f[0] == user_id]
        if user_followups:
            uid, status, _ = user_followups[0]
            permanent_facts.mark_health_resolved(uid)
            templates = [
                f"Hey! I remember you were feeling {status}. How are you now? 💫",
                f"You mentioned being {status} before. Feeling better? 🏥",
                f"Hope you're better! I recall you weren't feeling well 💖"
            ]
            return random.choice(templates)

        # Step 4: AI response
        if ai_provider:
            context = self._build_ai_context(user_id, user_message, emotional_context)
            raw_response = await ai_provider.get_response(
                message=user_message,
                user_id=user_id,
                context=context,
                sentiment_data=emotional_context
            )
        else:
            raw_response = self._generate_fallback(user_message, emotional_context)

        # Step 5: Adapt response
        adapted_response = ultimate_response_system.build_response(
            response=raw_response,
            final_score=emotional_context['score'],
            contains_gen_alpha=emotional_context.get('gen_alpha_vibes', False),
            toxicity_level=emotional_context.get('toxicity_level', 0)
        )

        # Step 6: Store conversation (sync)
        semantic_memory.store_conversation(user_id, user_message, adapted_response)

        return adapted_response

    def _build_ai_context(self, user_id: str, current_message: str, emotional_context: Dict) -> str:
        """Build context string for AI provider (sync version)"""
        parts = ["You are MelodyAI V3, an affectionate anime-style AI companion with Gen Z humor.\n"]

        facts_context = permanent_facts.get_user_context(user_id)
        if facts_context:
            parts.append(f"\n👤 USER PROFILE:\n{facts_context}")

        mem_context = semantic_memory.get_conversation_context(user_id, current_message)
        if mem_context:
            parts.append(f"\n📜 MEMORY CONTEXT:\n{mem_context}")

        if emotional_context.get('emotional_whiplash'):
            parts.append("\n🎢 EMOTIONAL CONTEXT: Rapid mood changes detected, respond gently.")
        if emotional_context.get('sentiment') == 'negative':
            parts.append(f"\n😠 USER MOOD: Negative (score {emotional_context['score']}). Respond with support.")
        if emotional_context.get('gen_alpha_vibes'):
            parts.append("\n🔥 CONVERSATION STYLE: Gen Alpha slang detected. Match energy.")
        if emotional_context.get('toxicity_level', 0) > 0:
            parts.append("\n⚠️ TONE ADJUSTMENT: Slightly toxic behavior detected, use playful sass.")

        return "\n".join(parts)

    def _generate_fallback(self, message: str, emotional_context: Dict) -> str:
        s = emotional_context.get('sentiment')
        if s == 'positive': return random.choice(["That's awesome! 💫","I love that! ✨","So cool! 🌟"])
        elif s == 'negative': return random.choice(["I'm here for you 🫂","That sounds tough 💔","You're not alone 💖"])
        else: return random.choice(["Interesting! 💫","I see 🎵","Got it! 🌟"])


# Global instance
intelligence_orchestrator = IntelligenceOrchestrator()