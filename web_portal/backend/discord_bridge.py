# discord_bridge.py - CURATED LEAGUE TROLL EDITION
import discord
from discord.ext import commands
import asyncio
import os
import re
import random
from dotenv import load_dotenv
from analytics import analytics

load_dotenv()

class DiscordBridge:
    def __init__(self, web_portal_ref):
        self.web_portal = web_portal_ref
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        self.target_channel_id = int(os.getenv('WEB_PORTAL_CHANNEL_ID', 1337024526923595786))
        self._announcement_sent = False
        self.setup_events()
    
    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'✅ DISCORD BRIDGE READY! Logged in as {self.bot.user}')
            print("🔮 Web portal bridge ready - announcement handled by main bot")
        
        @self.bot.event
        async def on_message(message):
            # Ignore bot messages and web portal messages to prevent loops
            if (message.author.bot or 
                message.channel.id != self.target_channel_id):
                return
            
            print(f"📥 DISCORD MESSAGE RECEIVED: {message.author.display_name}: {message.content}")
            
            # Send Discord message to web portal
            discord_msg = {
                'id': f"discord_{message.id}",
                'user': message.author.display_name,
                'message': message.content,
                'timestamp': message.created_at.isoformat(),
                'source': 'discord',
                'mysterious': False
            }
            
            # Track analytics
            analytics.track_message(discord_msg)
            
            # Broadcast to web clients
            if hasattr(self.web_portal, 'broadcast_message'):
                self.web_portal.broadcast_message(discord_msg)
                print(f"📥 DISCORD → WEB: {message.author.display_name}: {message.content}")
            else:
                print("❌ Web portal not available for broadcasting")
            
            # Process commands for Melody AI
            await self.bot.process_commands(message)
    
    async def send_to_discord(self, message_data):
        """Send message from web to Discord with CURATED LEAGUE TROLL NAMES"""
        try:
            channel = self.bot.get_channel(self.target_channel_id)
            if channel:
                message_content = message_data['message']
                
                # Convert Discord user IDs to proper mentions
                user_id_pattern = r'@(\d{17,19})'
                message_content = re.sub(user_id_pattern, r'<@\1>', message_content)
                
                # CURATED LEAGUE OF LEGENDS TROLL NAMES
                league_troll_names = [
                    "🐈 Fiddle Me Mommy says:"                    # Pure nightmare fuel
                                       # Which one is real?!
                ]
                
                # Pick random League troll name
                selected_name = random.choice(league_troll_names)
                discord_message = f"**{selected_name}** {message_content}"
                
                # Send with allowed mentions so pings actually work
                await channel.send(
                    discord_message,
                    allowed_mentions=discord.AllowedMentions(
                        users=True,
                        roles=False,  
                        everyone=False,
                        replied_user=False
                    )
                )
                print(f"📤 WEB → DISCORD LEAGUE: {selected_name}: {message_content}")
                return True
            else:
                print(f"❌ Channel {self.target_channel_id} not found")
        except Exception as e:
            print(f"❌ Failed to send to Discord: {e}")
        return False
    
    async def start(self):
        """Start the Discord bot"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if token:
            print("🔗 STARTING DISCORD BRIDGE...")
            try:
                await self.bot.start(token)
            except RuntimeError as e:
                if "There is no current event loop" in str(e):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    await self.bot.start(token)
                else:
                    raise e
        else:
            print("❌ No Discord token found in .env file")

# Global instance
_discord_bridge_instance = None

def setup_discord_bridge(web_portal_ref):
    global _discord_bridge_instance
    if _discord_bridge_instance is None:
        _discord_bridge_instance = DiscordBridge(web_portal_ref)
        print("🆕 Created new Discord bridge instance")
    else:
        print("♻️ Using existing Discord bridge instance")
    return _discord_bridge_instance