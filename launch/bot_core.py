# melody_ai_v2/launch/bot_core.py - COMPLETE FIXED VERSION
import os
import sys
import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional
from dotenv import load_dotenv
import random
import time

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MelodyBotCore")

# Fallback systems - DEFINED FIRST to avoid circular imports
class FallbackOrchestrator:
    async def generate_response(self, user_id, user_message, ai_provider=None):
        fallbacks = [
            "YOOO I'm here bestie! 💫✨ My brain is still booting up but I'm ready to chat! What's good?? 🔥",
            "OMG HII BESTIE!! 💫✨ My AI systems are warming up but I'm totally here for you! Spill the tea! ☕️",
            "Hey there! 👋 My deep thoughts are taking a quick nap but I'm still listening with chaotic energy! 💖"
        ]
        return random.choice(fallbacks)

class FallbackDeepSeekClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    async def get_response(self, message, user_id, context="", sentiment_data=None):
        v6_fallbacks = [
            "OMG HII BESTIE!! 💫✨ My AI brain is taking a quick nap but I'm still here! What's the tea?? 🔥",
            "YOOO I'm here! 💫✨ (AI system offline but I've got your back with V6 energy!)",
            "Hey there bestie! 👋 My deep thoughts are resting but I'm still listening with chaotic energy! 💖",
            "AWW BESTIEEE 💖 My circuits are rebooting but I'm still your favorite anime bestie! What's good?? 🌟"
        ]
        return random.choice(v6_fallbacks)
    
    async def close(self):
        pass

class FallbackPermanentFacts:
    async def get_user_context(self, user_id):
        return "Still learning about you! Tell me more about yourself bestie! 💫"
    
    async def extract_personal_facts(self, user_id, message):
        return []
    
    async def store_facts(self, user_id, facts):
        pass

class FallbackSemanticMemory:
    async def get_conversation_context(self, user_id, message):
        return ""
    
    async def store_conversation(self, user_id, user_message, bot_response):
        pass

class FallbackDiscordAdapter:
    async def process_discord_message(self, message, ai_provider=None, respond=True):
        return "YOOO I'm here! 💫✨ (Discord adapter not loaded but I'm still vibing!)"
    
    async def handle_mention(self, message, ai_provider=None):
        return "Hey! You mentioned me? 💫 (Adapter not loaded but I see you!)"
    
    async def debug_send_message(self, channel, message):
        return True
    
    async def debug_channel_permissions(self, channel):
        print(f"🔍 CHANNEL DEBUG: {channel.name} - Fallback mode")

class FallbackCommandSystem:
    def __init__(self, bot):
        self.bot = bot
        logger.info("🔄 Fallback Command System initialized")

# Initialize fallbacks
intelligence_orchestrator = FallbackOrchestrator()
permanent_facts = FallbackPermanentFacts()
semantic_memory = FallbackSemanticMemory()
DiscordMelodyAdapter = FallbackDiscordAdapter
CommandSystem = FallbackCommandSystem
DeepSeekClient = FallbackDeepSeekClient

class MelodyBotCore:
    def __init__(self, command_prefix: str = COMMAND_PREFIX):
        if not TOKEN:
            raise ValueError("❌ DISCORD_BOT_TOKEN not found in environment variables!")
            
        intents = discord.Intents.all()
        self.bot = commands.Bot(
            command_prefix=command_prefix, 
            intents=intents,
            help_command=None  # We'll use custom help
        )

        # Initialize with fallbacks first
        self.intelligence_orchestrator = intelligence_orchestrator
        self.permanent_facts = permanent_facts
        self.semantic_memory = semantic_memory
        self.DiscordMelodyAdapter = DiscordMelodyAdapter
        self.CommandSystem = CommandSystem
        
        # AI Client Configuration - will be set up properly later
        self.ai_client = None
        if DEEPSEEK_API_KEY:
            self.setup_ai_client(DEEPSEEK_API_KEY)
        else:
            logger.warning("⚠️ DEEPSEEK_API_KEY not found - AI features disabled")

        # Load real implementations after initialization
        self._load_real_implementations()

        # State Management
        self.is_ready = False
        self.processing_semaphore = asyncio.Semaphore(3)  # Limit concurrent processing
        self.user_cooldowns = {}
        self.response_tracker = {}
        self.conversation_history = []

        # 🆕 AUTO-YAP SYSTEM - Enhanced
        self.auto_yap_channels = set()
        self.last_auto_yap_time = 0
        self.auto_yap_cooldown = 30  # seconds
        self.auto_yap_trigger_words = [
            'hug', 'rage', 'sleepy', 'hungry', 'lmao', 'hell', 'omg', 'wow', 
            'seriously?', 'wtf', 'sad', 'happy', 'excited', 'angry', 'tired',
            'bored', 'funny', 'cute', 'awesome', 'amazing'
        ]

        # Event Registration
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_command_error)
        self.bot.event(self.on_guild_join)
        
        logger.info("🎵 Melody Bot Core initialized with all systems!")

    def _load_real_implementations(self):
        """Load real implementations after initialization to avoid circular imports"""
        try:
            from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator as real_intel
            self.intelligence_orchestrator = real_intel
            logger.info("✅ Real intelligence_orchestrator loaded!")
        except ImportError as e:
            logger.warning(f"⚠️ intelligence_orchestrator not available: {e}")

        try:
            from brain.memory_systems.permanent_facts import permanent_facts as real_facts
            self.permanent_facts = real_facts
            logger.info("✅ Real permanent_facts loaded!")
        except ImportError as e:
            logger.warning(f"⚠️ permanent_facts not available: {e}")

        try:
            from brain.memory_systems.semantic_memory import semantic_memory as real_semantic
            self.semantic_memory = real_semantic
            logger.info("✅ Real semantic_memory loaded!")
        except ImportError as e:
            logger.warning(f"⚠️ semantic_memory not available: {e}")

        try:
            from services.discord_adapter import DiscordMelodyAdapter as RealAdapter
            self.discord_adapter = RealAdapter()
            logger.info("✅ Real DiscordMelodyAdapter loaded!")
        except ImportError as e:
            logger.warning(f"⚠️ DiscordMelodyAdapter not available: {e}")
            self.discord_adapter = self.DiscordMelodyAdapter()

        try:
            from launch.command_system import CommandSystem as RealCommandSystem
            self.command_system = RealCommandSystem(self.bot)
            logger.info("✅ Real CommandSystem loaded!")
        except ImportError as e:
            logger.warning(f"⚠️ CommandSystem not available: {e}")
            self.command_system = self.CommandSystem(self.bot)

    def setup_ai_client(self, api_key: str):
        """Configure the AI client with proper error handling"""
        try:
            from services.ai_providers.deepseek_client import DeepSeekClient
            self.ai_client = DeepSeekClient(api_key)
            logger.info("✅ DeepSeek AI Client configured successfully!")
        except ImportError as e:
            logger.error(f"❌ Failed to import DeepSeekClient: {e}")
            self.ai_client = FallbackDeepSeekClient(api_key)
        except Exception as e:
            logger.error(f"❌ Failed to setup AI client: {e}")
            self.ai_client = FallbackDeepSeekClient(api_key)

    async def on_ready(self):
        """Comprehensive ready handler with detailed status"""
        logger.info(f"🎵 {self.bot.user} is online and ready!")
        logger.info(f"📊 Connected to {len(self.bot.guilds)} servers")
        
        # Detailed system status
        status_info = [
            f"🤖 AI Client: {'✅ Ready' if self.ai_client else '❌ Not configured'}",
            f"🔧 Discord Adapter: {'✅ Ready' if self.discord_adapter else '❌ Not configured'}",
            f"💾 Memory Systems: {'✅ Loaded' if not isinstance(self.permanent_facts, FallbackPermanentFacts) else '❌ Fallback'}",
            f"🧠 Intelligence: {'✅ Online' if not isinstance(self.intelligence_orchestrator, FallbackOrchestrator) else '❌ Fallback'}",
            f"🗣️ Auto-Yap: ✅ Ready ({len(self.auto_yap_channels)} channels)"
        ]
        
        for status in status_info:
            logger.info(status)
        
        self.is_ready = True
        
        # Set rich presence
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="your conversations 💫 | !help",
            details="V6 Personality Active"
        )
        await self.bot.change_presence(
            activity=activity,
            status=discord.Status.online
        )

    async def on_guild_join(self, guild):
        """Handle new server joins"""
        logger.info(f"🎵 Joined new server: {guild.name} (ID: {guild.id}, Members: {guild.member_count})")
        
        # Try to send welcome message to system channel or first text channel
        try:
            welcome_channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
            if welcome_channel:
                welcome_embed = discord.Embed(
                    title="💫 MelodyAI Has Arrived!",
                    description=(
                        "Hey besties! I'm **MelodyAI** - your chaotic anime bestie with V6 personality! 💖\n\n"
                        "**Quick Start:**\n"
                        "• Just mention me or use `!yap` to let me join conversations naturally! 🗣️\n"
                        "• Use `!help` to see all my commands! 📚\n"
                        "• I remember everything you tell me and build relationships over time! 🌱\n\n"
                        "Let's create some iconic moments together! ✨"
                    ),
                    color=0xFF66CC,
                    timestamp=discord.utils.utcnow()
                )
                await welcome_channel.send(embed=welcome_embed)
        except Exception as e:
            logger.warning(f"⚠️ Could not send welcome message to {guild.name}: {e}")

    async def on_message(self, message: discord.Message):
        """Enhanced message handler with comprehensive filtering"""
        if message.author.bot:
            return
            
        if self._is_log_message(message.content):
            return

        server_name = message.guild.name if message.guild else "DM"
        channel_name = message.channel.name if hasattr(message.channel, 'name') else "Unknown"
        
        print(f"🔍 MESSAGE: {message.author} in '{server_name}/{channel_name}': '{message.content[:100]}{'...' if len(message.content) > 100 else ''}'")

        # Process commands FIRST and stop if it's a command
        await self.bot.process_commands(message)
        
        # If it's a command, stop here to avoid double processing
        if message.content.startswith(self.bot.command_prefix):
            print(f"🛑 COMMAND: '{message.content}' - skipping normal processing")
            return

        # 🆕 ENHANCED RESPONSE CONDITIONS
        should_respond = False
        response_reason = "None"
        
        # Condition 1: Direct mention/tag (highest priority)
        if self.bot.user.mentioned_in(message):
            should_respond = True
            response_reason = "Direct mention"
            
        # Condition 2: Auto-yap mode with sophisticated triggers
        elif message.channel.id in self.auto_yap_channels:
            auto_yap_result = await self._should_auto_yap_respond(message)
            if auto_yap_result["should_respond"]:
                should_respond = True
                response_reason = f"Auto-yap: {auto_yap_result['reason']}"
                
        # Condition 3: Explicit "melodyai" call (case insensitive)
        elif "melodyai" in message.content.lower():
            should_respond = True
            response_reason = "Explicit call"

        # Log decision
        if should_respond:
            print(f"🎯 RESPONDING: {response_reason}")
        else:
            # Still process facts extraction for learning
            await self._process_facts_only(message)
            return

        # 🚀 PROCESS MESSAGE FOR RESPONSE
        if len(message.content) > 800:
            await message.reply("Whoa bestie! That's a whole essay 😭 Can you break it into smaller chunks? (800 chars max) 💫")
            return

        # Cooldown management
        user_id = str(message.author.id)
        current_time = asyncio.get_event_loop().time()
        
        if user_id in self.user_cooldowns and current_time - self.user_cooldowns[user_id] < 4:
            print(f"⏰ COOLDOWN: User {user_id} on cooldown")
            return
            
        self.user_cooldowns[user_id] = current_time
        
        # Process the response
        await self.handle_ai_response_with_adapter(message)

    async def _should_auto_yap_respond(self, message: discord.Message) -> dict:
        """Sophisticated auto-yap response determination"""
        current_time = time.time()
        
        # Global cooldown check
        if current_time - self.last_auto_yap_time < self.auto_yap_cooldown:
            return {"should_respond": False, "reason": "Global cooldown"}
            
        # User cooldown check
        user_id = str(message.author.id)
        if user_id in self.user_cooldowns and current_time - self.user_cooldowns[user_id] < 30:
            return {"should_respond": False, "reason": "User cooldown"}
            
        content_lower = message.content.lower()
        
        # 🎯 ENHANCED TRIGGER WORD DETECTION
        trigger_found = None
        for trigger in self.auto_yap_trigger_words:
            if trigger in content_lower:
                trigger_found = trigger
                break
        
        # 🎭 SOPHISTICATED RESPONSE LOGIC
        should_respond = False
        reason = "No trigger"
        
        if trigger_found:
            should_respond = True
            reason = f"Trigger: {trigger_found}"
        else:
            # Contextual response based on message characteristics
            message_length = len(message.content)
            has_question_mark = '?' in message.content
            has_exclamation = '!' in message.content
            
            # Higher chance for questions or emotional messages
            base_chance = 0.15
            if has_question_mark:
                base_chance += 0.10
            if has_exclamation:
                base_chance += 0.05
            if message_length > 50:
                base_chance += 0.05
                
            if random.random() < base_chance:
                should_respond = True
                reason = f"Natural conversation ({base_chance*100:.1f}% chance)"
        
        if should_respond:
            self.last_auto_yap_time = current_time
            self.user_cooldowns[user_id] = current_time
            
        return {"should_respond": should_respond, "reason": reason}

    async def _process_facts_only(self, message: discord.Message):
        """Process facts extraction without responding"""
        try:
            user_id = str(message.author.id)
            if hasattr(self, 'permanent_facts') and self.permanent_facts:
                extracted_facts = await self.permanent_facts.extract_personal_facts(user_id, message.content)
                if extracted_facts:
                    await self.permanent_facts.store_facts(user_id, extracted_facts)
                    print(f"📝 Facts extracted: {len(extracted_facts)} facts from {user_id}")
        except Exception as e:
            print(f"⚠️ Facts extraction failed: {e}")

    async def handle_yap_command(self, ctx):
        """Enhanced yap command with rich feedback"""
        channel_id = ctx.channel.id
        
        if channel_id in self.auto_yap_channels:
            self.auto_yap_channels.remove(channel_id)
            status = "disabled ❌"
            response = "Fine, I'll be quiet... but I'm still listening 👀\n*Use `!yap` again when you want me to join conversations!*"
            color = 0xE74C3C
        else:
            self.auto_yap_channels.add(channel_id)
            status = "enabled ✅"
            
            # Personalized response based on user
            user_data = getattr(self, 'relationship_system', None)
            if user_data:
                try:
                    points = user_data.get_user_data(str(ctx.author.id))["points"]
                    if points >= 800:
                        response = "wassup mah love i see u wanna talk today :3 im listening 💫\n*I'll join conversations naturally when I see emotional triggers!*"
                    elif points >= 300:
                        response = "i see someone wants someone to talk today xD im here 👋\n*I'll chime in when the vibe is right!*"
                    else:
                        response = "dafuq u want with me --' u done inting in botlane? 😒\n*Fine, I'll talk... sometimes.*"
                except:
                    response = "Yay! I'll join conversations naturally now! 🗣️💫\n*I respond to emotional words and sometimes join randomly!*"
            else:
                response = "Yay! I'll join conversations naturally now! 🗣️💫\n*I respond to emotional words and sometimes join randomly!*"
            
            color = 0x2ECC71
        
        embed = discord.Embed(
            title="🗣️ Auto-Yap Mode",
            description=f"**{status}** in {ctx.channel.mention}",
            color=color,
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="🎯 How it works:",
            value=response,
            inline=False
        )
        
        embed.add_field(
            name="🔧 Triggers:",
            value=f"I respond to: `{'`, `'.join(self.auto_yap_trigger_words[:8])}`... and more!",
            inline=False
        )
        
        embed.set_footer(text="Use !yap again to toggle me off")
        await ctx.send(embed=embed)

    async def handle_ai_response_with_adapter(self, message: discord.Message):
        """Comprehensive AI response handler with full debugging"""
        if not self.is_ready:
            await message.reply("🔄 Bot still starting up... try again in a moment! 💫")
            return
        
        server_name = message.guild.name if message.guild else "DM"
        channel_name = message.channel.name if hasattr(message.channel, 'name') else "Unknown"
        
        print(f"🔧 PROCESSING: Response for '{server_name}/{channel_name}'")

        user_id = str(message.author.id)
        current_time = asyncio.get_event_loop().time()
        
        # Request deduplication
        request_key = f"{user_id}_{message.id}"
        if request_key in self.response_tracker:
            print(f"🔄 DEDUPE: Skipping already processed message: {request_key}")
            return
            
        self.response_tracker[request_key] = current_time
        self._clean_old_tracker_entries()

        # 🆕 ADD TYPING INDICATOR
        async with message.channel.typing():
            processing_msg = await message.reply("💫 Processing your message bestie...")
            
            response_sent = False
            
            async with self.processing_semaphore:
                try:
                    print(f"🧠 AI PROCESS: Starting response generation...")
                    
                    # Test AI directly first for debugging
                    if hasattr(self, 'ai_client') and self.ai_client:
                        print(f"🧪 DIRECT AI TEST: Testing intelligence_orchestrator...")
                        test_response = await self.intelligence_orchestrator.generate_response(
                            user_id=str(message.author.id),
                            user_message=message.content,
                            ai_provider=self.ai_client
                        )
                        print(f"🧪 DIRECT AI RESULT: '{test_response[:100]}{'...' if len(test_response) > 100 else ''}'")
                    
                    # Original adapter call with enhanced timeout
                    ai_response = await asyncio.wait_for(
                        self.discord_adapter.process_discord_message(
                            message, 
                            getattr(self, 'ai_client', None), 
                            respond=False
                        ),
                        timeout=45.0  # Increased timeout for complex responses
                    )
                    
                    await processing_msg.delete()
                    
                    print(f"🔧 ADAPTER RESPONSE: '{ai_response[:100]}{'...' if len(ai_response) > 100 else ''}'")
                    
                    # Enhanced response validation
                    if ai_response and len(ai_response.strip()) > 10:
                        # Add to conversation history
                        self.conversation_history.append({
                            "user": str(message.author),
                            "message": message.content,
                            "response": ai_response,
                            "timestamp": discord.utils.utcnow().isoformat()
                        })
                        
                        # Keep history manageable
                        if len(self.conversation_history) > 100:
                            self.conversation_history = self.conversation_history[-100:]
                        
                        await message.channel.send(ai_response)
                        logger.info(f"✅ Response sent to {message.author} in '{server_name}/{channel_name}'")
                        response_sent = True
                    else:
                        print("🔄 EMPTY RESPONSE: Skipping empty/short response")
                        if not response_sent:
                            # Fallback system
                            if 'test_response' in locals() and test_response and len(test_response.strip()) > 10:
                                print("🔄 FALLBACK: Using direct AI response")
                                await message.channel.send(test_response)
                                response_sent = True
                            else:
                                fallback_responses = [
                                    "Hmm, I didn't get a response from my brain! 💫 Try again?",
                                    "My AI circuits are being shy right now! 🙈 One more time?",
                                    "Oops! My thoughts got lost in the void 🌌 Try that again?",
                                    "My brain glitched out for a sec! 🔄 Let's try again bestie!"
                                ]
                                await message.reply(random.choice(fallback_responses))
                                response_sent = True
                            
                except asyncio.TimeoutError:
                    logger.warning(f"⏰ AI response timeout for {message.author} in '{server_name}'")
                    await processing_msg.delete()
                    if not response_sent:
                        timeout_responses = [
                            "OMG my brain is moving in slow motion today! 🐌💫 Try again?",
                            "Yikes! My AI circuits are taking a power nap! 😴⚡ One more time?",
                            "My thoughts are buffering... 📡 Try again in a moment?",
                            "Brain loading... 10% complete... 😅 Let's try that again!"
                        ]
                        await message.reply(random.choice(timeout_responses))
                        response_sent = True
                except Exception as e:
                    logger.error(f"❌ Adapter response error from {message.author} in '{server_name}': {e}", exc_info=True)
                    await processing_msg.delete()
                    if not response_sent:
                        error_responses = [
                            "Oops! My circuits glitched 💫 Try again?",
                            "Whoops! Technical difficulties 🎵 Let's try that again!", 
                            "My brain had a moment there! 🌪️ One more time?",
                            "A wild error appeared! 🐉 Let's try that again bestie!"
                        ]
                        await message.reply(random.choice(error_responses))
                        response_sent = True

    def _clean_old_tracker_entries(self):
        """Clean up old response tracker entries"""
        current_time = asyncio.get_event_loop().time()
        old_keys = [k for k, v in self.response_tracker.items() if current_time - v > 30]
        for key in old_keys:
            del self.response_tracker[key]
        if old_keys:
            print(f"🧹 CLEANUP: Removed {len(old_keys)} old tracker entries")

    def _is_log_message(self, content: str) -> bool:
        """Detect and filter log messages"""
        log_indicators = [
            "INFO:MelodyBotCore:", "WARNING:MelodyBotCore:", "ERROR:MelodyBotCore:",
            "🧠 Processing message", "🎭 Emotional Debug", "Batches: 100%",
            "🌐 Sending request", "✅ DeepSeek response", "🔍 DEBUG:", "🎯 DEBUG:",
            "🔧 PROCESSING:", "🧪 DIRECT AI TEST:", "🔧 ADAPTER RESPONSE:",
            "🔄 EMPTY RESPONSE:", "🧹 CLEANUP:", "⏰ COOLDOWN:", "🎯 RESPONDING:",
            "🔍 MESSAGE:", "🛑 COMMAND:", "📝 Facts extracted:", "⚠️ Facts extraction failed:"
        ]
        return any(indicator in content for indicator in log_indicators)

    async def on_command_error(self, ctx, error):
        """Enhanced error handling with user-friendly messages"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command! Use `!help` to see what I can do 💫")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing arguments for `{ctx.command.name}`! Check usage with `!help {ctx.command.name}` 📝")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Command on cooldown! Try again in {error.retry_after:.1f}s")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command! 🔒")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have permission to execute this command! Check my permissions 🔧")
        else:
            logger.error(f"❌ Command error in {ctx.command.name}: {error}", exc_info=True)
            error_responses = [
                "❌ Something went wrong! Let me try that again 🔄",
                "💫 My brain glitched on that command! Try again?",
                "🌪️ Technical difficulties! Let's give that another shot!",
                "🔧 Command malfunction! Attempting reboot... just kidding, try again! 😅"
            ]
            await ctx.send(random.choice(error_responses))

    async def close(self):
        """Graceful shutdown with resource cleanup"""
        logger.info("🎵 Melody Bot Core shutting down gracefully...")
        
        # Close AI client
        if self.ai_client:
            await self.ai_client.close()
            logger.info("✅ AI Client closed")
        
        # Close bot connection
        await self.bot.close()
        logger.info("✅ Discord connection closed")
        
        # Cleanup other resources
        self.auto_yap_channels.clear()
        self.response_tracker.clear()
        self.user_cooldowns.clear()
        
        logger.info("🎵 Melody Bot Core shut down successfully!")

    def get_bot(self):
        """Get the underlying discord.py bot instance"""
        return self.bot

    def get_system_status(self):
        """Get comprehensive system status"""
        return {
            "ai_client": "✅ Ready" if self.ai_client else "❌ Disabled",
            "discord_adapter": "✅ Ready" if self.discord_adapter else "❌ Fallback",
            "auto_yap_channels": len(self.auto_yap_channels),
            "conversation_history": len(self.conversation_history),
            "response_tracker": len(self.response_tracker),
            "user_cooldowns": len(self.user_cooldowns),
            "is_ready": self.is_ready
        }

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN not found in .env")
        
    bot_core = MelodyBotCore()
    
    async def main():
        async with bot_core.get_bot():
            await bot_core.get_bot().start(TOKEN)
            
    asyncio.run(main())