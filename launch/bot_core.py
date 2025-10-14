# melody_ai_v2/launch/bot_core.py
import os
import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MelodyBotCore")

# Core systems
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.memory_systems.permanent_facts import permanent_facts
from brain.memory_systems.semantic_memory import semantic_memory


class MelodyBotCore:
    def __init__(self, command_prefix: str = COMMAND_PREFIX):
        # Discord bot setup
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)

        # AI Client
        self.ai_client: Optional[DeepSeekClient] = None
        if DEEPSEEK_API_KEY:
            self.setup_ai_client(DEEPSEEK_API_KEY)

        # Memory & state
        self.is_ready = False

        # Register events
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_command_error)

        logger.info("🎵 Melody Bot Core initialized!")

    def setup_ai_client(self, api_key: str):
        """Setup DeepSeek AI client"""
        self.ai_client = DeepSeekClient(api_key)
        logger.info("✅ DeepSeek AI Client configured!")

    async def on_ready(self):
        logger.info(f"🎵 {self.bot.user} is online and ready!")
        logger.info(f"📊 Connected to {len(self.bot.guilds)} servers")
        logger.info(f"🤖 AI Client: {'✅ Ready' if self.ai_client else '❌ Not configured'}")
        self.is_ready = True

        # Set custom status
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="your conversations 💫"
        )
        await self.bot.change_presence(activity=activity)

    async def on_message(self, message: discord.Message):
        """Handle incoming messages"""
        if message.author.bot:
            return

        # Process commands first
        await self.bot.process_commands(message)

        # Detect mention or "melodyai" keyword
        should_respond = (
            self.bot.user.mentioned_in(message) or
            "melodyai" in message.content.lower()
        )

        if should_respond:
            await self.handle_ai_response(message)

    async def handle_ai_response(self, message: discord.Message):
        """Generate AI response considering user context"""
        try:
            user_id = str(message.author.id)
            user_context = permanent_facts.get_user_context(user_id)
            conversation_summary = permanent_facts.storage.data.get("users", {}).get(user_id, {}).get("conversation_summary", "")
            if conversation_summary:
                user_context += f"\n\n📝 Previous summary:\n{conversation_summary}"

            full_message = f"{user_context}\n\nUser says: {message.content}" if user_context else message.content

            logger.info(f"🧠 AI Request from {message.author}: '{message.content}'")

            # Generate AI response
            if self.ai_client:
                ai_response = await intelligence_orchestrator.generate_response(
                    user_id=user_id,
                    user_message=full_message,
                    ai_provider=self.ai_client
                )
            else:
                # Fallback responses
                fallback_messages = [
                    "Hi there! My AI brain isn't fully configured yet 💫",
                    "Hello! I need my DeepSeek API key to chat properly 🧠",
                    "Hey! AI is offline, but I remember our chats ✨",
                    "Hi! Full conversation requires my API key 💖"
                ]
                import random
                ai_response = random.choice(fallback_messages)

            await message.reply(ai_response)
            logger.info(f"✅ Response sent: {ai_response[:100]}...")

        except Exception as e:
            logger.error(f"❌ AI Response error: {e}", exc_info=True)
            fallback_messages = [
                "Oops! My circuits glitched 💫 Try again?",
                "Whoops! Technical difficulties 🎵",
                "Ack! Brain freeze ❄️ Let me reboot!"
            ]
            import random
            await message.reply(random.choice(fallback_messages))

    async def on_command_error(self, ctx, error):
        """Handle command errors gracefully"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command! Use `!help` to see what I can do 💫")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing arguments! Check usage 📝")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Command on cooldown! Try again in {error.retry_after:.1f}s")
        else:
            logger.error(f"❌ Command error: {error}", exc_info=True)
            await ctx.send("❌ Something went wrong! Let me try that again 🔄")

    async def close(self):
        """Graceful shutdown"""
        if self.ai_client:
            await self.ai_client.close()
        await self.bot.close()
        logger.info("🎵 Melody Bot Core shut down successfully!")

    def get_bot(self):
        """Return discord.py bot instance"""
        return self.bot


# --- Run directly ---
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN not found in .env")

    bot_core = MelodyBotCore()

    async def main():
        async with bot_core.get_bot():
            await bot_core.get_bot().start(TOKEN)

    asyncio.run(main())
