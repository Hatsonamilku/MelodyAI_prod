import os
import sys
import asyncio
import random

# Make the parent folder (melody_ai_v2) visible to Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator

# Optional TTS
try:
    from gtts import gTTS
    import playsound
    TTS_ENABLED = True
except ImportError:
    print("gTTS or playsound not installed, audio will be skipped")
    TTS_ENABLED = False

# Load environment variables
load_dotenv()
DEESEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Initialize AI client
ai_client = DeepSeekClient(api_key=DEESEEK_API_KEY)

# ... rest of your script unchanged ...


# Multi-user conversation simulation
multi_user_chat = {
    "Alice": [
        "Hey Melody! I had the best day ever! 😍",
        "I watched Naruto all night, it was epic!"
    ],
    "Bob": [
        "Melody, my ranked game was terrible 😭",
        "I can't believe my KDA was 0/12/3 💀"
    ],
    "Charlie": [
        "Melody you're so cute! 💖",
        "I love talking to you, you know everything about me ✨"
    ]
}

# Surprise comments Melody can inject
surprise_comments = [
    "By the way, did you guys hear about the latest anime episode? 😏",
    "Just a thought, but maybe you should take a little break! ✨",
    "I’m curious… what’s your favorite game moment? 🎮",
    "Did someone say snack time? 🍪",
    "*sparkles* Feeling extra magical today! 💫",
    "Wait, did you really do that? 😲"
]

async def simulate_multi_user_chat():
    max_turns = max(len(messages) for messages in multi_user_chat.values())
    
    # Track personality drift per user
    personality_log = {user: [] for user in multi_user_chat.keys()}

    for turn in range(max_turns):
        for user_id, messages in multi_user_chat.items():
            if turn < len(messages):
                user_msg = messages[turn]
                print(f"\n{user_id}: {user_msg}")
                
                response = await intelligence_orchestrator.generate_response(
                    user_id=user_id,
                    user_message=user_msg,
                    ai_provider=ai_client
                )
                
                # Log personality indicators
                emotional_context = intelligence_orchestrator._build_ai_context(
                    user_id, user_msg, 
                    intelligence_orchestrator._generate_fallback_response(user_msg, {})
                )
                personality_log[user_id].append({
                    "message": user_msg,
                    "response": response
                })

                print(f"Melody: {response}")

                # Optional TTS
                if TTS_ENABLED:
                    tts = gTTS(response, lang="en")
                    audio_file = f"tts_{user_id}.mp3"
                    tts.save(audio_file)
                    playsound.playsound(audio_file)
                    os.remove(audio_file)

                # Surprise comment with 30% probability
                if random.random() < 0.3:
                    surprise = random.choice(surprise_comments)
                    print(f"\nMelody (surprise): {surprise}")
                    if TTS_ENABLED:
                        tts = gTTS(surprise, lang="en")
                        audio_file = f"tts_surprise_{user_id}.mp3"
                        tts.save(audio_file)
                        playsound.playsound(audio_file)
                        os.remove(audio_file)

    # Print final memory & personality analytics
    print("\n📊 --- Personality & Memory Analytics ---")
    for user_id, logs in personality_log.items():
        print(f"\nUser: {user_id}")
        for i, entry in enumerate(logs):
            print(f" Turn {i+1}:")
            print(f"  Message: {entry['message']}")
            print(f"  Melody Response: {entry['response'][:80]}...")  # Truncate for readability
        
        insights = intelligence_orchestrator.get_user_insights(user_id)
        print(f"  ✅ Insights: {insights}")

if __name__ == "__main__":
    async def main():
        try:
            await simulate_multi_user_chat()
        finally:
            await ai_client.close()  # Properly close aiohttp session

    asyncio.run(main())
