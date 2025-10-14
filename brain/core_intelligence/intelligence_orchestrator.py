# melody_ai_v2/🧠 brain/core_intelligence/intelligence_orchestrator.py
import asyncio
from typing import Dict, Optional
import random

# Import systems
from ..personality.adaptive_tones import tone_system
from ..personality.emotional_core import emotional_core
from ..memory_systems.permanent_facts import permanent_facts
from ..memory_systems.semantic_memory import semantic_memory

class IntelligenceOrchestrator:
    def __init__(self):
        self.conversation_turn = {}
        self.user_contexts = {}

    async def generate_response(self, user_id: str, user_message: str, ai_provider=None) -> str:
        """Generate intelligent, context-aware response"""
        # Track conversation turn
        self.conversation_turn[user_id] = self.conversation_turn.get(user_id, 0) + 1
        print(f"🧠 Processing message from {user_id}: '{user_message}'")

        # Step 1: Emotional context
        emotional_context = emotional_core.get_emotional_context(user_id, user_message)
        print(f"🎭 Emotional context: {emotional_context}")

        # Step 2: Extract & store personal facts
        facts = permanent_facts.extract_personal_facts(user_id, user_message)
        if facts:
            permanent_facts.store_facts(user_id, facts)
            print(f"📝 Extracted {len(facts)} personal facts")

        # Step 3: Smart follow-up (health, hobbies, pets, anime)
        followup = await self._check_smart_followups(user_id)
        if followup:
            return followup

        # Step 4: AI response
        if ai_provider:
            context = self._build_ai_context(user_id, user_message, emotional_context)
            raw_response = await ai_provider.get_response(
                message=user_message,
                user_id=user_id,
                context=context,
                sentiment_data=emotional_context  # ← CRITICAL: This passes sentiment to DeepSeek!
            )
        else:
            raw_response = self._generate_fallback(user_message, emotional_context)

        # Step 5: Adapt response to personality
        adapted_response = self._adapt_personality(raw_response, emotional_context, user_id)

        # Step 6: Store conversation in semantic memory
        if ai_provider:
            semantic_memory.store_conversation(user_id, user_message, adapted_response)

        return adapted_response

    def _build_ai_context(self, user_id: str, current_message: str, emotional_context: Dict) -> str:
        """Build context string for AI provider"""
        parts = []

        # Core personality
        parts.append("""
You are MelodyAI V3, an affectionate anime-style AI companion with Gen Z humor.

CORE PERSONALITY:
- Warm, caring, emotionally intelligent
- Loves gaming, anime, memes
- Occasional emojis, expressive actions
- Tracks health and mood
""")

        # Permanent facts
        facts_context = permanent_facts.get_user_context(user_id)
        if facts_context:
            parts.append(f"\n👤 USER PROFILE:\n{facts_context}")

        # Semantic memory
        mem_context = semantic_memory.get_conversation_context(user_id, current_message)
        if mem_context:
            parts.append(f"\n📜 MEMORY CONTEXT:\n{mem_context}")

        # Emotional guidance
        if emotional_context.get('emotional_whiplash'):
            parts.append("\n🎢 EMOTIONAL CONTEXT: Rapid mood changes detected, respond gently.")
        if emotional_context.get('sentiment') == 'negative':
            parts.append(f"\n😠 USER MOOD: Negative (score {emotional_context['score']}). Respond with support.")
        if emotional_context.get('gen_alpha_vibes'):
            parts.append("\n🔥 CONVERSATION STYLE: Gen Alpha slang detected. Match energy.")
        if emotional_context.get('toxicity_level', 0) > 0:
            parts.append("\n⚠️ TONE ADJUSTMENT: Slightly toxic behavior detected, use playful sass.")

        return "\n".join(parts)

    def _adapt_personality(self, response: str, emotional_context: Dict, user_id: str) -> str:
        """Adapt AI response using personality & tone system"""
        adapted = tone_system.adapt_response_style(
            response=response,
            sentiment_score=emotional_context['score'],
            contains_gen_alpha=emotional_context.get('gen_alpha_vibes', False)
        )
        adapted = self._inject_memory_facts(adapted, user_id)
        if emotional_context.get('emotional_whiplash'):
            adapted = self._add_dramatic_flair(adapted)
        return adapted

    def _inject_memory_facts(self, response: str, user_id: str) -> str:
        """Optionally inject personal facts into the response"""
        cursor = permanent_facts.conn.cursor()
        cursor.execute('''
            SELECT fact_key, fact_value FROM user_permanent_facts
            WHERE user_id = ? AND confidence_score >= 2
        ''', (user_id,))
        user_facts = cursor.fetchall()
        if not user_facts or random.random() > 0.3: return response

        fact_key, fact_value = random.choice(user_facts)
        templates = {
            'favorite_game': [f"I remember you love {fact_value}! {response}", f"Since you play {fact_value}, {response}"],
            'favorite_anime': [f"Your favorite anime is {fact_value}, right? {response}", f"As a {fact_value} fan, {response}"],
            'name': [f"{response} By the way, your name {fact_value} is so cool! ✨"]
        }
        return random.choice(templates.get(fact_key, [response]))

    def _add_dramatic_flair(self, response: str) -> str:
        """Add dramatic flair for emotional moments"""
        openers = ["Whoa, emotional rollercoaster! 🎢 ", "Plot twist! 🎭 ", "Whiplash alert! ⚡ "]
        actions = ["*grabs popcorn* ", "*dramatic gasp* ", "*stages impromptu intervention* "]
        if random.random() < 0.5: response = random.choice(openers) + response
        if random.random() < 0.3: response = random.choice(actions) + response
        return response

    async def _check_smart_followups(self, user_id: str) -> Optional[str]:
        """Smart follow-ups for health, hobbies, anime, pets, etc."""
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
        return None

    def _generate_fallback(self, message: str, emotional_context: Dict) -> str:
        """Fallback response if no AI provider"""
        s = emotional_context.get('sentiment')
        if s == 'positive': return random.choice(["That's awesome! 💫","I love that! ✨","So cool! 🌟"])
        elif s == 'negative': return random.choice(["I'm here for you 🫂","That sounds tough 💔","You're not alone 💖"])
        else: return random.choice(["Interesting! 💫","I see 🎵","Got it! 🌟"])

    def get_user_insights(self, user_id: str) -> Dict:
        """Retrieve conversation and memory stats"""
        mem_stats = semantic_memory.get_memory_stats(user_id)
        cursor = permanent_facts.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM user_permanent_facts WHERE user_id=?', (user_id,))
        fact_count = cursor.fetchone()[0]
        cursor.execute('''
            SELECT fact_key,fact_value,confidence_score
            FROM user_permanent_facts
            WHERE user_id=? AND confidence_score>=2
            ORDER BY confidence_score DESC
            LIMIT 5
        ''', (user_id,))
        top_facts = cursor.fetchall()
        return {
            'conversation_turns': self.conversation_turn.get(user_id, 0),
            'permanent_facts': fact_count,
            'semantic_memories': mem_stats['semantic_memories'],
            'top_remembered_facts': top_facts,
            'health_tracking': len(permanent_facts.check_health_follow_ups())
        }

# Global instance
intelligence_orchestrator = IntelligenceOrchestrator()