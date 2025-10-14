# ==========================================================
# 🎭 MelodyAI v2 — Multi-User Interactive Personality Test Suite (Staggered)
# ==========================================================

import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.discord_adapter import DiscordMelodyAdapter
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.personality.emotional_core import EmotionalCore

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", 941401145690185810))

SIMULATED_USERS = {
    "Bob the Rizzler": {"desc": "super toxic, aggressive, trolling", "color": 0xE74C3C},
    "Yuli": {"desc": "chaotic, funny, like MelodyAI", "color": 0xF39C12},
    "Patrick": {"desc": "clueless, silly, random", "color": 0x3498DB},
    "Rita": {"desc": "intelligent, reads a lot, knows kpop & anime", "color": 0xFF69B4}
}

BASE_MESSAGES = {
    "Bob the Rizzler": [
        "LOL you can't be serious", "That's pathetic, honestly",
        "Bro you're so dumb fr", "This is trash"
    ],
    "Yuli": [
        "Don't take it too seriously lol", "Lmao that's chaotic",
        "Bro just vibing", "You're dramatic af"
    ],
    "Patrick": [
        "Uh… what are we doing again?", "I don't get it lol",
        "Is this even real?", "Why does this thing exist?"
    ],
    "Rita": [
        "Logic dictates this is the best solution", "I think we should analyze the data",
        "Everything has a reason", "Let's do this efficiently"
    ]
}

class MelodyMultiUserInteractiveBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

        self.melody_adapter = DiscordMelodyAdapter()
        self.ai_provider = DeepSeekClient(api_key=DEEPSEEK_API_KEY)
        self.emotional_core = EmotionalCore()

        self.auto_chat_enabled = False
        self.conversation_history = []

    async def on_ready(self):
        print(f"🧪 Melody Multi-User Bot logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name="Interactive AutoChat 🔄"))
        print(f"🔹 Listening in channel ID {TEST_CHANNEL_ID}")
        self.auto_chat_loop.start()
        self.periodic_summary.start()

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != TEST_CHANNEL_ID:
            return

        content_lower = message.content.lower()
        if content_lower.startswith("!loop"):
            self.auto_chat_enabled = not self.auto_chat_enabled
            status = "enabled ✅" if self.auto_chat_enabled else "disabled ⛔"
            await message.channel.send(f"🔁 AutoChat loop is now **{status}**!")
            return
        elif content_lower.startswith("!bench"):
            await message.channel.send("⚙️ Benchmark test suite (placeholder)")
            return

        await self.melody_adapter.process_discord_message(message, self.ai_provider, respond=False)
        self.conversation_history.append({"user": str(message.author), "message": message.content})

    # ------------------------------------------------------
    # 🔁 AUTO CHAT LOOP WITH STAGGERED USER MESSAGES
    # ------------------------------------------------------
    @tasks.loop(seconds=8)
    async def auto_chat_loop(self):
        if not self.auto_chat_enabled:
            return
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel:
            return

        # Cycle through all simulated users in random order
        users_order = list(SIMULATED_USERS.keys())
        random.shuffle(users_order)

        for simulated_user in users_order:
            user_info = SIMULATED_USERS[simulated_user]
            convo_text = ""
            for msg in self.conversation_history[-10:]:
                convo_text += f"{msg['user']}: {msg['message']}\n"

            prompt_user = f"""
            You are '{simulated_user}', a Discord user. Personality: {user_info['desc']}.
            Continue the conversation naturally with other users:
            {convo_text}
            Reply concisely in 1-3 sentences (~50 tokens), in character.
            """

            try:
                simulated_reply = await self.ai_provider.get_response(
                    user_id=simulated_user,
                    message=prompt_user
                )
            except Exception as e:
                print(f"⚠️ {simulated_user} DeepSeek error: {e}")
                simulated_reply = "(error retrieving AI response)"

            simulated_reply = simulated_reply[:250] + "…" if len(simulated_reply) > 250 else simulated_reply

            embed_user = discord.Embed(
                title=f"{simulated_user} says:",
                description=simulated_reply,
                color=user_info["color"],
                timestamp=datetime.utcnow()
            )
            await channel.send(embed=embed_user)
            self.conversation_history.append({"user": simulated_user, "message": simulated_reply})

            # Random small delay between users to stagger messages
            await asyncio.sleep(random.uniform(0.5, 2.5))

        # After all users, MelodyAI replies
        convo_text_melody = ""
        for msg in self.conversation_history[-10:]:
            convo_text_melody += f"{msg['user']}: {msg['message']}\n"

        prompt_melody = f"""
        You are MelodyAI. Continue the group conversation naturally.
        Consider all users and recent messages:
        {convo_text_melody}
        Reply concisely in 3-5 sentences (~50-80 tokens), witty and engaging.
        """

        try:
            melody_reply = await self.ai_provider.get_response(
                user_id="MelodyAI",
                message=prompt_melody
            )
        except Exception as e:
            print(f"⚠️ MelodyAI DeepSeek error: {e}")
            melody_reply = "(error retrieving AI response)"

        melody_reply = melody_reply[:350] + "…" if len(melody_reply) > 350 else melody_reply

        async with channel.typing():
            await asyncio.sleep(3)

        embed_ai = discord.Embed(
            title=f"💬 MelodyAI replies:",
            description=melody_reply,
            color=0x2ECC71,
            timestamp=datetime.utcnow()
        )
        await channel.send(embed=embed_ai)
        self.conversation_history.append({"user": "MelodyAI", "message": melody_reply})

    @auto_chat_loop.before_loop
    async def before_auto_chat(self):
        await self.wait_until_ready()

    # ------------------------------------------------------
    # 🧾 PERIODIC SUMMARY
    # ------------------------------------------------------
    @tasks.loop(minutes=5)
    async def periodic_summary(self):
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel or not self.conversation_history:
            return

        summary_prompt = f"""
        Summarize the last 10 messages concisely (max 3 sentences):
        {self.conversation_history[-10:]}
        """
        try:
            summary = await self.ai_provider.get_response(
                user_id="summary",
                message=summary_prompt
            )
            summary = summary[:350] + "…" if len(summary) > 350 else summary
            embed_summary = discord.Embed(
                title="🧠 Conversation Summary",
                description=summary,
                color=0x9B59B6,
                timestamp=datetime.utcnow()
            )
            await channel.send(embed=embed_summary)
        except Exception as e:
            print(f"⚠️ Summary generation failed: {e}")

    @periodic_summary.before_loop
    async def before_periodic_summary(self):
        await self.wait_until_ready()


# ==========================================================
# 🚀 ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    if not TOKEN or not DEEPSEEK_API_KEY:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN or DEEPSEEK_API_KEY not found in .env")

    bot = MelodyMultiUserInteractiveBot()

    async def main():
        async with bot:
            await bot.start(TOKEN)

    asyncio.run(main())
