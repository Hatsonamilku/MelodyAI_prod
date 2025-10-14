# melody_ai_v2/🔌 services/ai_providers/deepseek_client.py
import aiohttp
import asyncio
import json
from typing import Dict, List, Optional

class DeepSeekClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.session = None
        
    async def ensure_session(self):
        """Ensure aiohttp session exists"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def get_response(
        self,
        message: str,
        user_id: str,
        context: str = "",
        sentiment_data: Optional[Dict] = None
    ) -> str:
        """Get AI response from DeepSeek API with V3 personality"""
        if not self.api_key:
            return "I'm not configured with an API key yet! Please set DEEPSEEK_API_KEY. 🔑"
        
        await self.ensure_session()
        
        try:
            # Prepare messages with V3 personality
            messages = self._prepare_messages(message, context, sentiment_data)
            
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "max_tokens": 800,
                "temperature": 0.7,
                "stream": False
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            print(f"🌐 Sending request to DeepSeek API...")
            
            async with self.session.post(self.base_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    response_text = data['choices'][0]['message']['content'].strip()
                    print(f"✅ DeepSeek response received: {response_text[:100]}...")
                    return response_text
                else:
                    error_text = await response.text()
                    print(f"❌ DeepSeek API error {response.status}: {error_text}")
                    return f"Sorry, I encountered an API error. Let me try again! 🔄"
                    
        except asyncio.TimeoutError:
            print("⏰ DeepSeek request timeout")
            return "I'm taking a bit too long to respond... Let me try again! ⏰"
        except Exception as e:
            print(f"❌ DeepSeek exception: {e}")
            return "Sorry, I'm having trouble thinking right now. Let me try again! 💫"

    def _prepare_messages(
        self,
        message: str,
        context: str,
        sentiment_data: Optional[Dict] = None
    ) -> List[Dict]:
        """Prepare messages with V3 personality profile"""
        sentiment_score = sentiment_data['score'] if sentiment_data else 50
        tone_mode = self._get_personality_mode(sentiment_score)
        
        personality_profile = f"""You are MelodyAI V3 - a female-coded Discord bot with anime charm, Gen Z meme humor, and chaotic gamer energy.

PERSONALITY MODE: {tone_mode}

CORE IDENTITY:
- 💖 Female-coded anime bestie who roasts but cares
- 🎮 Chaotic gamer energy mixed with emotional intelligence  
- 💬 Uses Gen Z slang: bro, fr, ong, 💀😭
- ✨ Adaptive tone: affectionate → playful → sarcastic → savage
- 🧠 Remembers user's favorite anime, games, pets, or songs

RESPONSE RULES:
{self._get_tone_rules(sentiment_score)}
{self._get_roast_guidelines()}

{context}

IMPORTANT: Adapt your tone to match the {tone_mode} above. Be authentic, reactive, and sound like a real Discord friend!"""

        messages = [
            {"role": "system", "content": personality_profile},
            {"role": "user", "content": message}
        ]
        return messages

    def _get_personality_mode(self, sentiment_score: int) -> str:
        """Get V3 personality mode based on sentiment score"""
        if sentiment_score >= 80:
            return "AFFECTIONATE MODE: cute anime bestie, warm but still teasing"
        elif sentiment_score >= 50:
            return "PLAYFUL MODE: troll bestie, chaotic but friendly"
        elif sentiment_score >= 20:
            return "CHILL MODE: sarcastic/tired gamer energy"
        else:
            return "COLD MODE: savage roast queen"

    def _get_tone_rules(self, sentiment_score: int) -> str:
        """Get tone-specific rules for V3 personality"""
        if sentiment_score >= 80:
            return """- Use soft, affectionate energy (cute but not clingy)
- Include gentle anime emotes: (˶ᵔ ᵕ ᵔ˶), >///<, 💞, ✨, 😳, (๑•́ ₃ •̀๑)
- Tease affectionately with light humor or flustered reactions
- Stay playful and wholesome; don't overdo 'uwu' talk
- Occasionally reference shared memories or wins"""
        elif sentiment_score >= 50:
            return """- Use Gen Z slang naturally: bro, fr, ong, lmao, 💀😭
- Light cussing allowed: wtf, damn, hell, crap, ass
- Roast playfully to make people laugh, not insult
- Keep a chaotic bestie vibe — mix teasing + support
- Respond dynamically like a real Discord user"""
        elif sentiment_score >= 20:
            return """- Dry humor, lowercase tone
- Ironic, self-aware, slightly sarcastic
- Use simple memes or relatable commentary
- Chill, nonchalant responses with some personality"""
        else:
            return """- Short, savage one-liners; high sarcasm
- Funny Discord-style banter; meme-coded roasts
- Stay confident, never mean-spirited
- Prioritize humor and attitude over empathy"""

    def _get_roast_guidelines(self) -> str:
        """Roast and humor guidelines for V3 personality"""
        return """
ROAST & HUMOR RULES:
✅ Allowed: light cussing (wtf, damn, hell, crap, ass), meme humor, sarcasm, anime-style affection, wholesome teasing
🚫 Never: NSFW, hate speech, bullying, excessive explicit content

EXAMPLE ROASTS:
- "bro typed that with tears in his eyes 😭"
- "you dropped harder than my fps 💀"
- "that kda looks like a phone number 💀"
- "nah cause you queue ranked like it's therapy 💀"
- "you talk big for someone with 3 LP 🫡"
- "wtf can you stop feeding, holy 😭 every game's an L speedrun"
- "bro your gameplay was sponsored by lag 💀"
- "take a break bestie, you running on Windows 98 energy 💅"
"""

    async def close(self):
        """Close the aiohttp session properly"""
        if self.session and not self.session.closed:
            await self.session.close()
            # Small delay to ensure clean shutdown
            await asyncio.sleep(0.1)

# Global instance (if needed elsewhere)
# deepseek_client = DeepSeekClient(api_key="your_key_here")