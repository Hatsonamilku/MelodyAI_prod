# melody_ai_v2/run_melody.py
import os
import sys
from dotenv import load_dotenv

# Load environment variables from root
load_dotenv()

print("🎵 Launching Melody AI from root...")

# Check tokens
if not os.getenv('DISCORD_BOT_TOKEN'):
    print("❌ ERROR: No Discord token found!")
    sys.exit(1)

# Add current directory to path and import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from launch.main import main
    import asyncio
    
    print("✅ All systems ready! Starting bot...")
    asyncio.run(main())
    
except Exception as e:
    print(f"❌ Failed to start: {e}")
    import traceback
    traceback.print_exc()