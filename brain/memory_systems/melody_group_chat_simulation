# melody_group_chat_simulation.py
import os
import asyncio
import random
from dotenv import load_dotenv

from services.ai_providers.deepseek_client import DeepSeekClient
from brain.personality.emotional_core import emotional_core
from brain.personality.adaptive_tones import tone_system

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

# Simulated multi-user chat
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

async def handle_user_message(user_id: str, user_msg: str):
    print(f"\n{user_id}: {user_msg}")

    # Emotional context
    context = emotional_core.get_emotional_context(user_id, user_msg)

    # DeepSeek AI response
    ai_response = await ai_client.get_response(user_msg, user_id)

    # Adapt response style
    final_response = tone_system.adapt_response_style(
        ai_response,
        sentiment_score=context["score"],
        contains_gen_alpha=context["gen_alpha_vibes"]
    )

    print(f"Melody: {final_response}")

    # Optional TTS
    if TTS_ENABLED:
        tts = gTTS(final_response, lang="en")
        audio_file = f"tts_{user_id}.mp3"
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

    # Random surprise comment with 25% probability
    if random.random() < 0.25:
        surprise = random.choice(surprise_comments)
        print(f"\nMelody (surprise): {surprise}")
        if TTS_ENABLED:
            tts = gTTS(surprise, lang="en")
            audio_file = f"tts_surprise_{user_id}.mp3"
            tts.save(audio_file)
            playsound.playsound(audio_file)
            os.remove(audio_file)

async def group_chat_simulation():
    # Flatten messages into a chronological list
    messages_queue = []
    max_turns = max(len(msgs) for msgs in multi_user_chat.values())
    for turn in range(max_turns):
        for user_id, msgs in multi_user_chat.items():
            if turn < len(msgs):
                messages_queue.append((user_id, msgs[turn]))

    # Randomize timing for more natural interleaving
    for user_id, user_msg in messages_queue:
        await handle_user_message(user_id, user_msg)
        await asyncio.sleep(random.uniform(1.0, 2.5))  # Simulate typing delay

async def main():
    await group_chat_simulation()
    await ai_client.close()  # Close DeepSeek session

if __name__ == "__main__":
    asyncio.run(main())
