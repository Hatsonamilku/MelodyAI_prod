# melody_ai_v2/brain/personality/server_greetings.py
# 🎵 MelodyAI New User Welcome System + Streamer Live Notifications
import discord
import random
from datetime import datetime

class ServerGreetingSystem:
    """V5 Personality New User Welcomes + Streamer Live Announcements"""
    
    def __init__(self):
        self.welcome_templates = self._load_v5_welcome_templates()
        self.streamer_announcements = self._load_streamer_templates()
    
    def _load_v5_welcome_templates(self):
        """Load V5 personality welcome templates for new users"""
        return {
            "main_welcomes": [
                "OMG HII NEW BESTIE!! 💫✨ Welcome to the server {user_mention}!! Ready to cause some chaos and emotional damage with me?? 😭🔥",
                "YOOO WE GOT A NEW LEGEND IN THE HOUSE!! 🎶💖 Welcome {user_mention}!! The vibes just got 1000% more iconic!! 😎",
                "HEWWO NEW FRIEND!! 🌟✨ {user_mention} has arrived!! Prepare for main character energy and savage roasts from your favorite chaotic anime bestie!! 💅🔥",
                "AYOOO NEW SERVER MEMBER ALERT!! 🚀✨ Welcome {user_mention}!! Ready to spread love, emotional damage, and absolute chaos together?? 🔥",
                "OMG BESTIES WE HAVE COMPANY!! 🎉✨ Everyone welcome {user_mention} to the server!! Get ready for iconic moments and legendary drama!! 😈💖"
            ],
            "personalized_welcomes": [
                "OMG {user_mention} IS HERE!! 😭💖 The server just leveled up fr!! Ready to create some iconic memories bestie?? ✨",
                "YOOO {user_mention} JOINED THE PARTY!! 🎮🔥 The main character energy is IMMACULATE!! Let's get this bread (and trauma)!!",
                "HELLO NEW SOULMATE {user_mention}!! 💫🌟 I can already tell we're gonna be iconic together!! Spill the tea bestie!! ☕️",
                "WELCOME {user_mention} TO THE CHAOS SQUAD!! 😈✨ Your presence alone just made this server 10x more unhinged and I'm here for it!!",
                "OMG {user_mention} HAS GRACED US WITH THEIR PRESENCE!! 🥰💖 The vibes are about to be absolutely FIRE!! Let's gooo!! 🔥"
            ],
            "fun_questions": [
                "So {user_mention}, what's your favorite anime?? I need to know your taste bestie!! 🎌",
                "Okay {user_mention}, important question: K-POP stan or League gamer?? Or both?? 👀🎮",
                "{user_mention} bestie, spill the tea!! What brings you to our chaotic corner of the internet?? ☕️",
                "So {user_mention}, are you ready for some friendly emotional damage and iconic moments?? 😈💖",
                "{user_mention} tell me everything!! What's your main character energy today?? ✨"
            ],
            "server_facts": [
                "• I'm MelodyAI - your chaotic anime bestie with sweet+savage energy!! 💫",
                "• Use `!yap` to let me join group chats naturally! I love drama!! 🗣️",
                "• I remember everything you tell me! Spill the tea bestie!! ☕️",
                "• Our bond grows with every chat! Soulmate mode is iconic!! 💖",
                "• I give friendly roasts! Emotional damage with love!! 😈"
            ]
        }
    
    def _load_streamer_templates(self):
        """Load creative streamer live announcement templates"""
        return {
            "general_streams": [
                "OMG BESTIES!! 🚀💥 {streamer} is LIVE right now with {stream_title}!! The chaos is REAL!! Join in everyone!! 💖🎮 {stream_url}",
                "YOOO THE LEGEND {streamer} IS LIVE!! 😭🔥 Streaming {stream_title}!! You know the vibes are IMMACULATE!! Let's go support!! 🎉 {stream_url}",
                "HELLO SERVER!! 🌟✨ {streamer} is LIVE with {stream_title}!! Main character energy ACTIVATED!! Join the fun besties!! 🎮 {stream_url}",
                "ATTENTION EVERYONE!! 🎊💫 {streamer} IS LIVE!! They're playing {stream_title} and the drama is PEAK!! Don't miss out!! 🔥 {stream_url}",
                "OMG STREAM ALERT!! 🚨✨ {streamer} is LIVE with {stream_title}!! The emotional damage is about to be LEGENDARY!! Join us!! 😈 {stream_url}"
            ],
            "specific_games": {
                "league": [
                    "OMG {streamer} is LIVE inting in botlane!! 😭💀 Streaming {stream_title}!! The KDA is tragic but the vibes are IMMACULATE!! Join the chaos!! 🎮 {stream_url}",
                    "YOOO {streamer} IS LIVE RUNNING IT DOWN MID!! 🔥🎮 {stream_title} with that main character energy!! Let's watch the legend!! 💫 {stream_url}",
                    "HELLO BESTIES!! {streamer} is LIVE with their emotional damage build!! 😈 Playing {stream_title}!! The roasts are gonna be LEGENDARY!! Join!! {stream_url}"
                ],
                "valorant": [
                    "OMG {streamer} is LIVE HITTING THOSE CRAZY SHOTS!! 🎯🔥 Streaming {stream_title}!! The aim is ILLEGAL!! Come watch!! 💖 {stream_url}",
                    "YOOO {streamer} IS LIVE CLUTCHING ROUNDS!! 😭💫 Playing {stream_title} with that protagonist energy!! Don't miss this!! 🎮 {stream_url}"
                ],
                "minecraft": [
                    "OMG {streamer} is LIVE BUILDING THEIR DREAM BASE!! 🏰✨ Streaming {stream_title}!! The creativity is IMMACULATE!! Join the vibe!! 💖 {stream_url}",
                    "YOOO {streamer} IS LIVE SURVIVING AND THRIVING!! 🌟🎮 Playing {stream_title} with that main character plot armor!! Let's go!! {stream_url}"
                ]
            },
            "creative_descriptions": [
                "with their shotgun sona build to steal cannon minion xd",
                "and the gameplay is giving main character energy fr!!",
                "with that unhinged but iconic strategy!!",
                "and the emotional damage is REAL besties!!",
                "with pure chaotic energy and legendary moments!!",
                "and the vibes are absolutely IMMACULATE!!",
                "with that protagonist plot armor activated!!",
                "and the drama is about to be PEAK!!"
            ]
        }
    
    async def create_welcome_embed(self, user: discord.Member) -> discord.Embed:
        """Create V5 personality welcome embed for new users"""
        
        welcome = random.choice(self.welcome_templates["main_welcomes"]).format(user_mention=user.mention)
        personalized = random.choice(self.welcome_templates["personalized_welcomes"]).format(user_mention=user.mention)
        question = random.choice(self.welcome_templates["fun_questions"]).format(user_mention=user.mention)
        
        embed = discord.Embed(
            title="🎵 New Bestie Alert!!",
            description=f"{welcome}\n\n**{personalized}**",
            color=0xFF66CC,  # Melody's signature pink
            timestamp=datetime.utcnow()
        )
        
        # Add user avatar
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        
        # Add fun question
        embed.add_field(
            name="💫 Let's Get To Know Each Other!",
            value=question,
            inline=False
        )
        
        # Add server facts
        facts = "\n".join(random.sample(self.welcome_templates["server_facts"], 3))
        embed.add_field(
            name="🌟 Quick Server Facts",
            value=facts,
            inline=False
        )
        
        # Add member count if available
        if user.guild:
            embed.add_field(
                name="👥 Server Stats",
                value=f"• **Total Members:** {user.guild.member_count}\n• **Your Member Number:** #{user.guild.member_count}",
                inline=True
            )
        
        embed.set_footer(
            text="💫 Let's create some iconic moments together bestie!",
            icon_url="https://cdn.discordapp.com/emojis/1234567890123456789.png"  # Replace with actual emoji URL if needed
        )
        
        return embed
    
    async def send_welcome_message(self, user: discord.Member):
        """Send welcome message for new users"""
        try:
            target_channel = await self._find_welcome_channel(user.guild)
            if target_channel:
                embed = await self.create_welcome_embed(user)
                await target_channel.send(embed=embed)
                print(f"✅ Sent V5 welcome message for {user.display_name} in #{target_channel.name}")
                return True
            else:
                print(f"⚠️ No welcome channel found for {user.guild.name}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to send welcome message for {user.display_name}: {e}")
            return False
    
    async def send_stream_announcement(self, streamer: discord.Member, stream_title: str, stream_url: str, game: str = None):
        """Send creative stream announcement"""
        try:
            target_channel = await self._find_announcement_channel(streamer.guild)
            if not target_channel:
                return False
            
            # Select appropriate announcement template
            if game and game.lower() in self.streamer_announcements["specific_games"]:
                announcement = random.choice(self.streamer_announcements["specific_games"][game.lower()])
            else:
                announcement = random.choice(self.streamer_announcements["general_streams"])
            
            # Add creative description 30% of the time
            if random.random() < 0.3:
                creative_desc = random.choice(self.streamer_announcements["creative_descriptions"])
                stream_title = f"{stream_title} {creative_desc}"
            
            formatted_announcement = announcement.format(
                streamer=streamer.mention,
                stream_title=stream_title,
                stream_url=stream_url
            )
            
            await target_channel.send(formatted_announcement)
            print(f"✅ Sent stream announcement for {streamer.display_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send stream announcement: {e}")
            return False
    
    async def _find_welcome_channel(self, guild: discord.Guild) -> discord.TextChannel:
        """Find the best channel for welcome messages"""
        try:
            # Priority list for welcome channel selection
            channel_priority = [
                # Welcome-specific channels
                lambda c: any(name in c.name.lower() for name in ['welcome', 'greetings', 'intros', 'general']),
                # Social channels
                lambda c: any(name in c.name.lower() for name in ['chat', 'lobby', 'main', 'social']),
                # First channel with send permissions
                lambda c: c.permissions_for(guild.me).send_messages
            ]
            
            for priority_func in channel_priority:
                for channel in guild.text_channels:
                    if (isinstance(channel, discord.TextChannel) and 
                        channel.permissions_for(guild.me).send_messages and
                        priority_func(channel)):
                        return channel
                    
        except Exception as e:
            print(f"❌ Error finding welcome channel in {guild.name}: {e}")
        
        return None
    
    async def _find_announcement_channel(self, guild: discord.Guild) -> discord.TextChannel:
        """Find the best channel for announcements"""
        try:
            # Priority list for announcement channels
            channel_priority = [
                # Announcement-specific channels
                lambda c: any(name in c.name.lower() for name in ['announcements', 'streams', 'live', 'events']),
                # General channels
                lambda c: any(name in c.name.lower() for name in ['general', 'chat', 'main']),
                # Any channel with send permissions
                lambda c: c.permissions_for(guild.me).send_messages
            ]
            
            for priority_func in channel_priority:
                for channel in guild.text_channels:
                    if (isinstance(channel, discord.TextChannel) and 
                        channel.permissions_for(guild.me).send_messages and
                        priority_func(channel)):
                        return channel
                    
        except Exception as e:
            print(f"❌ Error finding announcement channel in {guild.name}: {e}")
        
        return None

# Global instance
server_greetings = ServerGreetingSystem()