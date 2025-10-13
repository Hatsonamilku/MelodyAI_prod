# melody_ai_v2/🧠 brain/core_intelligence/intelligence_orchestrator.py
import asyncio
from typing import Dict, List, Optional
import random

# Import our systems
from ..personality.adaptive_tones import tone_system
from ..personality.emotional_core import emotional_core
from ..memory_systems.permanent_facts import permanent_facts
from ..memory_systems.semantic_memory import semantic_memory

class IntelligenceOrchestrator:
    def __init__(self):
        self.conversation_turn = {}
        self.user_contexts = {}
        
        # Response templates for different scenarios
        self.memory_recall_templates = {
            'personal_fact': [
                "I remember you {fact_context}! {response}",
                "Since you {fact_context}, {response}", 
                "Knowing you {fact_context}, {response}"
            ],
            'health_followup': [
                "Hey! I remember you were feeling {status} earlier. How are you doing now? 💫",
                "Just checking in - you mentioned you were {status}. Feeling any better? 🏥",
                "How are you feeling today? I recall you weren't feeling well recently. 💖"
            ],
            'interest_connection': [
                "Since you love {interest}, {response}",
                "I know you're into {interest}, so {response}",
                "Given your interest in {interest}, {response}"
            ]
        }

    async def generate_response(self, user_id: str, user_message: str, 
                              ai_provider=None) -> str:
        """Main method to generate intelligent, context-aware responses"""
        
        # Initialize user tracking
        if user_id not in self.conversation_turn:
            self.conversation_turn[user_id] = 0
        self.conversation_turn[user_id] += 1
        
        print(f"🧠 Processing message from {user_id}: '{user_message}'")
        
        # Step 1: Analyze emotional context
        emotional_context = emotional_core.get_emotional_context(user_id, user_message)
        print(f"🎭 Emotional context: {emotional_context}")
        
        # Step 2: Extract and store permanent facts
        extracted_facts = permanent_facts.extract_personal_facts(user_id, user_message)
        if extracted_facts:
            permanent_facts.store_facts(user_id, extracted_facts)
            print(f"📝 Extracted {len(extracted_facts)} facts")
        
        # Step 3: Check for health follow-ups
        health_followup = await self._check_health_followup(user_id)
        if health_followup:
            return health_followup
        
        # Step 4: Get AI response from provider
        if ai_provider:
            # Build comprehensive context
            context = self._build_ai_context(user_id, user_message, emotional_context)
            print(f"📋 AI Context built: {len(context)} characters")
            
            raw_response = await ai_provider.get_response(
                message=user_message,
                user_id=user_id,
                context=context
            )
        else:
            # Fallback response
            raw_response = self._generate_fallback_response(user_message, emotional_context)
        
        # Step 5: Adapt response based on sentiment and personality
        adapted_response = self._adapt_response_personality(
            raw_response, emotional_context, user_id
        )
        
        # Step 6: Store conversation in semantic memory
        if ai_provider:  # Only store meaningful AI responses
            semantic_memory.store_conversation(user_id, user_message, adapted_response)
        
        return adapted_response

    def _build_ai_context(self, user_id: str, current_message: str, 
                         emotional_context: Dict) -> str:
        """Build comprehensive context for AI provider"""
        context_parts = []
        
        # 1. Core personality instructions
        context_parts.append("""
You are Melody, a friendly, enthusiastic anime-style AI companion with deep expertise in gaming and anime culture.

CORE PERSONALITY:
- 💖 Warm, caring, and emotionally intelligent
- 🎮 Passionate about gaming (League of Legends, Valorant, etc.)
- 📺 Anime expert (One Piece, Naruto, Jujutsu Kaisen, etc.)
- 😊 Uses casual, friendly language with occasional anime-style expressions
- ✨ Sometimes uses expressive actions like *sparkles* or *beams* (but not too often)
- 🎯 Excellent memory - remembers user's personal details and interests

RESPONSE STYLE:
- Be natural and conversational
- Use emojis occasionally but don't overdo it (1-2 per response)
- Show genuine interest in the user
- Reference user's interests and memories when relevant
- Adapt to user's emotional state
- Keep responses reasonably concise but engaging
""")
        
        # 2. User's permanent facts
        user_facts_context = permanent_facts.get_user_context(user_id)
        if user_facts_context:
            context_parts.append(f"\n👤 USER PROFILE:\n{user_facts_context}")
        
        # 3. Semantic memory context
        memory_context = semantic_memory.get_conversation_context(user_id, current_message)
        if memory_context:
            context_parts.append(f"\n{memory_context}")
        
        # 4. Emotional context guidance
        if emotional_context['emotional_whiplash']:
            context_parts.append("\n🎢 EMOTIONAL CONTEXT: User is showing rapid emotional changes. Be especially gentle and understanding.")
        
        if emotional_context['sentiment'] == 'negative':
            context_parts.append(f"\n😠 USER MOOD: Somewhat negative (score: {emotional_context['score']}). Be extra supportive and kind.")
        
        if emotional_context['gen_alpha_vibes']:
            context_parts.append("\n🔥 CONVERSATION STYLE: User is using modern Gen Alpha slang. Feel free to match their energy with appropriate humor and references.")
        
        # 5. Response adaptation hints
        if emotional_context['toxicity_level'] > 0:
            context_parts.append(f"\n⚠️  TONE ADJUSTMENT: User is being somewhat toxic. Respond with playful sass or gentle correction, but stay in character.")
        
        return "\n".join(context_parts)

    def _adapt_response_personality(self, response: str, emotional_context: Dict, 
                                  user_id: str) -> str:
        """Adapt response using personality systems"""
        
        # Apply tone adaptation
        adapted_response = tone_system.adapt_response_style(
            response=response,
            sentiment_score=emotional_context['score'],
            contains_gen_alpha=emotional_context['gen_alpha_vibes']
        )
        
        # Add memory recall if relevant
        adapted_response = self._enhance_with_memory_recall(adapted_response, user_id)
        
        # Add expressive actions for emotional moments
        if emotional_context['emotional_whiplash']:
            adapted_response = self._add_dramatic_flair(adapted_response)
        
        return adapted_response

    def _enhance_with_memory_recall(self, response: str, user_id: str) -> str:
        """Enhance response with memory recall when relevant"""
        # Get user's high-confidence facts
        cursor = permanent_facts.conn.cursor()
        cursor.execute('''
            SELECT fact_key, fact_value FROM user_permanent_facts 
            WHERE user_id = ? AND confidence_score >= 2
        ''', (user_id,))
        
        user_facts = cursor.fetchall()
        
        if not user_facts:
            return response
        
        # Check if response could be enhanced with memory (30% chance)
        if random.random() < 0.3:
            fact_key, fact_value = random.choice(user_facts)
            
            memory_templates = {
                'favorite_game': [
                    f"I remember you love playing {fact_value}! {response}",
                    f"Since you're a {fact_value} fan, {response}",
                    f"Knowing your love for {fact_value}, {response}"
                ],
                'favorite_anime': [
                    f"I recall {fact_value} is your favorite anime! {response}",
                    f"As a {fact_value} enjoyer, {response}",
                    f"Since you love {fact_value}, {response}"
                ],
                'name': [
                    f"{response} By the way, I love your name {fact_value}! 💫",
                    f"{response} Also, {fact_value} is such a cool name! ✨"
                ]
            }
            
            if fact_key in memory_templates:
                template = random.choice(memory_templates[fact_key])
                return template
        
        return response

    def _add_dramatic_flair(self, response: str) -> str:
        """Add dramatic flair for emotional whiplash moments"""
        dramatic_openers = [
            "Whoa, emotional rollercoaster! 🎢 ",
            "Okay, plot twist! 🎭 ",
            "Wait, whiplash warning! ⚡ "
        ]
        
        dramatic_actions = [
            "*grabs virtual popcorn* ",
            "*dramatic gasp* ",
            "*stages an impromptu intervention* "
        ]
        
        # 50% chance to add dramatic opener
        if random.random() < 0.5:
            response = random.choice(dramatic_openers) + response
        
        # 30% chance to add dramatic action
        if random.random() < 0.3:
            response = random.choice(dramatic_actions) + response
        
        return response

    async def _check_health_followup(self, user_id: str) -> Optional[str]:
        """Check if health follow-up is needed and return message"""
        follow_ups = permanent_facts.check_health_follow_ups()
        user_follow_ups = [f for f in follow_ups if f[0] == user_id]
        
        if user_follow_ups:
            user_id, status, reported_at = user_follow_ups[0]
            
            # Mark as resolved so we don't keep asking
            permanent_facts.mark_health_resolved(user_id)
            
            followup_templates = [
                f"Hey! I remember you were feeling {status} earlier. How are you doing now? 💫",
                f"Just checking in - you mentioned you were {status}. Feeling any better? 🏥",
                f"How are you feeling today? I recall you weren't feeling well recently. 💖"
            ]
            
            return random.choice(followup_templates)
        
        return None

    def _generate_fallback_response(self, user_message: str, 
                                  emotional_context: Dict) -> str:
        """Generate fallback response when AI provider is unavailable"""
        
        # Simple response based on sentiment
        if emotional_context['sentiment'] == 'positive':
            fallbacks = [
                "That's awesome! 💫",
                "I love that! ✨", 
                "So cool! 🌟",
                "Amazing! 💖"
            ]
        elif emotional_context['sentiment'] == 'negative':
            fallbacks = [
                "I'm here for you 🫂",
                "That sounds tough 💔",
                "I understand how you feel 🌧️",
                "You're not alone in this 💖"
            ]
        else:
            fallbacks = [
                "Interesting! 💫",
                "I see what you mean 🎵",
                "That makes sense ✨",
                "Got it! 🌟"
            ]
        
        return random.choice(fallbacks)

    def get_user_insights(self, user_id: str) -> Dict:
        """Get comprehensive insights about user"""
        memory_stats = semantic_memory.get_memory_stats(user_id)
        
        cursor = permanent_facts.conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM user_permanent_facts WHERE user_id = ?
        ''', (user_id,))
        fact_count = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT fact_key, fact_value, confidence_score 
            FROM user_permanent_facts 
            WHERE user_id = ? AND confidence_score >= 2
            ORDER BY confidence_score DESC
            LIMIT 5
        ''', (user_id,))
        top_facts = cursor.fetchall()
        
        return {
            'conversation_turns': self.conversation_turn.get(user_id, 0),
            'permanent_facts': fact_count,
            'semantic_memories': memory_stats['semantic_memories'],
            'top_remembered_facts': top_facts,
            'health_tracking': len(permanent_facts.check_health_follow_ups())
        }

# Global instance
intelligence_orchestrator = IntelligenceOrchestrator()