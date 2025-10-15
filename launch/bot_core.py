# melody_ai_v2/launch/bot_core.py - FIXED VERSION
import os
import sys
import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MelodyBotCore")

# Core systems - NOW WITH PROPER IMPORTS
try:
    from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
    from services.ai_providers.deepseek_client import DeepSeekClient
    from brain.memory_systems.permanent_facts import permanent_facts
    from brain.memory_systems.semantic_memory import semantic_memory
    from services.discord_adapter import DiscordMelodyAdapter
    from launch.command_system import CommandSystem  # 🆕 ADDED
    logger.info("✅ All core systems imported successfully!")
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    # Create fallbacks for missing components
    class FallbackOrchestrator:
        async def generate_response(self, user_id, user_message, ai_provider=None):
            return "YOOO I'm here bestie! 💫✨ My brain is still booting up but I'm ready to chat! What's good?? 🔥"
    intelligence_orchestrator = FallbackOrchestrator()
    
    class FallbackDeepSeekClient:
        async def get_response(self, *args, **kwargs):
            return "OMG HII BESTIE!! 💫✨ My AI brain is taking a quick nap but I'm still here! What's the tea?? 🔥"
        async def close(self):
            pass
    DeepSeekClient = FallbackDeepSeekClient
    
    class FallbackPermanentFacts:
        async def get_user_context(self, user_id):
            return ""
        async def extract_personal_facts(self, user_id, message):
            return []
        async def store_facts(self, user_id, facts):
            pass
    permanent_facts = FallbackPermanentFacts()
    
    class FallbackSemanticMemory:
        async def get_conversation_context(self, user_id, message):
            return ""
        async def store_conversation(self, user_id, user_message, bot_response):
            pass
    semantic_memory = FallbackSemanticMemory()
    
    class FallbackDiscordAdapter:
        async def process_discord_message(self, message, ai_provider=None, respond=True):
            return "YOOO I'm here! 💫✨ (Adapter not loaded)"
        async def handle_mention(self, message, ai_provider=None):
            return "Hey! You mentioned me? 💫 (Adapter not loaded)"
    DiscordMelodyAdapter = FallbackDiscordAdapter
    
    class FallbackCommandSystem:
        def __init__(self, bot):
            self.bot = bot
    CommandSystem = FallbackCommandSystem

class MelodyBotCore:
    def __init__(self, command_prefix: str = COMMAND_PREFIX):
        if not TOKEN:
            raise ValueError("❌ DISCORD_BOT_TOKEN not found in environment variables!")
            
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)

        self.ai_client: Optional[DeepSeekClient] = None
        if DEEPSEEK_API_KEY:
            self.setup_ai_client(DEEPSEEK_API_KEY)
        else:
            logger.warning("⚠️ DEEPSEEK_API_KEY not found - AI features disabled")

        self.discord_adapter = DiscordMelodyAdapter()
        logger.info("✅ Discord Melody Adapter initialized!")

        # 🆕 CRITICAL FIX: Connect command system
        self.command_system = CommandSystem(self.bot)
        logger.info("✅ Command System initialized!")

        self.is_ready = False
        self.processing_semaphore = asyncio.Semaphore(3)
        self.user_cooldowns = {}
        self.response_tracker = {}

        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_command_error)
        
        logger.info("🎵 Melody Bot Core initialized!")

    def setup_ai_client(self, api_key: str):
        try:
            self.ai_client = DeepSeekClient(api_key)
            logger.info("✅ DeepSeek AI Client configured!")
        except Exception as e:
            logger.error(f"❌ Failed to setup AI client: {e}")
            self.ai_client = None

    async def on_ready(self):
        logger.info(f"🎵 {self.bot.user} is online and ready!")
        logger.info(f"📊 Connected to {len(self.bot.guilds)} servers")
        logger.info(f"🤖 AI Client: {'✅ Ready' if self.ai_client else '❌ Not configured'}")
        logger.info(f"🔧 Discord Adapter: {'✅ Ready' if self.discord_adapter else '❌ Not configured'}")
        
        self.is_ready = True
        
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="your conversations 💫"
        )
        await self.bot.change_presence(activity=activity)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
            
        if self._is_log_message(message.content):
            return

        server_name = message.guild.name if message.guild else "DM"
        print(f"🔍 DEBUG: Message from {message.author} in server '{server_name}' channel '{message.channel.name}'")
        print(f"🔍 DEBUG: Message content: '{message.content[:100]}{'...' if len(message.content) > 100 else ''}'")
        print(f"🆕 MESSAGE HANDLER: Processing message ID {message.id}")

        # 🆕 CRITICAL FIX: Process commands FIRST and stop if it's a command
        await self.bot.process_commands(message)
        
        # If it's a command, stop here to avoid double processing
        if message.content.startswith(self.bot.command_prefix):
            print(f"🛑 DEBUG: Stopping - this is a command: '{message.content}'")
            return

        should_respond = (
            self.bot.user.mentioned_in(message) or
            "melodyai" in message.content.lower() or
            (
                len(message.content.strip()) > 3 and 
                not message.content.startswith('!')
            )
        )

        if should_respond:
            print(f"🎯 DEBUG: Should respond to message in server '{server_name}' channel '{message.channel.name}'")
            
            if len(message.content) > 800:
                await message.reply("Whoa bestie! That's a whole essay 😭 Can you break it into smaller chunks? (800 chars max) 💫")
                return

            user_id = str(message.author.id)
            current_time = asyncio.get_event_loop().time()
            
            if user_id in self.user_cooldowns and current_time - self.user_cooldowns[user_id] < 4:
                print(f"⏰ DEBUG: Skipping response - user {user_id} on cooldown")
                return
                
            self.user_cooldowns[user_id] = current_time
            
            await self.handle_ai_response_with_adapter(message)

    async def handle_ai_response_with_adapter(self, message: discord.Message):
        """Use Discord adapter for AI responses - WITH AI DEBUGGING"""
        if not self.is_ready:
            await message.reply("🔄 Bot still starting up... try again in a moment! 💫")
            return
        
        server_name = message.guild.name if message.guild else "DM"
        channel_name = message.channel.name
        
        print(f"🔧 DEBUG: Processing response for server '{server_name}' channel '{channel_name}'")
        
        user_id = str(message.author.id)
        current_time = asyncio.get_event_loop().time()
        
        request_key = f"{user_id}_{message.id}"
        if request_key in self.response_tracker:
            print(f"🔄 DEBUG: Skipping already processed message: {request_key}")
            return
            
        self.response_tracker[request_key] = current_time
        self._clean_old_tracker_entries()
        
        processing_msg = await message.reply("💫 Processing your message bestie...")
        
        response_sent = False
        
        async with self.processing_semaphore:
            try:
                print(f"🔧 DEBUG: Using Discord adapter to process message")
                
                # 🆕 CRITICAL DEBUG: Test AI directly first
                print(f"🧪 DIRECT AI TEST: Testing intelligence_orchestrator directly...")
                test_response = await intelligence_orchestrator.generate_response(
                    user_id=str(message.author.id),
                    user_message=message.content,
                    ai_provider=self.ai_client
                )
                print(f"🧪 DIRECT AI RESULT: '{test_response}'")
                print(f"🧪 DIRECT AI LENGTH: {len(test_response) if test_response else 0} chars")
                print(f"🧪 DIRECT AI IS EMPTY: {not test_response or test_response.strip() == ''}")
                
                # Original adapter call
                ai_response = await asyncio.wait_for(
                    self.discord_adapter.process_discord_message(message, self.ai_client, respond=False),
                    timeout=35.0
                )
                
                await processing_msg.delete()
                
                print(f"🔧 ADAPTER RESPONSE: '{ai_response}'")
                print(f"🔧 ADAPTER RESPONSE LENGTH: {len(ai_response) if ai_response else 0} chars")
                print(f"🔧 ADAPTER RESPONSE IS EMPTY: {not ai_response or ai_response.strip() == ''}")
                
                if ai_response and len(ai_response.strip()) > 10:
                    # 🆕 CRITICAL FIX: Only bot_core sends the message
                    await message.channel.send(ai_response)
                    logger.info(f"✅ Response sent to {message.author} in '{server_name}/{channel_name}': {ai_response[:80]}...")
                    response_sent = True
                else:
                    print("🔄 DEBUG: Skipping empty/short response")
                    if not ai_response and not response_sent:
                        # 🆕 Use the direct test response if adapter returned empty
                        if test_response and len(test_response.strip()) > 10:
                            print("🔄 DEBUG: Using direct AI response as fallback")
                            await message.channel.send(test_response)
                            response_sent = True
                        else:
                            await message.reply("Hmm, I didn't get a response from my brain! 💫 Try again?")
                            response_sent = True
                        
            except asyncio.TimeoutError:
                logger.warning(f"⏰ AI response timeout for {message.author} in '{server_name}'")
                await processing_msg.delete()
                if not response_sent:
                    fallback_messages = [
                        "OMG my brain is moving in slow motion today! 🐌💫 Try again?",
                        "Yikes! My AI circuits are taking a power nap! 😴⚡ One more time?",
                    ]
                    await message.reply(random.choice(fallback_messages))
                    response_sent = True
            except Exception as e:
                logger.error(f"❌ Adapter response error from {message.author} in '{server_name}': {e}", exc_info=True)
                await processing_msg.delete()
                if not response_sent:
                    fallback_messages = [
                        "Oops! My circuits glitched 💫 Try again?",
                        "Whoops! Technical difficulties 🎵 Let's try that again!", 
                    ]
                    await message.reply(random.choice(fallback_messages))
                    response_sent = True

    def _clean_old_tracker_entries(self):
        current_time = asyncio.get_event_loop().time()
        old_keys = [k for k, v in self.response_tracker.items() if current_time - v > 30]
        for key in old_keys:
            del self.response_tracker[key]
        if old_keys:
            print(f"🧹 DEBUG: Cleaned {len(old_keys)} old tracker entries")

    def _is_log_message(self, content: str) -> bool:
        log_indicators = [
            "INFO:MelodyBotCore:", "WARNING:MelodyBotCore:", "ERROR:MelodyBotCore:",
            "🧠 Processing message", "🎭 Emotional Debug", "Batches: 100%",
            "🌐 Sending request", "✅ DeepSeek response", "🔍 DEBUG:", "🎯 DEBUG:"
        ]
        return any(indicator in content for indicator in log_indicators)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command! Use !help to see what I can do 💫")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing arguments! Check usage 📝")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Command on cooldown! Try again in {error.retry_after:.1f}s")
        else:
            logger.error(f"❌ Command error: {error}", exc_info=True)
            await ctx.send("❌ Something went wrong! Let me try that again 🔄")

    async def close(self):
        if self.ai_client:
            await self.ai_client.close()
        await self.bot.close()
        logger.info("🎵 Melody Bot Core shut down successfully!")

    def get_bot(self):
        return self.bot

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN not found in .env")
        
    bot_core = MelodyBotCore()
    
    async def main():
        async with bot_core.get_bot():
            await bot_core.get_bot().start(TOKEN)
            
    asyncio.run(main())