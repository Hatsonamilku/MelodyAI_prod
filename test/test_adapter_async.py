# melody_ai_v2/test/test_adapter_async.py
import asyncio
import os
import sys

# Ensure root is in Python path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from services.discord_adapter import DiscordMelodyAdapter

async def test_adapter():
    adapter = DiscordMelodyAdapter(bot=None)
    user_id = "1234567890"
    
    print("🔹 Fetching user insights...")
    insights = await adapter.get_user_insights(user_id)
    
    print("Insights received:")
    print(insights)

if __name__ == "__main__":
    asyncio.run(test_adapter())
