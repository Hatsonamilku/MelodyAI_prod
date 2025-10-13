#!/usr/bin/env python3
import os
import subprocess
import sys

def setup_melody():
    print("🎵 Setting up Melody AI v2...")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write('''# 🎵 MELODY AI CONFIGURATION
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 🎮 OPTIONAL: GAMING APIS
RIOT_API_KEY=your_riot_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
''')
        print("✅ .env file created! Please edit it with your API keys.")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("🎉 Setup complete!")
    print("🔑 Remember to:")
    print("   1. Edit .env with your API keys")
    print("   2. Run: cd '🚀 launch' && python main.py")

if __name__ == "__main__":
    setup_melody()