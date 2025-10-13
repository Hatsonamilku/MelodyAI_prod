import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("🔍 Environment Debug:")
print(f"DISCORD_BOT_TOKEN: {'✅ FOUND' if os.getenv('DISCORD_BOT_TOKEN') else '❌ MISSING'}")
print(f"DEEPSEEK_API_KEY: {'✅ FOUND' if os.getenv('DEEPSEEK_API_KEY') else '❌ MISSING'}")

if os.getenv('DISCORD_BOT_TOKEN'):
    token = os.getenv('DISCORD_BOT_TOKEN')
    print(f"Token length: {len(token)}")
    print(f"Token starts with: {token[:10]}...")