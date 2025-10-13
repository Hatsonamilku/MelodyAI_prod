# melody_ai_v2/launch/main.py
import asyncio
import os
import signal
import sys
from dotenv import load_dotenv

# 🛠️ FIX: Properly load environment from root
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

# Import our bot components
from launch.bot_core import MelodyBotCore
from launch.command_system import CommandSystem

class MelodyAILauncher:
    def __init__(self):
        self.bot_core = None
        self.command_system = None
        
    async def launch(self):
        """Launch the complete Melody AI system"""
        print("🎵 Starting Melody AI v2...")
        
        # Initialize bot core
        self.bot_core = MelodyBotCore(command_prefix="!")
        
        # Setup AI client
        if deepseek_key:
            self.bot_core.setup_ai_client(deepseek_key)
        else:
            print("⚠️  DEEPSEEK_API_KEY not found - AI responses will be limited")
        
        # Setup command system
        self.command_system = CommandSystem(self.bot_core.get_bot())
        
        # 🆕 ADD CHAMP COMMANDS
        if riot_key:
            from services.champ_module import setup_champ_commands
            await setup_champ_commands(self.bot_core.get_bot(), riot_key, self.bot_core.ai_client)
            print("🎮 Champion commands loaded!")
        else:
            print("⚠️  RIOT_API_KEY not found - !champ command disabled")
        
        print("✅ All systems initialized! Logging into Discord...")
        
        try:
            # Start the bot
            await self.bot_core.get_bot().start(discord_token)
            return True
        except KeyboardInterrupt:
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def shutdown(self):
        """Graceful shutdown"""
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