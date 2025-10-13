# melody_ai_v2/launch/bot_core.py
import discord
from discord.ext import commands
import asyncio
from typing import Optional

# Import our core systems
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.memory_systems.permanent_facts import permanent_facts
from brain.memory_systems.semantic_memory import semantic_memory

class MelodyBotCore:
    def __init__(self, command_prefix: str = "!"):
        # Discord bot setup
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        
        # Core systems
        self.ai_client: Optional[DeepSeekClient] = None
        self.is_ready = False
        
        # Register events
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.event(self.on_command_error)
        
        print("🎵 Melody Bot Core initialized!")

    def setup_ai_client(self, api_key: str):
        """Setup AI client with API key"""
        self.ai_client = DeepSeekClient(api_key)
        print("✅ DeepSeek AI Client configured!")

    async def on_ready(self):
        """Called when bot logs in successfully"""
        print(f"🎵 {self.bot.user} is online and ready!")
        print(f"📊 Connected to {len(self.bot.guilds)} servers")
        print(f"🤖 AI Client: {'✅ Ready' if self.ai_client else '❌ Not configured'}")
        self.is_ready = True
        
        # Set custom status
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="your conversations 💫"
        )
        await self.bot.change_presence(activity=activity)

    async def on_message(self, message):
        """Handle all incoming messages"""
        if message.author.bot:
            return
        
        # Process commands first
        await self.bot.process_commands(message)
        
        # Check if bot is mentioned for AI response
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            await self.handle_ai_response(message)

    async def handle_ai_response(self, message):
        """Process AI response for mentions"""
        try:
            user_id = str(message.author.id)
            
            print(f"🧠 AI Request from {message.author}: '{message.content}'")
            
            # Generate AI response
            if self.ai_client:
                ai_response = await intelligence_orchestrator.generate_response(
                    user_id=user_id,
                    user_message=message.content,
                    ai_provider=self.ai_client
                )
            else:
                # Fallback responses when AI is not available
                fallbacks = [
                    "Hi there! I'd love to chat, but I need my AI brain configured first! 💫",
                    "Hello! To have proper conversations, please set up my DeepSeek API key! 🧠",
                    "Hey! I'm here, but my advanced thinking needs an API key setup! ✨",
                    "Hi! I can remember things about you, but for full AI conversations I need my API key configured! 💖"
                ]
                import random
                ai_response = random.choice(fallbacks)
            
            # Send response
            await message.reply(ai_response)
            
            print(f"✅ Response sent: {ai_response[:100]}...")
            
        except Exception as e:
            print(f"❌ AI Response error: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback response
            fallbacks = [
                "Oops! My circuits glitched for a second 💫 Let me try that again!",
                "Whoops! Technical difficulties 🎵 One moment please~",
                "Ack! Brain freeze ❄️ Let me reboot real quick!"
            ]
            import random
            await message.reply(random.choice(fallbacks))

    async def on_command_error(self, ctx, error):
        """Handle command errors gracefully"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Unknown command! Use `!melody_help` to see what I can do! 💫")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing arguments! Check `!melody_help` for usage. 📝")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Command on cooldown! Try again in {error.retry_after:.1f}s")
        else:
            print(f"❌ Command error: {error}")
            await ctx.send("❌ Something went wrong! Let me try that again. 🔄")

    async def close(self):
        """Cleanup resources"""
        if self.ai_client:
            await self.ai_client.close()
        print("🎵 Melody Bot Core shut down successfully!")

    def get_bot(self):
        """Get the discord.py bot instance"""
        return self.bot