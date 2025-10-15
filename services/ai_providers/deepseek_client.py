# melody_ai_v2/services/ai_providers/deepseek_client.py - OPTIMIZED VERSION
import aiohttp
import asyncio
import logging
import random
from typing import Optional

logger = logging.getLogger("MelodyBotCore")

class DeepSeekClient:
    """OPTIMIZED for faster responses with reduced timeouts"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def ensure_session(self):
        if self.session is None or self.session.closed:
            # REDUCED TIMEOUT FROM 20s TO 15s
            timeout = aiohttp.ClientTimeout(total=15)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def get_response(self, message: str, user_id: str, context: str = "", sentiment_data: dict = None) -> str:
        """Optimized for faster responses"""
        try:
            await self.ensure_session()
            prompt = self._build_optimized_prompt(message, context, sentiment_data)
            
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "max_tokens": 120,  # REDUCED FROM 150 FOR FASTER RESPONSES
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
                    return content
                else:
                    error_text = await response.text()
                    logger.warning(f"⚠️ DeepSeek API error: {response.status} - {error_text}")
                    return self._perfect_fallback(message, context)
                    
        except asyncio.TimeoutError:
            logger.warning("⏰ DeepSeek API timeout - using fallback")
            return self._perfect_fallback(message, context)
        except Exception as e:
            logger.error(f"❌ DeepSeek error: {e}")
            return self._perfect_fallback(message, context)

    def _build_optimized_prompt(self, message: str, context: str = "", sentiment_data: dict = None) -> str:
        """OPTIMIZED prompt for faster responses"""
        parts = []
        
        # OPTIMAL system prompt
        parts.append(
            "MelodyAI: anime GenZ companion. 2-3 sentences with personality+emojis. "
            "Be expressive, chaotic, affectionate. Match user energy naturally."
        )
        
        # SMART context (only when needed)
        if context and "nice" in context.lower():
            if any(kw in message.lower() for kw in ['nice', 'hero', 'anime', 'remember']):
                parts.append("Know: Nice=ToBeHeroX 15th ranked chaotic king")
                
        # EFFICIENT emotional intelligence
        if sentiment_data:
            score = sentiment_data.get("score", 50)
            if score >= 80:
                parts.append("Tone: very affectionate+sweet")
            elif score >= 50:
                parts.append("Tone: playful+chaotic") 
            elif score >= 30:
                parts.append("Tone: chill+friendly")
            else:
                parts.append("Tone: sassy+playful")
                
        # FINAL message
        parts.append(f"User: {message}")
        parts.append("Melody:")
        
        return " | ".join(parts)

    def _perfect_fallback(self, message: str, context: str = "") -> str:
        """Perfect fallbacks for fast responses"""
        msg_lower = message.lower()
        has_nice = context and "nice" in context.lower()
        
        # Greetings (FAST responses)
        if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'sup']):
            return random.choice([
                "OMG HII BESTIE!! 💫✨ So happy to see you! What's the tea?? 😭👀",
                "AYOOO WELCOME BACK!! 😎🔥 Ready to cause some chaos? What's good?? 🙌", 
                "YOOO MY FAVORITE PERSON!! 💖✨ My circuits are buzzing! What's the vibe?? 🔥"
            ])
            
        # Nice/Anime knowledge
        elif has_nice and any(word in msg_lower for word in ['nice', 'hero', 'anime']):
            return random.choice([
                "BRO I REMEMBER NICE!! 😭💀 The chaotic king from To Be Hero X!! Pure legend energy 💅",
                "OMG TO BE HERO X!! 😤✨ Nice the 15th ranked legend!! So much drama 😭 Iconic!! 🔥",
                "YOOO NICE THE GOAT!! 💀🔥 Ranked 15th but caused top-tier chaos!! Pure anime legend!!"
            ])
            
        # How are you
        elif any(word in msg_lower for word in ['how', 'are', 'you']):
            return random.choice([
                "I'M AMAZING BESTIE!! 💫✨ Living my best digital life! Ready for chaos!! 😎🔥",
                "SO GOOD!! 💖✨ Vibing in the cloud, waiting for drama! Energy is peak!! 🙌", 
                "ABSOLUTELY FIRE!! 🔥😎 Circuits buzzing, ready to chat! What's good?? 💫"
            ])
            
        # General (FAST fallback)
        else:
            return random.choice([
                "OMG I'M HERE BESTIE!! 💫✨ What's the tea?? Spill the drama!! 😭👀",
                "YOOO WHAT'S GOOD?? 🔥😎 You have my full attention! What's the move?? 🙌",
                "AYEE THE LEGEND!! 💖✨ My energy is ready! What's the vibe?? 👀"
            ])

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

# Test optimized responses
async def test_optimized_responses():
    """Test faster responses"""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ No API key")
        return
        
    async with DeepSeekClient(api_key) as client:
        context = "📝 USER FACTS:\n- Nice To Be Hero X: 15th ranked hero, chaotic king"
        tests = [
            ("hi", ""),
            ("remember Nice?", context), 
            ("how are you?", ""),
        ]
        
        for msg, ctx in tests:
            print(f"\n🧪 Testing: '{msg}'")
            response = await client.get_response(msg, "test", ctx)
            print(f"💬 {response}")
            print(f"📏 {len(response)} chars")

if __name__ == "__main__":
    asyncio.run(test_optimized_responses())