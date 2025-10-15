# ==========================================================
# 🎭 MelodyAI v3 — ULTIMATE HYBRID TEST SUITE + RELATIONSHIP SYSTEM
# DEEPSEEK-POWERED USERS + PERMANENT FACTS + RELATIONSHIP ENGINE
# ==========================================================

import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
import sys
import time
import json
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.discord_adapter import DiscordMelodyAdapter
from services.ai_providers.deepseek_client import DeepSeekClient
from brain.personality.emotional_core import EmotionalCore
from brain.memory_systems.permanent_facts import permanent_facts

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", 1337024526923595786))

# 🎭 RELATIONSHIP SYSTEM CONFIGURATION
RELATIONSHIP_DATA_FILE = "relationship_data.json"

# Relationship Tiers with points, emojis, and emotional messages
RELATIONSHIP_TIERS = [
    {"name": "Soulmate", "min_points": 5000, "emoji": "💫", "color": 0xFF66CC, 
     "message": "You complete me... our souls are connected forever 💫",
     "busy_response": "I'm so sorry my baby 😔 I'm undergoing intensive tests to improve myself 💝 See you soon!"},
    {"name": "Twin Flame", "min_points": 3500, "emoji": "🔥", "color": 0xFF3366,
     "message": "We just GET each other on another level! 🔥",
     "busy_response": "Aww my flame 🔥 I'm busy with testing but I'll be back for you soon!"},
    {"name": "Kindred Spirit", "min_points": 2500, "emoji": "🌟", "color": 0xFF9966,
     "message": "We have such amazing chemistry! 💫",
     "busy_response": "Hey bestie! 🌟 I'm in testing mode right now, catch you later?"},
    {"name": "Bestie", "min_points": 1500, "emoji": "💖", "color": 0xFFD166,
     "message": "You're my favorite person to talk with! 💕",
     "busy_response": "Hey! I'm a bit busy with testing right now, talk later? 💕"},
    {"name": "Close Friend", "min_points": 800, "emoji": "😊", "color": 0x66CCFF,
     "message": "I really enjoy our conversations! 😊",
     "busy_response": "Testing mode active! I'll be back soon 😊"},
    {"name": "Acquaintance", "min_points": 300, "emoji": "👋", "color": 0xB0BEC5,
     "message": "Nice talking with you! 👋",
     "busy_response": "Busy testing right now, maybe later? 👋"},
    {"name": "Stranger", "min_points": 100, "emoji": "😒", "color": 0x9E9E9E,
     "message": "Hello there.",
     "busy_response": "Can't you see I'm busy right now? 😒 Testing mode active!"},
    {"name": "Rival", "min_points": 0, "emoji": "⚔️", "color": 0xE53935,
     "message": "We clearly don't see eye to eye... 😠",
     "busy_response": "WTF do you want? Can't you see I'm busy RN? ⚔️"}
]

class RelationshipSystem:
    def __init__(self, data_file=RELATIONSHIP_DATA_FILE):
        self.data_file = data_file
        self.relationships = self.load_relationships()
    
    def load_relationships(self):
        """Load relationship data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Error loading relationship data: {e}")
        return {}
    
    def save_relationships(self):
        """Save relationship data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.relationships, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving relationship data: {e}")
    
    def get_user_data(self, user_id):
        """Get or create user relationship data"""
        if user_id not in self.relationships:
            self.relationships[user_id] = {
                "points": 100,  # Start with 100 points (Stranger tier)
                "likes": 0,
                "dislikes": 0,
                "interactions": 0,
                "last_sync": datetime.utcnow().isoformat()
            }
        return self.relationships[user_id]
    
    def add_interaction(self, user_id, positive=True, points=10):
        """Add an interaction and update relationship points"""
        user_data = self.get_user_data(user_id)
        user_data["interactions"] += 1
        user_data["points"] += points
        user_data["last_sync"] = datetime.utcnow().isoformat()
        
        if positive:
            user_data["likes"] += 1
        else:
            user_data["dislikes"] += 1
        
        self.save_relationships()
        return user_data
    
    def get_tier_info(self, points):
        """Get tier information based on points"""
        for tier in RELATIONSHIP_TIERS:
            if points >= tier["min_points"]:
                current_tier = tier
                tier_index = RELATIONSHIP_TIERS.index(tier)
                break
        
        next_tier = RELATIONSHIP_TIERS[tier_index - 1] if tier_index > 0 else None
        
        # Calculate progress to next tier
        if next_tier:
            current_min = current_tier["min_points"]
            next_min = next_tier["min_points"]
            progress_percent = int(((points - current_min) / (next_min - current_min)) * 100)
            progress_percent = min(max(progress_percent, 0), 100)
        else:
            progress_percent = 100
        
        return current_tier, next_tier, progress_percent
    
    def calculate_compatibility(self, likes, interactions):
        """Calculate compatibility percentage"""
        if interactions == 0:
            return 0
        return int((likes / interactions) * 100)
    
    def get_busy_response(self, points):
        """Get emotional busy response based on relationship tier"""
        for tier in RELATIONSHIP_TIERS:
            if points >= tier["min_points"]:
                return tier["busy_response"]
        return RELATIONSHIP_TIERS[-1]["busy_response"]

# ULTIMATE USER PROFILES - FACT-RICH + DEEPSEEK INTELLIGENCE
SIMULATED_USERS = {
    "Bob the Rizzler": {
        "desc": "super toxic, aggressive, trolling, 25 years old from New York, loves Call of Duty",
        "color": 0xE74C3C,  # Red
        "fact_messages": [
            "My name is Bob and I'm from New York",
            "I'm 25 years old and I love Call of Duty",
            "Call me Bob, I live in Brooklyn",
            "My favorite game is Call of Duty",
            "I'm sick of this conversation",
            "I'm from New York, what about you?",
            "I love playing Call of Duty every day",
            "Feeling better now after being sick",
            "My name's Bob, remember that",
            "I enjoy toxic games like Call of Duty",
            "I'm 25, almost 26 next month",
            "Located in Manhattan, New York",
            "My favorite shooter is Call of Duty",
            "Not feeling well today, might be sick",
            "Everyone calls me Bob the Rizzler"
        ],
        "personality": "toxic, aggressive, trolling, loves arguing, always insults everything"
    },
    "Yuli": {
        "desc": "chaotic, funny, like MelodyAI, 22 from California, loves anime and pizza",
        "color": 0xF39C12,  # Orange
        "fact_messages": [
            "My name is Yuli and I'm from California",
            "I'm 22 years old, call me Yuli",
            "My favorite food is pizza, I love it",
            "I enjoy watching anime every weekend",
            "Based in Los Angeles, California",
            "I love anime like Naruto and One Piece",
            "My favorite anime character is Goku",
            "Not feeling well today, kinda sick",
            "I'm from California, the best state",
            "Pizza is my favorite food forever",
            "I'm 22, birthday is in March",
            "Located in LA, California",
            "My favorite anime is Demon Slayer",
            "Feeling better now, was sick yesterday",
            "Call me Yuli, that's my name"
        ],
        "personality": "chaotic, funny, energetic, loves anime and pizza, always vibing"
    },
    "Patrick": {
        "desc": "clueless, silly, random, 30 from Texas, loves Minecraft and burgers",
        "color": 0x3498DB,  # Blue
        "fact_messages": [
            "My name is Patrick, I'm from Texas",
            "I'm 30 years old, everyone calls me Pat",
            "My favorite game is Minecraft",
            "I love eating burgers every Friday",
            "Located in Houston, Texas",
            "Minecraft is the best game ever",
            "I'm from Texas, y'all remember that",
            "Feeling sick, might be the burgers",
            "Call me Patrick, that's my name",
            "I enjoy building in Minecraft",
            "I'm 30, feeling old sometimes",
            "Based in Dallas, Texas",
            "My favorite thing is Minecraft crafting",
            "Better now, was sick last week",
            "Name's Patrick, from Texas"
        ],
        "personality": "clueless, silly, random, easily confused, loves Minecraft and food"
    },
    "Rita": {
        "desc": "intelligent, reads a lot, knows kpop & anime, 28 from Seoul, loves reading and BTS",
        "color": 0xFF69B4,  # Pink
        "fact_messages": [
            "My name is Rita and I'm from Seoul",
            "I'm 28 years old, nice to meet you",
            "My favorite band is BTS, I love them",
            "I enjoy reading books every night",
            "I live in Seoul, South Korea",
            "BTS is my favorite music group",
            "I'm 28, almost 29 years old",
            "Feeling better after reading my book",
            "My name's Rita, from Seoul Korea",
            "I love BTS and their music",
            "I'm 28, turning 29 next year",
            "Based in Seoul, South Korea",
            "My favorite BTS song is Dynamite",
            "Was sick but recovered now",
            "Call me Rita, pleased to meet you"
        ],
        "personality": "intelligent, analytical, loves books and K-pop, always helpful and polite"
    }
}

class MelodyUltimateHybridBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

        self.melody_adapter = DiscordMelodyAdapter()
        self.ai_provider = DeepSeekClient(api_key=DEEPSEEK_API_KEY)
        self.emotional_core = EmotionalCore()
        self.relationship_system = RelationshipSystem()

        self.auto_chat_enabled = False
        self.conversation_history = []
        self.facts_extraction_count = 0
        self.cycle_count = 0
        self.last_message_time = 0  # Rate limiting

    async def on_ready(self):
        print(f"🧪 Melody ULTIMATE Hybrid Bot logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name="Hybrid Facts + Relationships 🔄💝"))
        print(f"🔹 Listening in channel ID {TEST_CHANNEL_ID}")
        
        # TEST CHANNEL ACCESS
        channel = self.get_channel(TEST_CHANNEL_ID)
        if channel:
            print(f"✅ Channel accessible: {channel.name} (ID: {channel.id})")
            # Test send a simple message first
            try:
                await channel.send("🔄 **MelodyAI v3 is ONLINE!** 💫\nTry `!relationship` to see our bond! ✨")
                print("✅ Test message sent successfully!")
            except Exception as e:
                print(f"❌ Test message failed: {e}")
        else:
            print("❌ Channel not found!")
            
        self.auto_chat_loop.start()
        self.periodic_summary.start()
        self.facts_report.start()

    async def safe_send(self, channel, content=None, embed=None):
        """Safe message sending with rate limit handling"""
        current_time = time.time()
        if current_time - self.last_message_time < 1.2:  # 1.2 second cooldown
            wait_time = 1.2 - (current_time - self.last_message_time)
            print(f"⏳ Rate limit cooldown: waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
        
        try:
            if embed:
                print(f"🚀 Sending embed: {embed.title}")
                message = await channel.send(embed=embed)
            else:
                print(f"🚀 Sending message: {content}")
                message = await channel.send(content)
                
            self.last_message_time = time.time()
            print(f"✅ SUCCESS: Message sent to Discord")
            return message
        except discord.HTTPException as e:
            print(f"❌ DISCORD HTTP ERROR: {e}")
        except discord.Forbidden as e:
            print(f"❌ DISCORD PERMISSION ERROR: {e} - Check bot permissions")
        except Exception as e:
            print(f"❌ UNKNOWN ERROR: {e}")
        return None

    async def on_message(self, message: discord.Message):
        if message.author.bot or message.channel.id != TEST_CHANNEL_ID:
            return

        content_lower = message.content.lower()
        print(f"📨 Message received: {content_lower} from {message.author}")
        
        # 🚨 CRITICAL FIX: Check for commands FIRST before adapter processes them
        if content_lower.startswith("!loop"):
            self.auto_chat_enabled = not self.auto_chat_enabled
            status = "enabled ✅" if self.auto_chat_enabled else "disabled ⛔"
            
            print(f"🔄 !loop command received - AutoChat now: {status}")
            
            embed = discord.Embed(
                title="🔁 AutoChat Loop",
                description=f"AutoChat is now **{status}**",
                color=0x2ECC71 if self.auto_chat_enabled else 0xE74C3C,
                timestamp=datetime.utcnow()
            )
            await self.safe_send(message.channel, embed=embed)
            return
            
        elif content_lower.startswith("!facts"):
            await self.show_facts_summary(message.channel)
            return
            
        elif content_lower.startswith("!bench"):
            await self.safe_send(message.channel, "⚙️ Running Permanent Facts Benchmark...")
            await self.run_facts_benchmark(message.channel)
            return
            
        elif content_lower.startswith("!relationship"):
            await self.handle_relationship_command(message)
            return
            
        elif content_lower.startswith("!leaderboard"):
            await self.handle_leaderboard_command(message)
            return
            
        elif content_lower.startswith("!gift"):
            await self.handle_gift_command(message)
            return

        # 🚨 CRITICAL: If !loop is enabled, REAL USERS are IGNORED for normal chat
        if self.auto_chat_enabled:
            # Real users get emotional busy response
            user_data = self.relationship_system.get_user_data(str(message.author))
            busy_response = self.relationship_system.get_busy_response(user_data["points"])
            
            # Send emotional busy notice
            embed = discord.Embed(
                title="🚧 Testing Mode Active",
                description=busy_response,
                color=0xFFA500,  # Orange warning color
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="💫 MelodyAI is currently in intensive testing mode")
            await self.safe_send(message.channel, embed=embed)
            return

        # ✅ NORMAL MODE: Process real user messages with BEAUTIFUL CARD-STYLE EMBEDS
        # Process user message for facts extraction
        extracted_facts = await permanent_facts.extract_personal_facts(str(message.author), message.content)
        if extracted_facts:
            await permanent_facts.store_facts(str(message.author), extracted_facts)
            self.facts_extraction_count += len(extracted_facts)

        # Add relationship interaction for real users
        user_data = self.relationship_system.add_interaction(str(message.author), positive=True, points=15)

        # 🚀 NEW: Get relationship info for the beautiful embed
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data["likes"], user_data["interactions"])

        # 🚀 NEW: Process with MelodyAI but use our beautiful card-style embed
        response = await self.melody_adapter.process_discord_message(
            message, 
            self.ai_provider, 
            respond=False  # 🚀 THIS IS KEY - adapter returns response instead of sending
        )
        
        if response:
            # 🎨 CREATE BEAUTIFUL CARD-STYLE EMBED
            embed = discord.Embed(
                color=current_tier["color"],
                timestamp=datetime.utcnow()
            )

            # 🎨 HEADER WITH LARGE PROMINENT MESSAGE
            embed.add_field(
                name=f"{current_tier['emoji']} MelodyAI → {message.author.display_name}",
                value=f"**{response}**",  # 🚀 LARGE BOLD TEXT for better readability
                inline=False
            )

            # 🎨 SEPARATOR
            embed.add_field(
                name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
                value="",
                inline=False
            )

            # 🎨 RELATIONSHIP PROGRESS SECTION
            tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
            compat_bar = "▰" * (compatibility // 20) + "▱" * (5 - compatibility // 20)

            relationship_section = f"""
❤️ **Love Meter:** {user_data['points']} pts • {current_tier['name']} {current_tier['emoji']}
{tier_bar} {progress_percent}% to {next_tier['name'] if next_tier else 'MAX'}

💞 **Compatibility:** {compatibility}%
{compat_bar}

💬 **Interactions:** {user_data['interactions']} (👍 {user_data['likes']} • 👎 {user_data['dislikes']})

🕒 **Last Sync:** {datetime.fromisoformat(user_data['last_sync']).strftime("%Y-%m-%d %H:%M:%S")}
"""

            # 🎨 CURRENT MOOD SYSTEM (Dynamic based on emotional core)
            mood_score = random.randint(40, 80)  # Simulated mood for now
            mood_emojis = {
                (0, 20): "😡 Angry",
                (21, 40): "😢 Sad", 
                (41, 60): "😐 Neutral",
                (61, 80): "😊 Happy",
                (81, 100): "😍 Ecstatic"
            }

            current_mood = "😐 Neutral"
            for range_tuple, mood in mood_emojis.items():
                if range_tuple[0] <= mood_score <= range_tuple[1]:
                    current_mood = mood
                    break

            mood_section = f"""
{current_mood.split()[0]} **Current Mood:** {mood_score} pts • {current_mood}
*(Changes dynamically: 😡 Angry, 😢 Sad, 😒 Rude, 😍 Happy, etc.)*
"""

            embed.add_field(
                name="💝 Relationship Progress",
                value=relationship_section,
                inline=False
            )

            embed.add_field(
                name="🌈 Current Emotional State", 
                value=mood_section,
                inline=False
            )

            # 🎨 CHAT HISTORY PREVIEW (Last 2 interactions)
            chat_history = ""
            recent_messages = self.conversation_history[-4:]  # Get last 4 messages
            
            if recent_messages:
                chat_history += "**💬 Recent Conversation Preview:**\n\n"
                for msg in recent_messages[-2:]:  # Show only last 2
                    timestamp = datetime.utcnow().strftime('%H:%M')
                    if msg["user"] == str(message.author):
                        display_name = message.author.display_name
                    else:
                        display_name = msg["user"]
                    
                    # Truncate long messages
                    preview_msg = msg['message'][:60] + "..." if len(msg['message']) > 60 else msg['message']
                    chat_history += f"• **{display_name}** — {timestamp}\n"
                    chat_history += f"  *\"{preview_msg}\"*\n\n"

            if chat_history:
                embed.add_field(
                    name="📝 Conversation Context",
                    value=chat_history,
                    inline=False
                )

            # 🎨 FOOTER WITH RELATIONSHIP SUMMARY
            embed.set_footer(
                text=f"💫 MelodyAI — Emotional Resonance Engine v5 | {current_tier['name']} Tier • {datetime.utcnow().strftime('%H:%M')}"
            )

            await self.safe_send(message.channel, embed=embed)
        
        self.conversation_history.append({"user": str(message.author), "message": message.content})

    # ------------------------------------------------------
    # 💝 RELATIONSHIP SYSTEM COMMANDS
    # ------------------------------------------------------
    async def handle_relationship_command(self, message):
        """Handle !relationship command with emotional busy notice if needed"""
        print(f"💝 Handling relationship command from {message.author}")
        
        target_user = message.author
        if message.mentions:
            target_user = message.mentions[0]
        
        user_data = self.relationship_system.get_user_data(str(target_user))
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data["likes"], user_data["interactions"])
        
        # Send emotional message first
        await message.channel.typing()
        await asyncio.sleep(1.5)
        await self.safe_send(message.channel, f"**{current_tier['emoji']} {current_tier['message']}**")
        
        # Then send the relationship embed
        await self.send_relationship_embed(message.channel, target_user, user_data, current_tier, next_tier, progress_percent, compatibility)

    async def handle_leaderboard_command(self, message):
        """Handle !leaderboard command"""
        print("🏆 Handling leaderboard command")
        await self.show_relationship_leaderboard(message.channel)

    async def handle_gift_command(self, message):
        """Handle !gift command to give points to other users"""
        print("🎁 Handling gift command")
        if not message.mentions:
            embed = discord.Embed(
                title="🎁 Gift Points",
                description="Usage: `!gift @user points`\nExample: `!gift @Yuli 50`",
                color=0xFFD700,
                timestamp=datetime.utcnow()
            )
            await self.safe_send(message.channel, embed=embed)
            return
        
        target_user = message.mentions[0]
        parts = message.content.split()
        
        if len(parts) < 3:
            embed = discord.Embed(
                title="❌ Invalid Format",
                description="Use: `!gift @user points`",
                color=0xE74C3C
            )
            await self.safe_send(message.channel, embed=embed)
            return
        
        try:
            points = int(parts[2])
            if points <= 0:
                raise ValueError("Points must be positive")
            
            # Add points to target user
            target_data = self.relationship_system.add_interaction(str(target_user), positive=True, points=points)
            
            embed = discord.Embed(
                title="🎁 Gift Sent!",
                description=f"**{message.author.display_name}** gifted **{points}** relationship points to **{target_user.display_name}**!",
                color=0xFFD700,
                timestamp=datetime.utcnow()
            )
            await self.safe_send(message.channel, embed=embed)
            
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid Points",
                description="Please provide a valid positive number of points.",
                color=0xE74C3C
            )
            await self.safe_send(message.channel, embed=embed)

    async def send_relationship_embed(self, channel, user, user_data, current_tier, next_tier, progress_percent, compatibility):
        """Send beautiful relationship embed for REAL USERS"""
        print(f"💞 Creating relationship embed for {user.display_name}")
        
        # Create progress bars
        tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
        next_tier_name = next_tier["name"] if next_tier else "MAX"
        tier_display = f"{tier_bar} `{progress_percent}% to {next_tier_name} {next_tier['emoji'] if next_tier else '💫'}`"
        
        compat_bar = "▰" * (compatibility // 20) + "▱" * (5 - compatibility // 20)
        compat_display = f"{compat_bar} `{compatibility}%`"
        
        # Create embed
        embed = discord.Embed(
            title=f"{current_tier['emoji']} MelodyAI → {user.display_name}",
            description=f"❤️ **Love Meter:** `{user_data['points']} pts` • *{current_tier['name']} {current_tier['emoji']}*\n{tier_display}",
            color=current_tier["color"],
            timestamp=datetime.utcnow()
        )
        
        # Add fields
        embed.add_field(
            name="💞 Compatibility", 
            value=compat_display, 
            inline=True
        )
        embed.add_field(
            name="💬 Interactions", 
            value=f"{user_data['interactions']} (👍 {user_data['likes']} • 👎 {user_data['dislikes']})", 
            inline=True
        )
        embed.add_field(
            name="🕒 Last Sync", 
            value=datetime.fromisoformat(user_data['last_sync']).strftime("%Y-%m-%d %H:%M:%S"), 
            inline=True
        )
        
        # Add emotional busy notice if in loop mode
        if self.auto_chat_enabled:
            busy_response = self.relationship_system.get_busy_response(user_data["points"])
            embed.add_field(
                name="🚧 Current Status",
                value=busy_response,
                inline=False
            )
        
        embed.set_footer(text=f"💫 MelodyAI — Emotional Resonance Engine v5 | {current_tier['name']} Tier")
        
        print(f"📤 Sending relationship embed for {user.display_name}")
        await self.safe_send(channel, embed=embed)

    async def show_relationship_leaderboard(self, channel):
        """Show relationship leaderboard"""
        print("🏆 Creating leaderboard embed")
        
        # Get all users with relationship data
        all_users = []
        for user_id, data in self.relationship_system.relationships.items():
            # Skip simulated users for leaderboard (they're temporary)
            if user_id in SIMULATED_USERS:
                continue
                
            # Try to get user object, fallback to user_id
            try:
                user = await self.fetch_user(int(user_id))
                display_name = user.display_name
            except:
                display_name = user_id
                
            all_users.append((display_name, data))
        
        # Sort by points
        all_users.sort(key=lambda x: x[1]["points"], reverse=True)
        top_users = all_users[:10]  # Top 10
        
        if not top_users:
            embed = discord.Embed(
                title="💝 Relationship Leaderboard",
                description="No relationship data yet! Start chatting to build your bond. 💫",
                color=0x9B59B6,
                timestamp=datetime.utcnow()
            )
            await self.safe_send(channel, embed=embed)
            return
        
        leaderboard_lines = []
        rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, (user_name, data) in enumerate(top_users):
            current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(data["points"])
            tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
            
            if i < len(rank_emojis):
                rank_emoji = rank_emojis[i]
            else:
                rank_emoji = f"{i+1}️⃣"
            
            if next_tier:
                progress_text = f"{tier_bar} `{progress_percent}% to {next_tier['name']} {next_tier['emoji']}`"
            else:
                progress_text = f"{tier_bar} `MAX`"
            
            leaderboard_lines.append(
                f"{rank_emoji} **{user_name}** {current_tier['emoji']} {current_tier['name']} — {data['points']} pts\n{progress_text}"
            )
        
        embed = discord.Embed(
            title="💝 MelodyAI → Top Bonds Leaderboard",
            description="\n".join(leaderboard_lines),
            color=0x9B59B6,
            timestamp=datetime.utcnow()
        )
        
        await self.safe_send(channel, embed=embed)

    # ------------------------------------------------------
    # 🔁 ULTIMATE HYBRID AUTO CHAT LOOP (SIMULATED USERS ONLY - LEGACY EMBEDS)
    # ------------------------------------------------------
    @tasks.loop(seconds=15)
    async def auto_chat_loop(self):
        print(f"🔁 CYCLE {self.cycle_count} - AutoChat Enabled: {self.auto_chat_enabled}")
        
        if not self.auto_chat_enabled:
            print("❌ Loop disabled, returning early")
            return
            
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel:
            print("❌ Channel not found")
            return

        print("🎯 STARTING HYBRID CHAT CYCLE (SIMULATED USERS ONLY)")
        self.cycle_count += 1
        
        # Track facts extracted in this cycle
        facts_extracted_this_cycle = {}

        # Cycle through all simulated users in random order
        users_order = list(SIMULATED_USERS.keys())
        random.shuffle(users_order)
        print(f"🔀 User order: {users_order}")

        for simulated_user in users_order:
            user_info = SIMULATED_USERS[simulated_user]
            
            # HYBRID APPROACH: 70% fact messages, 30% DeepSeek intelligent responses
            if random.random() < 0.7:
                # FACT-RICH TEMPLATE MESSAGE
                message = random.choice(user_info["fact_messages"])
                message_type = "📝 FACT"
                print(f"🎤 {simulated_user} using FACT template: {message}")
            else:
                # DEEPSEEK INTELLIGENT RESPONSE
                try:
                    # Build conversation context for DeepSeek
                    convo_context = ""
                    if self.conversation_history:
                        recent_msgs = self.conversation_history[-6:]  # Last 6 messages
                        convo_context = "Recent conversation:\n" + "\n".join(
                            [f"{msg['user']}: {msg['message']}" for msg in recent_msgs]
                        )
                    
                    deepseek_prompt = f"""
                    You are {simulated_user}. Personality: {user_info['personality']}
                    
                    {convo_context}
                    
                    Continue the conversation naturally in 1-2 sentences. Stay in character.
                    Reveal personal details naturally if it fits the conversation.
                    """
                    
                    message = await self.ai_provider.get_response(
                        user_id=f"deepseek_{simulated_user}",
                        message=deepseek_prompt
                    )
                    message_type = "🤖 DEEPSEEK"
                    print(f"🎤 {simulated_user} using DEEPSEEK: {message}")
                    
                except Exception as e:
                    print(f"❌ DeepSeek failed for {simulated_user}: {e}")
                    # Fallback to fact message
                    message = random.choice(user_info["fact_messages"])
                    message_type = "📝 FACT (Fallback)"
                    print(f"🎤 {simulated_user} using FALLBACK: {message}")

            # EXTRACT FACTS FROM THIS MESSAGE (works for both template and DeepSeek messages)
            extracted_facts = await permanent_facts.extract_personal_facts(simulated_user, message)
            if extracted_facts:
                await permanent_facts.store_facts(simulated_user, extracted_facts)
                facts_extracted_this_cycle[simulated_user] = extracted_facts
                self.facts_extraction_count += len(extracted_facts)

            # 🎭 LEGACY EMBED FOR SIMULATED USERS (NO RELATIONSHIP FIELDS)
            embed_user = discord.Embed(
                title=f"{message_type} - {simulated_user} says:",
                description=message,
                color=user_info["color"],
                timestamp=datetime.utcnow()
            )
            
            # Add fact count to embed if facts were extracted (LEGACY STYLE)
            if simulated_user in facts_extracted_this_cycle:
                fact_count = len(facts_extracted_this_cycle[simulated_user])
                embed_user.add_field(
                    name="🧠 Facts Extracted", 
                    value=f"{fact_count} new fact(s)", 
                    inline=True
                )
            
            print(f"📤 Sending LEGACY embed for {simulated_user}")
            sent_message = await self.safe_send(channel, embed=embed_user)
            if sent_message:
                print(f"✅ Message sent successfully for {simulated_user}")
                self.conversation_history.append({"user": simulated_user, "message": message})
            else:
                print(f"❌ FAILED to send message for {simulated_user}")

            # Small delay between users
            delay = random.uniform(2, 4)
            print(f"⏳ Waiting {delay:.1f}s before next user...")
            await asyncio.sleep(delay)

        # AFTER ALL USERS: Show facts summary
        if facts_extracted_this_cycle:
            summary_lines = ["**📊 FACTS EXTRACTED THIS CYCLE:**"]
            for user, facts in facts_extracted_this_cycle.items():
                fact_list = [f"`{f['key']}={f['value']}`" for f in facts]
                summary_lines.append(f"**{user}**: {', '.join(fact_list)}")
            
            embed_summary = discord.Embed(
                title="🧠 Permanent Facts Update",
                description="\n".join(summary_lines),
                color=0x9B59B6,  # Purple
                timestamp=datetime.utcnow()
            )
            await self.safe_send(channel, embed=embed_summary)

        # MELODYAI RESPONDS WITH CONTEXT FROM PERMANENT FACTS
        convo_text_melody = ""
        for msg in self.conversation_history[-8:]:
            convo_text_melody += f"{msg['user']}: {msg['message']}\n"

        # Get user contexts for MelodyAI
        user_contexts = []
        for user in SIMULATED_USERS.keys():
            context = await permanent_facts.get_user_context(user)
            if context:
                user_contexts.append(context)

        prompt_melody = f"""
        You are MelodyAI. Continue the group conversation naturally.
        
        Recent conversation:
        {convo_text_melody}
        
        User facts I remember:
        {' | '.join(user_contexts) if user_contexts else 'No user facts yet'}
        
        Reply concisely in 2-4 sentences, engaging and reference user facts if relevant.
        Be witty, fun, and interactive with the users.
        """

        try:
            melody_reply = await self.ai_provider.get_response(
                user_id="MelodyAI",
                message=prompt_melody
            )
            print("✅ MelodyAI response generated")
        except Exception as e:
            print(f"⚠️ MelodyAI DeepSeek error: {e}")
            melody_reply = "Hmm, something went wrong with my response generation..."

        async with channel.typing():
            await asyncio.sleep(2)

        # 🎭 LEGACY EMBED FOR MELODYAI RESPONSE
        embed_ai = discord.Embed(
            title=f"💬 MelodyAI replies:",
            description=melody_reply,
            color=0x2ECC71,  # Green
            timestamp=datetime.utcnow()
        )
        await self.safe_send(channel, embed=embed_ai)
        self.conversation_history.append({"user": "MelodyAI", "message": melody_reply})
        
        print("🎉 HYBRID CHAT CYCLE COMPLETED")

    @auto_chat_loop.before_loop
    async def before_auto_chat(self):
        await self.wait_until_ready()
        print("✅ Auto-chat loop is ready and waiting")

    # ------------------------------------------------------
    # 🧾 PERIODIC SUMMARY
    # ------------------------------------------------------
    @tasks.loop(minutes=3)
    async def periodic_summary(self):
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel or not self.conversation_history:
            return

        summary_prompt = f"""
        Summarize the last 8 messages concisely (max 2 sentences):
        {self.conversation_history[-8:]}
        """
        try:
            summary = await self.ai_provider.get_response(
                user_id="summary",
                message=summary_prompt
            )
            embed_summary = discord.Embed(
                title="🧠 Conversation Summary",
                description=summary,
                color=0x9B59B6,  # Purple
                timestamp=datetime.utcnow()
            )
            await self.safe_send(channel, embed=embed_summary)
        except Exception as e:
            print(f"⚠️ Summary generation failed: {e}")

    @periodic_summary.before_loop
    async def before_periodic_summary(self):
        await self.wait_until_ready()

    # ------------------------------------------------------
    # 📊 FACTS REPORTING
    # ------------------------------------------------------
    @tasks.loop(minutes=5)
    async def facts_report(self):
        """Show comprehensive facts report"""
        if not self.auto_chat_enabled:
            return
            
        channel = self.get_channel(TEST_CHANNEL_ID)
        if not channel:
            return

        # Get all stored facts
        all_facts = {}
        for user in SIMULATED_USERS.keys():
            user_facts = await permanent_facts.search_facts(user)
            if user_facts:
                all_facts[user] = user_facts

        if all_facts:
            report_lines = [f"📈 PERMANENT FACTS REPORT - Cycle {self.cycle_count}"]
            for user, facts in all_facts.items():
                fact_count = len(facts)
                sample_facts = [f[1] for f in facts[:3]]
                report_lines.append(f"**{user}**: {fact_count} facts - {', '.join(sample_facts)}{'...' if len(facts) > 3 else ''}")
            
            report_lines.append(f"\n**Total Facts Extracted**: {self.facts_extraction_count}")
            report_lines.append(f"**Total Cycles Completed**: {self.cycle_count}")
            
            embed_report = discord.Embed(
                title="📊 Permanent Facts System Report",
                description="\n".join(report_lines),
                color=0xE67E22,  # Orange
                timestamp=datetime.utcnow()
            )
            await self.safe_send(channel, embed=embed_report)

    @facts_report.before_loop
    async def before_facts_report(self):
        await self.wait_until_ready()

    # ------------------------------------------------------
    # 🔧 COMMAND HANDLERS
    # ------------------------------------------------------
    async def show_facts_summary(self, channel):
        """Show current facts summary"""
        summary_lines = ["🧠 CURRENT PERMANENT FACTS:"]
        
        for user in SIMULATED_USERS.keys():
            user_facts = await permanent_facts.search_facts(user)
            if user_facts:
                fact_list = [f"`{key}`" for _, key, _ in user_facts[:5]]
                summary_lines.append(f"**{user}**: {', '.join(fact_list)}{'...' if len(user_facts) > 5 else ''}")
            else:
                summary_lines.append(f"**{user}**: No facts yet")
        
        summary_lines.append(f"\n**Total Extraction Count**: {self.facts_extraction_count}")
        summary_lines.append(f"**Cycles Completed**: {self.cycle_count}")
        
        embed = discord.Embed(
            title="📝 Permanent Facts Status",
            description="\n".join(summary_lines),
            color=0x3498DB,  # Blue
            timestamp=datetime.utcnow()
        )
        await self.safe_send(channel, embed=embed)

    async def run_facts_benchmark(self, channel):
        """Run a quick benchmark test"""
        test_messages = [
            "My name is TestUser",
            "I'm from TestCity", 
            "I am 99 years old",
            "My favorite thing is testing"
        ]
        
        results = []
        for i, message in enumerate(test_messages):
            facts = await permanent_facts.extract_personal_facts("benchmark_user", message)
            results.append(f"{i+1}. '{message}' -> {len(facts)} facts")
        
        embed = discord.Embed(
            title="⚙️ Facts Benchmark Results",
            description="\n".join(results),
            color=0x95A5A6,  # Gray
            timestamp=datetime.utcnow()
        )
        await self.safe_send(channel, embed=embed)


# ==========================================================
# 🚀 ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    if not TOKEN or not DEEPSEEK_API_KEY:
        raise ValueError("⚠️ DISCORD_BOT_TOKEN or DEEPSEEK_API_KEY not found in .env")

    bot = MelodyUltimateHybridBot()

    async def main():
        async with bot:
            await bot.start(TOKEN)

    asyncio.run(main())