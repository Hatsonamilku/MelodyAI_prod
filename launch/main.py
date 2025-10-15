import asyncio
import os
import signal
import sys
from dotenv import load_dotenv

# 🛠️ Load environment from root
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(root_dir, '.env')
load_dotenv(env_path)

# Add root to Python path
sys.path.append(root_dir)

# Debug environment
discord_token = os.getenv('DISCORD_BOT_TOKEN')
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
riot_key = os.getenv('RIOT_API_KEY')

print(f"🔍 Environment loaded:")
print(f"   Discord Token: {'✅' if discord_token else '❌'}")
print(f"   DeepSeek Key: {'✅' if deepseek_key else '❌'}")
print(f"   Riot API Key: {'✅' if riot_key else '❌'}")

if not discord_token:
    print("❌ CRITICAL: No Discord token found!")
    print("💡 Make sure your .env file is in the root folder and contains DISCORD_BOT_TOKEN")
    sys.exit(1)

# Import bot components
from launch.bot_core import MelodyBotCore
from launch.command_system import CommandSystem
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator

# 🆕 ADD TEST COMMANDS CLASS HERE
import discord
from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_send(self, ctx):
        """Test if bot can send messages in this channel"""
        print(f"🔍 TEST: Manual test send command received in {ctx.channel.name}")
        try:
            msg = await ctx.send("✅ Test message received! Bot can send messages here.")
            print(f"✅ TEST: Successfully sent message with ID: {msg.id}")
        except Exception as e:
            print(f"❌ TEST: Failed to send: {e}")

    @commands.command()
    async def test_channel(self, ctx):
        """Debug channel permissions"""
        print(f"🔍 DEBUG CHANNEL: {ctx.channel.name} (ID: {ctx.channel.id})")
        
        perms = ctx.channel.permissions_for(ctx.guild.me)
        print(f"🔍 DEBUG CHANNEL: Send Messages: {perms.send_messages}")
        print(f"🔍 DEBUG CHANNEL: Read Messages: {perms.read_messages}")
        print(f"🔍 DEBUG CHANNEL: View Channel: {perms.view_channel}")
        
        await ctx.send(f"🔍 Channel Debug: Send Messages = {perms.send_messages}")

    @commands.command()
    async def test_ping(self, ctx):
        """Simple ping test"""
        await ctx.send("🏓 Pong! Bot is responsive!")

class MelodyAILauncher:
    def __init__(self):
        self.bot_core = None
        self.command_system = None

    async def launch(self):
        print("🎵 Starting Melody AI v2...")
        self.bot_core = MelodyBotCore(command_prefix="!")
       
        
        # 🆕 ADD THIS ONE LINE to load test commands
        await self.bot_core.get_bot().add_cog(TestCommands(self.bot_core.get_bot()))
        print("✅ Test commands loaded! Use !test_ping, !test_send, !test_channel.")
        
        print("✅ All systems initialized! Logging into Discord...")

        try:
            await self.bot_core.get_bot().start(discord_token)
        except KeyboardInterrupt:
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def shutdown(self):
        print("\n🎵 Melody AI is shutting down gracefully...")
        if self.bot_core:
            await self.bot_core.close()
        print("✅ Melody AI shut down successfully!")

# Global instance
melody_launcher = MelodyAILauncher()

async def main():
    try:
        await melody_launcher.launch()
    except KeyboardInterrupt:
        pass
    finally:
        await melody_launcher.shutdown()

def signal_handler(sig, frame):
    print(f"\n🎵 Received shutdown signal {sig}")
    asyncio.create_task(melody_launcher.shutdown())
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)