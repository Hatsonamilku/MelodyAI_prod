# test_discord_only.py
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TEST_CHANNEL_ID = 1337024526923595786

class SimpleBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        channel = self.get_channel(TEST_CHANNEL_ID)
        if channel:
            await channel.send("🧪 Simple test message - is this working?")
            print("Test message sent!")
        await self.close()

client = SimpleBot(intents=discord.Intents.default())
client.run(TOKEN)