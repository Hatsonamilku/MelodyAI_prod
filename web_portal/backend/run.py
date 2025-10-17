# run.py - Production Launcher
import os
import sys
from app import app, socketio, web_portal
from discord_bridge import setup_discord_bridge
import threading
import asyncio

def start_discord_bridge():
    """Start Discord bridge in background"""
    try:
        discord_bridge = setup_discord_bridge(web_portal)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(discord_bridge.start())
    except Exception as e:
        print(f"❌ Discord bridge failed: {e}")

if __name__ == "__main__":
    print("🌐 MELODY AI WEB PORTAL - PRODUCTION LAUNCH")
    print("=" * 50)
    
    # Check for Discord token
    if not os.getenv('DISCORD_BOT_TOKEN'):
        print("❌ ERROR: DISCORD_BOT_TOKEN not found in environment")
        print("💡 Create a .env file with your bot token")
        sys.exit(1)
    
    # Start Discord bridge in background thread
    discord_thread = threading.Thread(target=start_discord_bridge, daemon=True)
    discord_thread.start()
    
    print("✅ Discord bridge started in background")
    print("🌐 Starting web portal on http://localhost:5000")
    print("🔮 Hatsona Milku is awakening...")
    
    # Start web server
    socketio.run(
        app, 
        host="0.0.0.0", 
        port=5000, 
        debug=False,  # Set to False in production
        allow_unsafe_werkzeug=True
    )