# discord_bridge.py - ENHANCED WITH BETTER ERROR HANDLING
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
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.target_channel_id = int(os.getenv('WEB_PORTAL_CHANNEL_ID', 1337024526923595786))
        self.setup_events()
    
    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'✅ DISCORD BRIDGE READY! Logged in as {self.bot.user}')
            print(f'🏠 Connected to {len(self.bot.guilds)} servers:')
            for guild in self.bot.guilds:
                print(f'   - {guild.name} ({guild.member_count} members)')
            
            # Set initial status
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="the cloud portal 🌩️"
                )
            )
        
        @self.bot.event
        async def on_message(message):
            # Ignore bot messages
            if message.author.bot:
                return
            
            # Only listen to target channel
            if message.channel.id != self.target_channel_id:
                return
            
            print(f"📥 DISCORD MESSAGE: {message.author.display_name}: {message.content}")
            
            # Create message data for web portal
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
            
            # Process commands
            await self.bot.process_commands(message)
    
    async def send_to_discord(self, message_data):
        """Send message from web to Discord"""
        try:
            channel = self.bot.get_channel(self.target_channel_id)
            if channel and hasattr(channel, 'guild'):
                # Check permissions
                permissions = channel.permissions_for(channel.guild.me)
                if not permissions.send_messages:
                    print(f"❌ No permission to send messages in {channel.name}")
                    return False
                
                message_content = message_data['message']
                
                # Convert user ID mentions
                user_id_pattern = r'@(\d{17,19})'
                message_content = re.sub(user_id_pattern, r'<@\1>', message_content)
                
                # CURATED LEAGUE TROLL NAMES
                league_troll_names = [
                    "😨 Fiddle Me Mommy says:",
                    "💀 The Shadow Isles Watcher says:",
                    "🌙 Nocturne's Nightmare says:",
                    "🎭 Shaco's Clone says:",
                    "🌪️ Yasuo's Regret says:",
                    "❄️ Lissandra's Iceborn says:",
                    "🔮 Twisted Fate's Card says:",
                    "⚔️ Riven's Broken Blade says:",
                    "🌑 Diana's Moonlight says:",
                    "💥 Ziggs' Bomb says:"
                ]
                
                selected_name = random.choice(league_troll_names)
                discord_message = f"**{selected_name}** {message_content}"
                
                await channel.send(
                    discord_message,
                    allowed_mentions=discord.AllowedMentions(users=True)
                )
                print(f"📤 WEB → DISCORD: {selected_name}: {message_content}")
                return True
            else:
                print(f"❌ Channel {self.target_channel_id} not found or invalid")
                return False
        except Exception as e:
            print(f"❌ Failed to send to Discord: {e}")
            return False
    
    async def start(self):
        """Start the Discord bot"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if token:
            try:
                await self.bot.start(token)
            except Exception as e:
                print(f"❌ Discord login failed: {e}")
        else:
            print("❌ No Discord token found")

_discord_bridge_instance = None

def setup_discord_bridge(web_portal_ref):
    global _discord_bridge_instance
    if _discord_bridge_instance is None:
        _discord_bridge_instance = DiscordBridge(web_portal_ref)
    return _discord_bridge_instance