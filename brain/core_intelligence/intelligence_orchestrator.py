# melody_ai_v2/brain/core_intelligence/intelligence_orchestrator.py - DEBUG VERSION
import asyncio
import logging
import random
from typing import Optional, Dict, Any
from brain.personality.emotional_core import emotional_core
from brain.memory_systems.permanent_facts import permanent_facts
from brain.memory_systems.semantic_memory import semantic_memory

logger = logging.getLogger("MelodyBotCore")

class IntelligenceOrchestrator:
    """Main intelligence orchestrator that coordinates all AI systems"""
    
    def __init__(self):
        self.emotional_core = emotional_core
        self.permanent_facts = permanent_facts
        self.semantic_memory = semantic_memory
        logger.info("🧠 Intelligence Orchestrator initialized!")

    async def generate_response(self, user_id: str, user_message: str, ai_provider=None) -> str:
        """Main method to generate AI responses with full context"""
        try:
            # ADDED DEBUG LOGGING
            print(f"🎯 DEBUG: Generating response for user {user_id}: '{user_message[:50]}...'")
            
            # Step 1: Get emotional context
            emotional_context = self.emotional_core.get_emotional_context(user_id, user_message)
            print(f"🎭 DEBUG: Emotional score: {emotional_context.get('score', 50)}")
            
            # Step 2: Extract and store new facts from message - ADDED DEBUG
            new_facts = await self.permanent_facts.extract_personal_facts(user_id, user_message)
            print(f"📝 DEBUG: Extracted {len(new_facts)} new facts from: '{user_message}'")
            
            if new_facts:
                print(f"💾 DEBUG: Storing facts: {new_facts}")
                await self.permanent_facts.store_facts(user_id, new_facts)
            
            # Step 3: Get relevant memories - ADDED DEBUG
            memory_context = await self.semantic_memory.get_conversation_context(user_id, user_message)
            if memory_context:
                print("🧠 DEBUG: Found relevant memories")
            else:
                print("🧠 DEBUG: No relevant memories found")
            
            # Step 4: Get permanent facts context - ADDED DEBUG
            user_context = await self.permanent_facts.get_user_context(user_id)
            if user_context:
                print("📚 DEBUG: Loaded user context")
            else:
                print("📚 DEBUG: No user context found")
            
            # Step 5: Build comprehensive prompt
            full_prompt = self._build_comprehensive_prompt(
                user_message, 
                emotional_context,
                memory_context,
                user_context
            )
            
            # Step 6: Generate AI response
            if ai_provider:
                print("🤖 DEBUG: Calling AI provider...")
                response = await ai_provider.get_response(
                    message=user_message,
                    user_id=user_id,
                    context=full_prompt,
                    sentiment_data=emotional_context
                )
                
                # Step 7: Store conversation in semantic memory
                await self._store_conversation_memory(user_id, user_message, response)
                
                print(f"✅ DEBUG: Response generated: {response[:80]}...")
                return response
            else:
                fallback = self._get_fallback_response(emotional_context)
                print(f"⚠️ DEBUG: Using fallback: {fallback[:80]}...")
                return fallback
                
        except Exception as e:
            logger.error(f"❌ Intelligence orchestrator error: {e}")
            return "Oops! My brain had a moment 😭 Try again? 💫"

    def _build_comprehensive_prompt(self, user_message: str, emotional_context: Dict, 
                                  memory_context: str, user_context: str) -> str:
        """Build comprehensive prompt for AI"""
        prompt_parts = []
        
        # Emotional context
        if emotional_context:
            mood_score = emotional_context.get('score', 50)
            if mood_score >= 80:
                prompt_parts.append("USER MOOD: Very happy/affectionate - be extra sweet!")
            elif mood_score >= 60:
                prompt_parts.append("USER MOOD: Positive/playful - be fun and chaotic!") 
            elif mood_score >= 40:
                prompt_parts.append("USER MOOD: Neutral/chill - be friendly and engaging")
            elif mood_score >= 20:
                prompt_parts.append("USER MOOD: Slightly negative - be supportive")
            else:
                prompt_parts.append("USER MOOD: Negative/upset - be comforting")
                
            if emotional_context.get('is_friendly_banter'):
                prompt_parts.append("CONTEXT: Friendly banter - be playful and roast back nicely!")
            if emotional_context.get('should_roast_defense'):
                prompt_parts.append("CONTEXT: User might be testing you - be confident but friendly")
        
        # Memory context
        if memory_context:
            prompt_parts.append(memory_context)
            
        # User facts context
        if user_context:
            prompt_parts.append(user_context)
            
        # Final message
        prompt_parts.append(f"USER MESSAGE: {user_message}")
        prompt_parts.append("MelodyAI:")
        
        return "\n".join(prompt_parts)

    async def _store_conversation_memory(self, user_id: str, user_message: str, bot_response: str):
        """Store conversation in semantic memory"""
        try:
            # Calculate importance based on emotional context and content
            importance = 1.0
            if any(keyword in user_message.lower() for keyword in ['remember', 'important', 'never forget']):
                importance = 2.0
            elif any(keyword in user_message.lower() for keyword in ['name', 'live', 'favorite', 'hobby']):
                importance = 1.5
                
            await self.semantic_memory.store_conversation(
                user_id=user_id,
                user_message=user_message,
                bot_response=bot_response,
                importance=importance
            )
            print(f"💾 DEBUG: Stored conversation with importance {importance}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to store conversation memory: {e}")

    def _get_fallback_response(self, emotional_context: Dict) -> str:
        """Get fallback response when AI is unavailable"""
        mood_score = emotional_context.get('score', 50)
        
        if mood_score >= 70:
            return random.choice([
                "OMG I'm so excited to chat but my AI brain is taking a nap! 😴💫 Check back in a bit bestie! ✨",
                "YOOO the vibes are immaculate but my deep thoughts are offline! 🔧💫 BRB!",
                "AYEE I feel the energy but my circuits need a quick reboot! 😭💖 Back in a sec!"
            ])
        elif mood_score >= 40:
            return random.choice([
                "Hey! My deep thinking circuits are offline rn but I'm still here! 🔧💫",
                "Hmm my AI brain is being shy today! 😅 But I haven't forgotten you! ✨",
                "My creative juices are loading... slowly! 🐌💫 Still love chatting though!"
            ])
        else:
            return random.choice([
                "Ack! Technical difficulties but I haven't forgotten you! 😭💖 My memory still works! ✨",
                "Whoops! Brain glitch but I'm still here for you! 💫🔧",
                "My AI is having a moment but our connection is still strong! 💖🎵"
            ])

# Global instance
intelligence_orchestrator = IntelligenceOrchestrator()