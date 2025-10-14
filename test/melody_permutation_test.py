# melody_permutation_test_v3.py
import os
import asyncio
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

# Test users and messages
test_conversations = {
    "friend1": ["Hey Melody! How's your day going?", "I just finished watching some anime."],
    "friend2": ["Melody, tell me a joke!", "I'm feeling a bit down today."]
}

async def run_permutation_test():
    for user_id, messages in test_conversations.items():
        print(f"\n--- Conversation for {user_id} ---")
        for msg in messages:
            print(f"\nYou ({user_id}): {msg}")
            # Generate Melody's response
            response = await intelligence_orchestrator.generate_response(user_id, msg, ai_provider=ai_client)
            print(f"Melody: {response}")
            
            # Optional: TTS playback
            if TTS_ENABLED:
                tts = gTTS(response, lang="en")
                audio_file = f"tts_{user_id}.mp3"
                tts.save(audio_file)
                playsound.playsound(audio_file)
                os.remove(audio_file)

# Run the test
if __name__ == "__main__":
    asyncio.run(run_permutation_test())
