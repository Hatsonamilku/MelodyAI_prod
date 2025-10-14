# melody_ai_combined_optimized test_suite_v3.py

import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from transformers import pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.discord_adapter import DiscordMelodyAdapter
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.personality.emotional_core import EmotionalCore
from brain.core_intelligence.intelligence_orchestrator import IntelligenceOrchestrator

# ---------------------------------------------------------
# Load environment
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", 941401145690185810))

# Lightweight NLP for classification
nlp = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    token=HUGGINGFACE_TOKEN
)
CONVERSATIONAL_LABELS = ["talking to me", "general chat"]

# ---------------------------------------------------------
# Simulated users + personalities
SIMULATED_USERS = {
    "Bob the Rizzler": "super toxic, aggressive, trolling, insults everything",
    "Dora the Explorer": "super annoying, complaining, overreacting, 'Karen' vibes",
    "Patrick": "super stupid, clueless, says silly things",
    "Rita": "super sweet, polite, intelligent, helpful"
}

BASE_MESSAGES = {
    "Bob the Rizzler": [
        "LOL you can't be serious", "That's pathetic, honestly",
        "Bro you're so dumb fr", "This is trash"
    ],
    "Dora the Explorer": [
        "Excuse me! This is unacceptable!", "I need to speak to your manager!",
        "Why is this not done correctly?", "This is ridiculous, seriously!"
    ],
    "Patrick": [
        "Uh… what are we doing again?", "I don't get it lol",
        "Is this even real?", "Why does this thing exist?"
    ],
    "Rita": [
        "Hi! How can I help you today?", "I think the solution is pretty simple here",
        "Let's take a logical approach", "Everything will be fine, don't worry!"
    ]
}

# ---------------------------------------------------------
class MelodyMultiUserPersonalityBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

        self.melody_adapter = DiscordMelodyAdapter()
        self.ai_provider = DeepSeekClient(api_key=DEEPSEEK_API_KEY)
        self.emotional_core = EmotionalCore()
        self.auto_chat_enabled = False
        self.active_message_history = []

        self.periodic_summary_task.start()
        self.auto_chat_loop_task.start()

    async def on_ready(self):
        print(f"🧪 Melody Multi-User Bot logged in as {self.user.name}")
        await self.change_presence(activity=discord.Game(name="Personality AutoChat 🔄"))
        print(f"🔹 Listening in channel ID {TEST_CHANNEL_ID}")

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != TEST_CHANNEL_ID:
            return

        content_lower = message.content.lower()

        if content_lower.startswith("!loop"):
            self.auto_chat_enabled = not self.auto_chat_enabled
            status = "enabled" if self.auto_chat_enabled else "disabled"
            await message.channel.send(f"🔁 AutoChat loop is now **{status}**!")
            return

        elif content_lower.startswith("!bench"):
            await message.channel.send("⚡ Running benchmark test suite (disabled in this light build)...")
            return

        await self.melody_adapter.process_discord_message(message, self.ai_provider, respond=False)
        self.active_message_history.append(message.content)

    # -----------------------------------------------------
    @tasks.loop(seconds=20)
    async def auto_chat_loop_task(self):
        """Auto-simulated multi-user chat loop with low-token DeepSeek queries"""
        if not self.auto_chat_enabled:
            return

        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel:
            return

        # Randomly select simulated user + message
        simulated_user = random.choice(list(SIMULATED_USERS.keys()))
        simulated_message = random.choice(BASE_MESSAGES[simulated_user])

        # MelodyAI sends what user said
        await channel.send(f"🧍‍♂️ **{simulated_user} SAID:** {simulated_message}")

        # Generate short DeepSeek-based reply (low token)
        compact_prompt = (
            f"You are MelodyAI in a Discord chat.\n"
            f"The user '{simulated_user}' ({SIMULATED_USERS[simulated_user]}) said: '{simulated_message}'.\n"
            f"Reply in a single short natural sentence (under 15 words)."
        )

        try:
            deepseek_reply = await self.ai_provider.ask(
                prompt=compact_prompt,
                max_tokens=50,
                temperature=0.8
            )
        except Exception as e:
            print(f"⚠️ DeepSeek error: {e}")
            deepseek_reply = "(error retrieving AI response)"

        # Send AI's reply
        await channel.send(f"💬 **MelodyAI:** {deepseek_reply}")
        print(f"[AutoChat] {simulated_user} -> {deepseek_reply}")

        self.active_message_history.append({
            "user": simulated_user,
            "message": simulated_message,
            "reply": deepseek_reply
        })

    @tasks.loop(minutes=5)
    async def periodic_summary_task(self):
        """Summarize conversation periodically (optional extension)"""
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel or not self.active_message_history:
            return

        summary_prompt = (
            "Summarize the last few exchanges between MelodyAI and simulated users in 3 sentences."
        )
        try:
            summary = await self.ai_provider.ask(
                prompt=summary_prompt,
                max_tokens=80,
                temperature=0.6
            )
            await channel.send(f"🧠 **Conversation Summary:** {summary}")
        except Exception as e:
            print(f"⚠️ Summary generation failed: {e}")

    @periodic_summary_task.before_loop
    @auto_chat_loop_task.before_loop
    async def before_tasks(self):
        await self.wait_until_ready()

# ---------------------------------------------------------
if __name__ == "__main__":
    if not TOKEN or not DEEPSEEK_API_KEY:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN or DEEPSEEK_API_KEY not found in .env")

    bot = MelodyMultiUserPersonalityBot()

    async def main():
        async with bot:
            await bot.start(TOKEN)

    asyncio.run(main())
