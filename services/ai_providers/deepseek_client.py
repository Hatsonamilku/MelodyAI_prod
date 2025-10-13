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
    
    async def get_response(self, message: str, user_id: str, 
                          context: str = "") -> str:
        """Get AI response from DeepSeek API"""
        if not self.api_key:
            return "I'm not configured with an API key yet! Please set DEEPSEEK_API_KEY. 🔑"
        
        await self.ensure_session()
        
        try:
            # Prepare messages array
            messages = self._prepare_messages(message, context)
            
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

    def _prepare_messages(self, message: str, context: str) -> List[Dict]:
        """Prepare messages array for API call"""
        messages = []
        
        # System message with context
        system_message = f"""You are Melody, an anime-style AI companion. Respond naturally and conversationally.

{context}

Remember:
- Be warm, friendly, and engaging
- Use occasional emojis but don't overdo it
- Show genuine interest in the user
- Reference their interests when relevant
- Keep responses conversational and not too long
- Adapt to their emotional state"""
        
        messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": message})
        
        return messages

    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()