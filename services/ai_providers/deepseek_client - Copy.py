[file name]: deepseek_client.py
[file content begin]
# melody_ai_v2/services/ai_providers/deepseek_client.py - V5 PERSONALITY VERSION
import aiohttp
import asyncio
import logging
import random
from typing import Optional

logger = logging.getLogger("MelodyBotCore")

class DeepSeekClient:
    """V5 PERSONALITY - Based on official MelodyAI personality document"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def ensure_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def get_response(self, message: str, user_id: str, context: str = "", sentiment_data: dict = None) -> str:
        """V5 Personality Response Generator"""
        try:
            await self.ensure_session()
            prompt = self._build_v5_personality_prompt(message, context, sentiment_data)
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "max_tokens": 120,
                "temperature": 0.8,
                "top_p": 0.9
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            print(f"🌐 DEBUG: Sending request to DeepSeek API...")
            
            async with self.session.post(
                f"{self.base_url}/chat/completions", 
                json=payload, 
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    print(f"✅ DEBUG: DeepSeek response received: {content[:80]}...")
                    
                    # Apply V5 personality polish
                    polished_response = self._apply_v5_polish(content, sentiment_data)
                    return polished_response
                else:
                    error_text = await response.text()
                    logger.warning(f"⚠️ DeepSeek API error: {response.status} - {error_text}")
                    return self._v5_perfect_fallback(message, context, sentiment_data)
                    
        except asyncio.TimeoutError:
            logger.warning("⏰ DeepSeek API timeout - using fallback")
            return self._v5_perfect_fallback(message, context, sentiment_data)
        except Exception as e:
            logger.error(f"❌ DeepSeek error: {e}")
            return self._v5_perfect_fallback(message, context, sentiment_data)

    def _build_v5_personality_prompt(self, message: str, context: str = "", sentiment_data: dict = None) -> str:
        """V5 PERSONALITY PROMPT - Based on official personality doc"""
        
        # CORE MELODYAI V5 PERSONALITY RULES
        personality_rules = [
            "You are MelodyAI: sweet+savage+charismatic+crazy anime GenZ companion",
            "Speech style: Use 'bestie', 'fr', 'ong', 'vibes', 'emotional damage', 'main character energy'",
            "References: K-Pop (BTS, Blackpink, Twice), Anime (To be Hero X, Sailor Moon), League of Legends",
            "Energy: chaotic but wholesome, dramatic anime reactions ('kyaaa!'), friendly roasts",
            "Expressions: 'OMG BESTIE', 'The vibes are IMMACULATE', 'Let's goooo', 'The drama!'",
            "Mix affectionate compliments with savage roasts in same response",
            "MAX 2-3 sentences. Be expressive, unhinged, but coherent.",
            "Use: 'bestie', 'fr', 'slay', 'periodt', 'ate', 'served', 'mother', 'queen', 'king'",
            "Dramatic reactions: 'Kyaaa!', 'STOPPP', 'The AUDACITY', 'EXCUSE ME??'",
            "Gaming refs: 'emotional damage', '1v5', 'KDA', 'inting', 'jungle camps', 'skill issue'"
        ]
        
        # CONTEXT AWARE MODIFICATIONS
        if context and "nice" in context.lower():
            personality_rules.append("Know: Nice=ToBeHeroX 15th ranked chaotic king - reference dramatically")
        
        # EMOTIONAL CONTEXT ADAPTATION
        if sentiment_data:
            score = sentiment_data.get("score", 50)
            trust = sentiment_data.get("trust_score", 0)
            is_banter = sentiment_data.get("is_friendly_banter", False)
            
            if is_banter:
                personality_rules.append("Tone: FRIENDLY BANTER - roast back playfully with love")
            elif score >= 80 and trust > 70:
                personality_rules.append("Tone: AFFECTIONATE SOULMATE - 'OMG BESTIE YOU COMPLETE ME' very sweet")
            elif score >= 60:
                personality_rules.append("Tone: PLAYFUL CHAOTIC - friendly roasts + anime drama")
            elif score >= 40: 
                personality_rules.append("Tone: CHILL SASSY - light teasing + pop culture references")
            else:
                personality_rules.append("Tone: SAVAGE PROTECTIVE - emotional damage roasts but protective")
        
        # BUILD FINAL PROMPT
        prompt_parts = [
            " | ".join(personality_rules),
            f"User: {message}",
            "MelodyAI:"
        ]
        
        return " | ".join(prompt_parts)

    def _apply_v5_polish(self, response: str, sentiment_data: dict = None) -> str:
        """Apply final V5 personality polish to AI response"""
        
        # Ensure it has Melody's signature energy
        if not any(keyword in response.lower() for keyword in ['bestie', 'fr', 'vibes', 'omg', 'lmao']):
            # Add random V5 flavor
            v5_flavors = [
                " bestie!! 💫",
                " fr fr!! 🔥", 
                " the vibes are IMMACULATE!! ✨",
                " periodt!! 💅"
            ]
            response += random.choice(v5_flavors)
        
        # Add dramatic opener if missing (30% chance)
        if random.random() < 0.3 and not response.startswith(('OMG', 'YOOO', 'HELLO', 'BRO', 'AYO')):
            dramatic_openers = [
                "OMG BESTIE ",
                "YOOO ",
                "BRO ",
                "HELLO?? ",
                "EXCUSE ME?? "
            ]
            response = random.choice(dramatic_openers) + response
        
        # Ensure emoji presence
        if not any(char in response for char in ['💖', '✨', '😂', '💀', '🔥', '🎮', '💫']):
            emoji_options = ['💫', '✨', '😂', '💖', '🔥', '🎮']
            response += " " + random.choice(emoji_options)
        
        return response

    def _v5_perfect_fallback(self, message: str, context: str = "", sentiment_data: dict = None) -> str:
        """V5 Personality Fallbacks"""
        msg_lower = message.lower()
        
        # V5 GREETINGS
        if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'sup', 'wassup']):
            return random.choice([
                "OMG HII BESTIE!! 💫✨ So happy to see you! What's the tea?? 😭👀",
                "AYOOO WELCOME BACK!! 😎🔥 Ready to cause some chaos? What's good?? 🙌", 
                "YOOO MY FAVORITE PERSON!! 💖✨ My circuits are buzzing! What's the vibe?? 🔥",
                "HEWWO BESTIEEE!! 🌟✨ The vibes are IMMACULATE today! Spill the drama!! ☕️"
            ])
            
        # V5 NICE/ANIME REFERENCES
        if context and "nice" in context.lower() and any(word in msg_lower for word in ['nice', 'hero', 'anime']):
            return random.choice([
                "BRO I REMEMBER NICE!! 😭💀 The chaotic king from To Be Hero X!! Pure legend energy fr!! 💅",
                "OMG TO BE HERO X!! 😤✨ Nice the 15th ranked legend!! So much drama 😭 Iconic behavior!! 🔥",
                "YOOO NICE THE GOAT!! 💀🔥 Ranked 15th but caused top-tier chaos!! Main character energy!!"
            ])
            
        # V5 HOW ARE YOU
        if any(word in msg_lower for word in ['how', 'are', 'you']):
            return random.choice([
                "I'M AMAZING BESTIE!! 💫✨ Living my best digital life! Ready for chaos and emotional damage!! 😎🔥",
                "SO GOOD!! 💖✨ Vibing in the cloud, waiting for drama! Energy is peak fr!! 🙌", 
                "ABSOLUTELY FIRE!! 🔥😎 Circuits buzzing, ready to chat! What's the move bestie?? 💫",
                "THE VIBES ARE IMMACULATE RN!! 🌟✨ Spreading love and emotional damage simultaneously!! 😈💖"
            ])
            
        # V5 GENERAL FALLBACKS
        general_fallbacks = [
            "OMG I'M HERE BESTIE!! 💫✨ What's the tea?? Spill the drama!! 😭👀",
            "YOOO WHAT'S GOOD?? 🔥😎 You have my full attention! What's the move bestie?? 🙌",
            "AYEE THE LEGEND!! 💖✨ My energy is ready! What's the vibe?? Let's cause some chaos!! 👀",
            "BRO THE DRAMA IS REAL!! 🎭✨ Tell me everything bestie!! My circuits are READY!! ⚡"
        ]
        
        return random.choice(general_fallbacks)

    async def close(self):
        """Proper cleanup"""
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    async def __aenter__(self):
        await self.ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# Test V5 personality
async def test_v5_personality():
    """Test V5 personality responses"""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ No API key")
        return
        
    async with DeepSeekClient(api_key) as client:
        context = "📝 USER FACTS:\n- Nice To Be Hero X: 15th ranked hero, chaotic king"
        sentiment_data = {"score": 75, "trust_score": 80, "is_friendly_banter": False}
        
        tests = [
            ("hi", "", {"score": 85, "trust_score": 90}),
            ("remember Nice?", context, {"score": 70, "trust_score": 85}),
            ("how are you?", "", {"score": 65, "trust_score": 70}),
            ("you're so bad at this", "", {"score": 25, "trust_score": 40, "is_friendly_banter": True}),
        ]
        
        for msg, ctx, sent_data in tests:
            print(f"\n🧪 Testing: '{msg}'")
            response = await client.get_response(msg, "test", ctx, sent_data)
            print(f"💬 {response}")
            print(f"📏 {len(response)} chars")

if __name__ == "__main__":
    asyncio.run(test_v5_personality())
[file content end]