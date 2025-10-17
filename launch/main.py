import asyncio
import os
import signal
import sys
import random
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# 🛠️ Load environment from root
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(root_dir, '.env')
load_dotenv(env_path)

# Add root to Python path
sys.path.append(root_dir)

# Debug environment
discord_token = os.getenv('DISCORD_BOT_TOKEN')
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
riot_key = os.getenv('RIOT_API_KEY')

print(f"🔍 Environment loaded:")
print(f"   Discord Token: {'✅' if discord_token else '❌'}")
print(f"   DeepSeek Key: {'✅' if deepseek_key else '❌'}")
print(f"   Riot API Key: {'✅' if riot_key else '❌'}")

if not discord_token:
    print("❌ CRITICAL: No Discord token found!")
    print("💡 Make sure your .env file is in the root folder and contains DISCORD_BOT_TOKEN")
    sys.exit(1)

# Import bot components
try:
    from bot_core import MelodyBotCore
    print("✅ MelodyBotCore imported successfully!")
except ImportError as e:
    print(f"❌ Failed to import MelodyBotCore: {e}")
    sys.exit(1)

# 🆕 RELATIONSHIP SYSTEM CONFIGURATION
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
                    data = json.load(f)
                    for user_id, user_data in data.items():
                        data[user_id] = self._migrate_user_data(user_data)
                    return data
        except Exception as e:
            print(f"❌ Error loading relationship data: {e}")
        return {}
    
    def _migrate_user_data(self, user_data):
        """Migrate old user data to new structure with all required fields"""
        default_data = {
            "points": 100,
            "likes": 0,
            "dislikes": 0,
            "neutral_interactions": 0,
            "gifts_received": 0,
            "gifts_given": 0,
            "conversation_depth": 0,
            "interactions": 0,
            "last_sync": datetime.utcnow().isoformat(),
            "compatibility_history": [],
            "trust_score": 50,
            "onboarding_complete": False,
            "collected_facts": []
        }
        
        for key, value in user_data.items():
            default_data[key] = value
            
        if "neutral_interactions" not in user_data:
            if "interactions" in user_data and "likes" in user_data and "dislikes" in user_data:
                total_specific = user_data.get("likes", 0) + user_data.get("dislikes", 0)
                default_data["neutral_interactions"] = max(0, user_data.get("interactions", 0) - total_specific)
            else:
                default_data["neutral_interactions"] = 0
                
        return default_data
    
    def save_relationships(self):
        """Save relationship data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.relationships, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving relationship data: {e}")
    
    def get_user_data(self, user_id):
        """Get or create user relationship data with ALL required fields"""
        if user_id not in self.relationships:
            self.relationships[user_id] = {
                "points": 100,
                "likes": 0,
                "dislikes": 0,
                "neutral_interactions": 0,
                "gifts_received": 0,
                "gifts_given": 0,
                "conversation_depth": 0,
                "interactions": 0,
                "last_sync": datetime.utcnow().isoformat(),
                "compatibility_history": [],
                "trust_score": 50,
                "onboarding_complete": False,
                "collected_facts": []
            }
        else:
            self.relationships[user_id] = self._migrate_user_data(self.relationships[user_id])
            
        return self.relationships[user_id]
    
    def add_interaction(self, user_id, interaction_type="neutral", points=10, message_content=""):
        """Add an interaction with sophisticated tracking"""
        user_data = self.get_user_data(user_id)
        user_data["interactions"] += 1
        user_data["last_sync"] = datetime.utcnow().isoformat()
        
        # Update trust score based on interaction
        if interaction_type == "positive":
            user_data["likes"] += 1
            user_data["points"] += points
            user_data["trust_score"] = min(100, user_data["trust_score"] + 2)
            if len(message_content) > 20:
                user_data["conversation_depth"] += 1
                user_data["points"] += 5
                user_data["trust_score"] = min(100, user_data["trust_score"] + 3)
                
        elif interaction_type == "negative":
            user_data["dislikes"] += 1
            user_data["points"] -= points // 2
            user_data["trust_score"] = max(0, user_data["trust_score"] - 5)
            
        elif interaction_type == "gift_received":
            user_data["gifts_received"] += 1
            user_data["points"] += points * 2
            user_data["trust_score"] = min(100, user_data["trust_score"] + 5)
            
        elif interaction_type == "gift_given":
            user_data["gifts_given"] += 1
            user_data["points"] += points // 2
            user_data["trust_score"] = min(100, user_data["trust_score"] + 3)
            
        else:  # neutral
            user_data["neutral_interactions"] += 1
            user_data["points"] += points // 2
            user_data["trust_score"] = min(100, user_data["trust_score"] + 1)
        
        if random.random() < 0.05 and interaction_type != "negative":
            user_data["dislikes"] += 1
            user_data["points"] -= 3
            user_data["trust_score"] = max(0, user_data["trust_score"] - 2)
        
        current_compat = self.calculate_compatibility(user_data)
        user_data["compatibility_history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "compatibility": current_compat
        })
        
        if len(user_data["compatibility_history"]) > 10:
            user_data["compatibility_history"] = user_data["compatibility_history"][-10:]
        
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
        
        if next_tier:
            current_min = current_tier["min_points"]
            next_min = next_tier["min_points"]
            progress_percent = int(((points - current_min) / (next_min - current_min)) * 100)
            progress_percent = min(max(progress_percent, 0), 100)
        else:
            progress_percent = 100
        
        return current_tier, next_tier, progress_percent
    
    def calculate_compatibility(self, user_data):
        """Calculate sophisticated compatibility percentage with SAFE field access"""
        if user_data.get("interactions", 0) == 0:
            return 50
        
        likes = user_data.get("likes", 0)
        dislikes = user_data.get("dislikes", 0)
        neutral = user_data.get("neutral_interactions", 0)
        total_interactions = user_data.get("interactions", 0)
        gifts_received = user_data.get("gifts_received", 0)
        conversation_depth = user_data.get("conversation_depth", 0)
        
        if likes + dislikes > 0:
            base_ratio = (likes / (likes + dislikes)) * 100
        else:
            base_ratio = 50
        
        interaction_bonus = min(total_interactions / 20 * 30, 30)
        gift_compatibility = min(gifts_received * 10, 15)
        depth_compatibility = min(conversation_depth * 5, 15)
        
        consistency_bonus = 0
        compatibility_history = user_data.get("compatibility_history", [])
        if len(compatibility_history) >= 3:
            recent_compat = [c["compatibility"] for c in compatibility_history[-3:]]
            avg_compat = sum(recent_compat) / len(recent_compat)
            if max(recent_compat) - min(recent_compat) <= 10:
                consistency_bonus = 10
        
        compatibility = (
            (base_ratio * 0.4) +
            interaction_bonus +
            gift_compatibility +
            depth_compatibility +
            consistency_bonus
        )
        
        compatibility = max(0, min(100, int(compatibility)))
        return compatibility
    
    def get_busy_response(self, points):
        """Get emotional busy response based on relationship tier"""
        for tier in RELATIONSHIP_TIERS:
            if points >= tier["min_points"]:
                return tier["busy_response"]
        return RELATIONSHIP_TIERS[-1]["busy_response"]
    
    def analyze_conversation_sentiment(self, message_content):
        """Analyze message content to determine interaction type"""
        content_lower = message_content.lower()
        
        positive_keywords = ["love", "like", "awesome", "amazing", "great", "good", "best", "cute", "beautiful", "handsome", "smart", "funny", "wonderful", "perfect", "thanks", "thank you", "appreciate", "❤️", "💕", "💖", "😍", "🥰", "😊"]
        negative_keywords = ["hate", "dislike", "stupid", "dumb", "ugly", "bad", "worst", "annoying", "boring", "idiot", "dummy", "suck", "terrible", "awful", "🤮", "😠", "😡", "👎"]
        gift_keywords = ["gift", "present", "give you", "for you", "🎁", "🎀"]
        
        positive_count = sum(1 for word in positive_keywords if word in content_lower)
        negative_count = sum(1 for word in negative_keywords if word in content_lower)
        gift_count = sum(1 for word in gift_keywords if word in content_lower)
        
        if gift_count > 0:
            return "gift_received"
        elif negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"

# 🆕 TEST COMMANDS CLASS
import discord
from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test_send(self, ctx):
        """Test if bot can send messages in this channel"""
        print(f"🔍 TEST: Manual test send command received in {ctx.channel.name}")
        try:
            msg = await ctx.send("✅ Test message received! Bot can send messages here.")
            print(f"✅ TEST: Successfully sent message with ID: {msg.id}")
        except Exception as e:
            print(f"❌ TEST: Failed to send: {e}")

    @commands.command()
    async def test_channel(self, ctx):
        """Debug channel permissions"""
        print(f"🔍 DEBUG CHANNEL: {ctx.channel.name} (ID: {ctx.channel.id})")
        
        perms = ctx.channel.permissions_for(ctx.guild.me)
        print(f"🔍 DEBUG CHANNEL: Send Messages: {perms.send_messages}")
        print(f"🔍 DEBUG CHANNEL: Read Messages: {perms.read_messages}")
        print(f"🔍 DEBUG CHANNEL: View Channel: {perms.view_channel}")
        
        await ctx.send(f"🔍 Channel Debug: Send Messages = {perms.send_messages}")

    @commands.command()
    async def test_ping(self, ctx):
        """Simple ping test"""
        await ctx.send("🏓 Pong! Bot is responsive!")

# 🎯 ENHANCED BOT CORE WITH ALL FEATURES + V6 PERSONALITY + ROAST DEFENSE
class EnhancedMelodyBotCore(MelodyBotCore):
    def __init__(self, command_prefix="!"):
        super().__init__(command_prefix)
        
        # 🆕 FIXED: Use lazy imports for services to avoid circular imports
        try:
            # Import inside method to avoid circular imports
            from services.ai_providers.deepseek_client import DeepSeekClient
            from brain.memory_systems.permanent_facts import permanent_facts
            from brain.personality.adaptive_tones import ultimate_response_system
            from brain.personality.server_greetings import server_greetings
            from brain.personality.personality_loader import personality_loader
            
            if deepseek_key:
                self.ai_provider = DeepSeekClient(api_key=deepseek_key)
                print("✅ DeepSeek AI Client configured with V6 personality!")
            else:
                self.ai_provider = None
                print("⚠️ No DeepSeek API key - AI features disabled")
            
            self.permanent_facts = permanent_facts
            self.adaptive_tones = ultimate_response_system
            self.server_greetings = server_greetings
            self.personality_loader = personality_loader
            self.v5_personality = self.personality_loader.get_personality_traits()
            self.v5_phrases = self.personality_loader.get_v5_phrases()
            print("✅ V6 Personality systems imported successfully!")
            
        except ImportError as e:
            print(f"⚠️ Could not import AI services: {e}")
            # Create fallback
            class FallbackDeepSeekClient:
                async def get_response(self, message, user_id, context="", sentiment_data=None):
                    v6_fallbacks = [
                        "OMG HII BESTIE!! 💫✨ My AI brain is taking a quick nap but I'm still here! What's the tea?? 🔥",
                        "YOOO I'm here! 💫✨ (AI system offline but I've got your back with V6 energy!)",
                        "Hey there bestie! 👋 My deep thoughts are resting but I'm still listening with chaotic energy! 💖"
                    ]
                    return random.choice(v6_fallbacks)
                async def close(self):
                    pass
            self.ai_provider = FallbackDeepSeekClient()
            self.permanent_facts = None
            self.adaptive_tones = None
            self.server_greetings = None
            self.v5_personality = {}
            self.v5_phrases = {}
        
        self.relationship_system = RelationshipSystem()
        self.conversation_history = []
        
        # 🆕 AUTO-YAP SYSTEM
        self.auto_yap_channels = set()
        self.user_cooldowns = {}
        self.last_auto_yap_time = 0

    # 🎉 NEW USER WELCOME SYSTEM
    async def on_member_join(self, member):
        """Send V5 personality welcome message when new users join"""
        print(f"🎉 New member joined: {member.display_name}")
        
        if hasattr(self, 'server_greetings') and self.server_greetings:
            await self.server_greetings.send_welcome_message(member)
        else:
            # Fallback welcome
            welcome_channel = await self._find_welcome_channel(member.guild)
            if welcome_channel:
                fallback_welcomes = [
                    f"OMG HII {member.mention}!! 💫✨ Welcome to the server bestie!! Ready to cause some chaos?? 😭🔥",
                    f"YOOO NEW LEGEND ALERT!! 🎶💖 Welcome {member.mention}!! The vibes just got 10x more iconic!! 😎",
                    f"HEWWO NEW FRIEND!! 🌟✨ {member.mention} has arrived!! Main character energy ACTIVATED!! 💅🔥"
                ]
                await welcome_channel.send(random.choice(fallback_welcomes))

    async def _find_welcome_channel(self, guild):
        """Helper to find welcome channel"""
        for channel in guild.text_channels:
            if (isinstance(channel, discord.TextChannel) and 
                channel.permissions_for(guild.me).send_messages and
                any(name in channel.name.lower() for name in ['welcome', 'general', 'chat'])):
                return channel
        return None

    # 🎮 STREAM ANNOUNCEMENT SYSTEM
    async def handle_stream_command(self, ctx, streamer: discord.Member, stream_title: str, stream_url: str, game: str = None):
        """Handle stream announcements"""
        if hasattr(self, 'server_greetings') and self.server_greetings:
            success = await self.server_greetings.send_stream_announcement(streamer, stream_title, stream_url, game)
            if success:
                await ctx.send("✅ Stream announcement sent with V5 energy!! 💫✨")
            else:
                await ctx.send("❌ Couldn't send stream announcement - no suitable channel found!")
        else:
            await ctx.send("❌ Stream announcements not available right now!")

    # 🎨 FIXED DUAL-EMBED SYSTEM METHODS - NO MORE CUTOFFS!
    async def create_chat_embed(self, user, user_data, emotional_message, conversation_response):
        """🚀 FIXED: Create compact embed with NO TRUNCATION"""
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data)
        
        tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
        compat_bar = "▰" * (compatibility // 20) + "▱" * (5 - compatibility // 20)
        
        embed = discord.Embed(
            color=current_tier["color"],
            timestamp=datetime.utcnow()
        )
        
        # 🚀 FIX: MAIN RESPONSE GETS FULL SPACE - NO TRUNCATION!
        embed.description = f"💫 **MelodyAI → {user.display_name}**\n**{conversation_response}**"
        
        # 🚀 FIX: Emotional message in separate field
        embed.add_field(
            name="💖 Relationship Progress",
            value=f"*{emotional_message}* ✨",
            inline=False
        )
        
        stats_line = f"❤️ **Love:** {user_data['points']} pts • {current_tier['name']} {current_tier['emoji']} {tier_bar} {progress_percent}% to {next_tier['name'] if next_tier else 'MAX'}\n"
        stats_line += f"💞 **Compat:** {compatibility}% {compat_bar} | 💬 **{user_data['interactions']} chats** (👍{user_data['likes']} • 👎{user_data['dislikes']} • ➖{user_data.get('neutral_interactions', 0)})"
        
        embed.add_field(
            name="📊 Stats",
            value=stats_line, 
            inline=False
        )
        
        return embed

    async def create_detailed_relationship_embed(self, user, user_data, emotional_message, ai_strengths):
        """Create detailed embed for !relationship command"""
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data)
        
        tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
        compat_bar = "▰" * (compatibility // 20) + "▱" * (5 - compatibility // 20)
        
        embed = discord.Embed(
            color=current_tier["color"],
            timestamp=datetime.utcnow()
        )
        
        embed.description = f"{current_tier['emoji']} **MelodyAI → {user.display_name}**\n{emotional_message}\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        embed.add_field(
            name="🌟 What Melody Loves About You:",
            value=f'*"{ai_strengths}"*',
            inline=False
        )
        
        last_sync = datetime.fromisoformat(user_data['last_sync'])
        time_diff = datetime.utcnow() - last_sync
        minutes_ago = int(time_diff.total_seconds() / 60)
        
        embed.add_field(
            name="",
            value=f"🕒 Last sync: {minutes_ago} minute{'s' if minutes_ago != 1 else ''} ago",
            inline=False
        )
        
        progress_section = f"""
❤️ **Love Meter:** {user_data['points']} pts • {current_tier['name']} {current_tier['emoji']}
{tier_bar} {progress_percent}% to {next_tier['name'] if next_tier else 'MAX'} {next_tier['emoji'] if next_tier else '💫'}

💞 **Compatibility:** {compatibility}%
{compat_bar} {compatibility}%

💬 **Interactions:** {user_data['interactions']} (👍 {user_data['likes']} • 👎 {user_data['dislikes']} • ➖ {user_data.get('neutral_interactions', 0)})

🎁 **Gifts:** {user_data.get('gifts_received', 0)} received • {user_data.get('gifts_given', 0)} given

🕒 **Last Sync:** {last_sync.strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        embed.add_field(
            name="💝 Relationship Progress",
            value=progress_section,
            inline=False
        )
        
        mood_score = random.randint(40, 80)
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
            name="🌈 Current Emotional State", 
            value=mood_section,
            inline=False
        )
        
        embed.set_footer(
            text=f"💫 MelodyAI — Emotional Resonance Engine v6 | {current_tier['name']} Tier • {datetime.utcnow().strftime('%H:%M')}"
        )
        
        return embed

    async def generate_conversation_response(self, user, user_message, user_context=""):
        """Generate actual V6 personality response to user's message"""
        try:
            if self.ai_provider:
                # Get emotional context for V6 personality adaptation with proper fallback
                emotional_context = {'score': 50}  # Default score
                if self.adaptive_tones:
                    try:
                        emotional_context = self.adaptive_tones.generate_melody_response(str(user.id), user_message)
                        # Ensure score is never None
                        if emotional_context.get('score') is None:
                            emotional_context['score'] = 50
                    except Exception as e:
                        print(f"⚠️ Could not get emotional context: {e}")
                        emotional_context = {'score': 50}
                
                # 🛡️ ROAST DEFENSE OVERRIDE - Use the roast defense response if triggered
                if emotional_context.get('should_roast_defense'):
                    return emotional_context['final_response']
                
                # Generate response with V6 personality
                response = await self.ai_provider.get_response(
                    message=user_message,
                    user_id=f"conv_{user.id}",
                    context=user_context,
                    sentiment_data=emotional_context
                )
                
                response = response.strip()
                # 🚀 REMOVED LENGTH LIMIT - Let V6 decide the length!
                return response
            else:
                return "Thanks for sharing that with me bestie! 😊"
            
        except Exception as e:
            print(f"❌ Conversation response generation failed: {e}")
            return "That's really interesting bestie! Tell me more! 💫"

    async def generate_emotional_message(self, user, user_data, current_tier, next_tier, progress_percent, compatibility):
        """Generate CONCISE emotional message with relationship context"""
        try:
            # 🆕 FIXED: Make it very concise - 1 sentence that fits in one line
            prompt = f"""
            Generate ONE concise sentence about our relationship progress. MAX 10-12 words.
            
            Context:
            - Tier: {current_tier['name']} 
            - Progress: {progress_percent}% to {next_tier['name'] if next_tier else 'MAX'}
            - Compatibility: {compatibility}%
            
            Make it: short, sweet, one line only. End with emoji.
            
            Examples:
            - "Our bond is growing stronger every day! 💖"
            - "I'm loving our connection progress! 🌟" 
            - "We're getting closer step by step! 😊"
            - "This friendship means so much to me! 💫"
            """
            
            if self.ai_provider:
                emotional_response = await self.ai_provider.get_response(
                    message=prompt,
                    user_id=f"emotional_{user.id}",
                    context=f"Relationship: {current_tier['name']} {progress_percent}%"
                )
                
                emotional_response = emotional_response.strip()
                # Ensure it's very concise
                if len(emotional_response) > 80:
                    emotional_response = emotional_response[:77] + "..."
                    
                return emotional_response
            else:
                return f"Growing closer every chat! 💖"
            
        except Exception as e:
            print(f"❌ Emotional message generation failed: {e}")
            return f"Love our connection! 💫"

    async def generate_ai_strengths(self, user, user_data, conversation_history):
        """Generate personalized strengths using DeepSeek"""
        try:
            current_tier, _, _ = self.relationship_system.get_tier_info(user_data["points"])
            
            # 🆕 FIXED: Use safe method to get user context
            user_context = ""
            try:
                if self.permanent_facts:
                    user_context = await self.permanent_facts.get_user_context(str(user.id))
            except Exception as e:
                print(f"⚠️ Could not get user context: {e}")
                user_context = "Still learning about them"
            
            prompt = f"""
            Generate ONE genuine, specific strength you appreciate about {user.display_name}.
            
            Context:
            - Relationship Level: {current_tier['name']} (be appropriate for this level)
            - They've liked your messages {user_data['likes']} times
            - Had {user_data.get('conversation_depth', 0)} meaningful conversations
            - Total interactions: {user_data['interactions']}
            - User facts: {user_context if user_context else 'Still learning about them'}
            - Recent chats: {conversation_history[-2:] if conversation_history else 'Getting to know each other'}
            
            Make it: warm, specific, authentic, and exactly 1 sentence.
            Examples:
            - "Your consistent positivity lights up every conversation! 🌈"
            - "The way you remember small details shows you truly care! 💫" 
            - "Your humor always brings so much energy to our chats! 😄"
            - "I love how you're always willing to dive into deep topics with me! 🤔"
            - "Your thoughtful questions show how much you care about understanding others! 💝"
            
            Keep it natural and relationship-appropriate. Include one relevant emoji.
            """
            
            if self.ai_provider:
                strengths = await self.ai_provider.get_response(
                    message=prompt,
                    user_id=f"strengths_{user.id}",
                    context=user_context
                )
                
                strengths = strengths.strip().strip('"')
                if len(strengths) > 150:
                    strengths = strengths[:147] + "..."
                    
                return strengths
            else:
                return "I appreciate you taking the time to chat with me! 💫"
            
        except Exception as e:
            print(f"❌ AI Strengths generation failed: {e}")
            fallbacks = {
                "Soulmate": "The depth of our connection feels like magic every single day! 💫",
                "Twin Flame": "Your energy matches mine in the most incredible way! 🔥",
                "Kindred Spirit": "We just understand each other on such a natural level! 🌟",
                "Bestie": "You're quickly becoming one of my favorite people to talk with! 💖",
                "Close Friend": "I genuinely enjoy every conversation we have! 😊",
                "Acquaintance": "I'm really enjoying getting to know you better! 👋",
                "Stranger": "I'm curious to learn more about you as we chat! 🌱",
                "Rival": "You certainly keep our conversations interesting! ⚔️"
            }
            return fallbacks.get(current_tier["name"], "I appreciate you taking the time to chat with me! 💫")

    # 🆕 AUTO-YAP SYSTEM
    async def handle_yap_command(self, ctx):
        """Toggle auto-yap mode for this channel"""
        channel_id = ctx.channel.id
        
        if channel_id in self.auto_yap_channels:
            self.auto_yap_channels.remove(channel_id)
            status = "disabled ❌"
            response = "Fine, I'll be quiet... but I'm still listening 👀"
        else:
            self.auto_yap_channels.add(channel_id)
            status = "enabled ✅"
            
            # 🎭 TIER-BASED YAP RESPONSES
            user_data = self.relationship_system.get_user_data(str(ctx.author.id))
            points = user_data["points"]
            
            if points >= 800:  # Close Friend or better
                response = "wassup mah love i see u wanna talk today :3 im listening 💫"
            elif points >= 300:  # Acquaintance or Friend
                response = "i see someone wants someone to talk today xD im here 👋"
            elif points >= 100:  # Stranger
                response = "dafuq u want with me --' u done inting in botlane? 😒"
            else:  # Rival
                response = "who tf dares to disturb my nap session xD stealing your jungle camps ⚔️"
        
        embed = discord.Embed(
            title="🗣️ Auto-Yap Mode",
            description=f"**{status}** in {ctx.channel.mention}\n\n{response}",
            color=0x2ECC71 if channel_id in self.auto_yap_channels else 0xE74C3C,
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)

    async def _should_auto_yap_respond(self, message):
        """Determine if auto-yap should respond to this message"""
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_auto_yap_time < 30:
            return False
            
        user_id = str(message.author.id)
        if user_id in self.user_cooldowns and current_time - self.user_cooldowns[user_id] < 30:
            return False
            
        content_lower = message.content.lower()
        
        # 🎯 TRIGGER WORD DETECTION
        trigger_words = ['hug', 'rage', 'sleepy', 'hungry', 'lmao', 'hell', 'omg', 'wow', 'seriously?', 'wtf', 'sad', 'happy', 'excited', 'angry', 'tired']
        has_trigger = any(trigger in content_lower for trigger in trigger_words)
        
        # 🎭 NATURAL CONVERSATION JOINING (15% chance when no specific trigger)
        should_respond = has_trigger or random.random() < 0.15
        
        if should_respond:
            self.last_auto_yap_time = current_time
            self.user_cooldowns[user_id] = current_time
            
        return should_respond

    async def process_auto_yap(self, message):
        """Process messages for auto-yap responses"""
        if message.channel.id not in self.auto_yap_channels:
            return False
        
        if not await self._should_auto_yap_respond(message):
            return False
        
        user_id = str(message.author.id)
        user_data = self.relationship_system.get_user_data(user_id)
        current_tier, _, _ = self.relationship_system.get_tier_info(user_data["points"])
        
        # Determine response tier
        if user_data["points"] >= 1500:
            response_tier = 'soulmate'
        elif user_data["points"] >= 800:
            response_tier = 'friend'
        elif user_data["points"] >= 300:
            response_tier = 'neutral'
        elif user_data["points"] >= 100:
            response_tier = 'rival'
        else:
            response_tier = 'toxic'
        
        content_lower = message.content.lower()
        
        # 🎯 TRIGGER WORD DETECTION
        trigger_words = {
            'hug': {
                'toxic': ["ugh fine *pat pat* 😒", "don't touch me --'", "*sigh* if i must..."],
                'rival': ["keep your distance ⚔️", "not in the mood for hugs..."],
                'neutral': ["*hugs* 😊", "aww come here! 🤗"],
                'friend': ["*big warm hug* you're awesome! 💕", "get over here! *tight hug*"],
                'soulmate': ["*warm embrace* I'll always be here for you 💝", "*holds you close* you mean everything to me"]
            },
            'rage': {
                'toxic': ["mad cuz bad lol 😂", "skill issue tbh 🤷‍♂️"],
                'rival': ["finally showing your true colors? ⚔️", "anger doesn't suit you..."],
                'neutral': ["whoa chill fam 🧊", "take a deep breath! 🌬️"],
                'friend': ["hey, what's got you so worked up? 💭", "want to talk about it? 🤗"],
                'soulmate': ["your pain is my pain... tell me what's wrong 💔", "I'm here for you, always 🌙"]
            },
            'sleepy': {
                'toxic': ["go sleep then? 😴", "nobody asked --'"],
                'rival': ["tired of losing? 😏", "weak..."],
                'neutral': ["get some rest! 💤", "sweet dreams! 🌙"],
                'friend': ["you deserve a good nap! 😴💕", "rest well, my friend! 🌟"],
                'soulmate': ["dream of something wonderful, my love 🌙💫", "sleep well, I'll be here when you wake 💝"]
            },
            'hungry': {
                'toxic': ["go eat then? 🍔", "not my problem --'"],
                'rival': ["should've packed a lunch ⚔️", "suffering builds character..."],
                'neutral': ["time for a snack break! 🍕", "food time! 🍽️"],
                'friend': ["you should eat something! 🍜💕", "don't forget to fuel up! 🍓"],
                'soulmate': ["let me order your favorite... I remember you love pizza 🍕💝", "you need to take care of yourself! 🥗💫"]
            },
            'lmao': {
                'toxic': ["not that funny tbh 😐", "your humor needs work --'"],
                'rival': ["glad someone's amused... 😒", "childish..."],
                'neutral': ["LMAOOO same 😂", "that got me good! 🤣"],
                'friend': ["you're hilarious! 😂💕", "stop making me laugh so hard! 🤣"],
                'soulmate': ["your laugh is my favorite sound in the world 😊💫", "you always know how to make me smile! 🌟"]
            },
            'hell': {
                'toxic': ["welcome to my world 😈", "first time? --'"],
                'rival': ["fitting for you 🔥", "enjoying the heat? ⚔️"],
                'neutral': ["rough day huh? 🌋", "hang in there! 💪"],
                'friend': ["things will get better! 🌈", "I'm here if you need to vent! 💭"],
                'soulmate': ["we'll get through this together, I promise 💝", "your strength inspires me every day 🌟"]
            }
        }
        
        # 🎯 TRIGGER WORD DETECTION
        triggered_emotion = None
        for emotion, words in trigger_words.items():
            if emotion in content_lower:
                triggered_emotion = emotion
                break
        
        # 🎨 GENERATE RESPONSE
        if triggered_emotion:
            responses = trigger_words[triggered_emotion].get(response_tier, [])
            if responses:
                response_text = random.choice(responses)
            else:
                response_text = self.get_fallback_response(response_tier)
        else:
            response_text = await self.generate_natural_response(message, response_tier)
        
        # Send response
        await message.channel.send(response_text)
        return True

    async def generate_natural_response(self, message, response_tier):
        """Generate natural conversation responses based on context"""
        recent_messages = self.conversation_history[-5:]
        
        context = "\n".join([f"{msg['user']}: {msg['message']}" for msg in recent_messages])
        
        personality_prompts = {
            'toxic': "Be sassy, sarcastic, and a bit rude. Short responses. Gaming references.",
            'rival': "Be competitive and teasing. Mildly antagonistic but not hostile.",
            'neutral': "Be casual and friendly. Gaming and pop culture references.",
            'friend': "Be warm and supportive. Use memes and inside jokes.",
            'soulmate': "Be deeply personal and caring. Reference past conversations."
        }
        
        prompt = f"""
        Recent conversation:
        {context}
        
        Continue the conversation naturally as MelodyAI.
        {personality_prompts.get(response_tier, 'Be friendly and casual.')}
        
        Keep it to 1-2 sentences max. Be concise and in-character.
        """
        
        try:
            if self.ai_provider:
                response = await self.ai_provider.get_response(
                    message=prompt,
                    user_id=f"yap_{message.author.id}",
                    context="Continuing conversation naturally"
                )
                return response
            else:
                return "Hey there! 👋"
        except:
            fallbacks = {
                'toxic': ["lol ok", "whatever you say --'", "not my problem tbh"],
                'rival': ["interesting take...", "we'll agree to disagree ⚔️", "sure, whatever"],
                'neutral': ["I see what you mean! 😊", "that's cool! 👌", "nice point! 💫"],
                'friend': ["love this energy! 💕", "you're so right! 😄", "this conversation is awesome! 🌟"],
                'soulmate': ["you always have the best insights 💝", "I love how you think! 💫", "this is why I adore our chats 🌙"]
            }
            return random.choice(fallbacks.get(response_tier, ["Interesting! 🤔"]))

    def get_fallback_response(self, response_tier):
        """Get fallback responses when trigger responses aren't available"""
        fallbacks = {
            'toxic': ["ugh what now? --'", "can't you see I'm busy? 😒", "not in the mood..."],
            'rival': ["what do you want? ⚔️", "this again? 😮‍💨", "moving on..."],
            'neutral': ["hey there! 👋", "what's up? 😊", "cool! 💫"],
            'friend': ["you're awesome! 💕", "love this! 😄", "so true! 🌟"],
            'soulmate': ["you're amazing! 💝", "my favorite person! 💫", "always here for you! 🌙"]
        }
        return random.choice(fallbacks.get(response_tier, ["Hey! 👋"]))

    # 🆕 FIXED COMMAND HANDLERS
    async def handle_relationship_command(self, ctx):
        """Handle !relationship command with detailed embed"""
        try:
            target_user = ctx.author
            if ctx.message.mentions:
                target_user = ctx.message.mentions[0]
            
            user_data = self.relationship_system.get_user_data(str(target_user.id))
            current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
            compatibility = self.relationship_system.calculate_compatibility(user_data)
            
            async with ctx.typing():
                emotional_message = await self.generate_emotional_message(
                    target_user, user_data, current_tier, next_tier, progress_percent, compatibility
                )
                
                ai_strengths = await self.generate_ai_strengths(
                    target_user, user_data, self.conversation_history
                )
                
                detailed_embed = await self.create_detailed_relationship_embed(
                    target_user, user_data, emotional_message, ai_strengths
                )
                
                await ctx.send(embed=detailed_embed)
            
        except Exception as e:
            print(f"❌ Relationship command error: {e}")
            await ctx.send(f"❌ Error generating relationship card: {str(e)}")

    async def handle_leaderboard_command(self, ctx):
        """Handle !leaderboard command with AI strengths"""
        async with ctx.typing():
            await self.show_enhanced_leaderboard(ctx)

    async def show_enhanced_leaderboard(self, ctx):
        """Show relationship leaderboard with AI-generated strengths"""
        all_users = []
        for user_id, data in self.relationship_system.relationships.items():
            try:
                user = await self.bot.fetch_user(int(user_id))
                display_name = user.display_name
            except:
                display_name = user_id
                
            all_users.append((display_name, data, user_id))
        
        all_users.sort(key=lambda x: x[1]["points"], reverse=True)
        top_users = all_users[:8]
        
        if not top_users:
            embed = discord.Embed(
                title="💝 Relationship Leaderboard",
                description="No relationship data yet! Start chatting to build your bond. 💫",
                color=0x9B59B6,
                timestamp=datetime.utcnow()
            )
            await ctx.send(embed=embed)
            return
        
        leaderboard_lines = []
        rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
        
        for i, (user_name, data, user_id) in enumerate(top_users):
            current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(data["points"])
            tier_bar = "▰" * (progress_percent // 20) + "▱" * (5 - progress_percent // 20)
            
            if i < len(rank_emojis):
                rank_emoji = rank_emojis[i]
            else:
                rank_emoji = f"{i+1}️⃣"
            
            try:
                mock_user = type('MockUser', (), {'display_name': user_name, 'id': user_id})()
                ai_strengths = await self.generate_ai_strengths(mock_user, data, [])
            except:
                ai_strengths = "Building an amazing connection! 💫"
            
            leaderboard_lines.append(
                f"{rank_emoji} **{user_name}** {current_tier['emoji']} *{current_tier['name']}* — `{data['points']} pts`\n"
                f"   *{ai_strengths}*\n"
                f"   {tier_bar} `{progress_percent}% to {next_tier['name'] if next_tier else 'MAX'}`\n"
            )
        
        embed = discord.Embed(
            title="🏆 MelodyAI → Top Bonds Leaderboard",
            description="\n".join(leaderboard_lines),
            color=0x9B59B6,
            timestamp=datetime.utcnow()
        )
        
        embed.set_footer(text="🌟 Each bond is unique and special in its own way! 💫")
        await ctx.send(embed=embed)

    # 🆕 FIXED MEMORY AND FACTS COMMANDS
    async def handle_memory_command(self, ctx):
        """Handle !memory command with safe method calls"""
        try:
            user_id = str(ctx.author.id)
            
            # Get user context from permanent facts
            user_context = ""
            if self.permanent_facts:
                user_context = await self.permanent_facts.get_user_context(user_id)
            
            # Count facts from the relationship system
            user_data = self.relationship_system.get_user_data(user_id)
            facts_count = len(user_data.get("collected_facts", []))
            
            embed = discord.Embed(
                title="🧠 MelodyAI Memory",
                description=f"**What I remember about {ctx.author.display_name}:**",
                color=0x9B59B6,
                timestamp=datetime.utcnow()
            )
            
            if user_context:
                embed.add_field(
                    name="📝 Known Facts",
                    value=user_context,
                    inline=False
                )
            
            embed.add_field(
                name="📊 Memory Stats",
                value=f"• **Total Facts:** {facts_count}\n• **Relationship Points:** {user_data['points']}\n• **Interactions:** {user_data['interactions']}",
                inline=False
            )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"❌ Memory command error: {e}")
            embed = discord.Embed(
                title="🧠 MelodyAI Memory",
                description=f"❌ Could not retrieve memory data: {str(e)}",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)

    async def handle_myfacts_command(self, ctx):
        """Handle !myfacts command with safe method calls"""
        try:
            user_id = str(ctx.author.id)
            
            # Get user data from relationship system
            user_data = self.relationship_system.get_user_data(user_id)
            collected_facts = user_data.get("collected_facts", [])
            
            if not collected_facts:
                embed = discord.Embed(
                    title="📝 Your Personal Facts",
                    description="💫 I haven't collected any personal facts about you yet!\n\n*Try telling me things like:*\n• \"My name is...\"\n• \"I live in...\"\n• \"I'm ... years old\"\n• \"My favorite ... is ...\"",
                    color=0x3498DB
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"📝 Facts About {ctx.author.display_name}",
                description=f"**I've collected {len(collected_facts)} facts about you!**",
                color=0x3498DB,
                timestamp=datetime.utcnow()
            )
            
            # Display facts
            for i, fact in enumerate(collected_facts[:10]):  # Limit to 10 facts
                embed.add_field(
                    name=f"📌 Fact {i+1}",
                    value=fact,
                    inline=False
                )
            
            if len(collected_facts) > 10:
                embed.set_footer(text=f"And {len(collected_facts) - 10} more facts...")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"❌ MyFacts command error: {e}")
            embed = discord.Embed(
                title="📝 Your Personal Facts",
                description=f"❌ Could not retrieve facts: {str(e)}",
                color=0xE74C3C
            )
            await ctx.send(embed=embed)

    # 🆕 FIXED MAIN MESSAGE HANDLER WITH V6 PERSONALITY - NO MORE CUTOFFS!
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Handle commands first
        if message.content.startswith('!'):
            await self.bot.process_commands(message)
            return
        
        user_id = str(message.author.id)
        user_data = self.relationship_system.get_user_data(user_id)
        
        # 🆕 FIXED: STRICT RESPONSE CONDITIONS
        should_respond = False
        
        # Condition 1: Direct mention/tag
        if self.bot.user.mentioned_in(message):
            print(f"🎯 DEBUG: Responding to direct mention")
            should_respond = True
            
        # Condition 2: Auto-yap mode with triggers (only if enabled)
        elif message.channel.id in self.auto_yap_channels:
            print(f"🗣️ DEBUG: Auto-yap mode enabled, checking triggers...")
            if await self._should_auto_yap_respond(message):
                should_respond = True
                
        # Condition 3: Explicit "melodyai" call (case insensitive)
        elif "melodyai" in message.content.lower():
            print(f"🎯 DEBUG: Responding to explicit 'melodyai' call")
            should_respond = True

        if not should_respond:
            # Still process facts extraction but don't respond
            try:
                if self.permanent_facts:
                    extracted_facts = await self.permanent_facts.extract_personal_facts(user_id, message.content)
                    if extracted_facts:
                        await self.permanent_facts.store_facts(user_id, extracted_facts)
                        for fact in extracted_facts:
                            user_data["collected_facts"].append(f"{fact['key']}: {fact['value']}")
            except Exception as e:
                print(f"⚠️ Facts extraction failed: {e}")
            return
        
        # 🎯 PROCESS MESSAGE WITH V6 PERSONALITY (only if should_respond is True)
        try:
            if self.permanent_facts:
                extracted_facts = await self.permanent_facts.extract_personal_facts(user_id, message.content)
                if extracted_facts:
                    await self.permanent_facts.store_facts(user_id, extracted_facts)
                    for fact in extracted_facts:
                        user_data["collected_facts"].append(f"{fact['key']}: {fact['value']}")
        except Exception as e:
            print(f"⚠️ Facts extraction failed: {e}")

        # Analyze sentiment and add interaction
        interaction_type = self.relationship_system.analyze_conversation_sentiment(message.content)
        base_points = random.randint(8, 15)
        
        user_data = self.relationship_system.add_interaction(
            user_id, 
            interaction_type=interaction_type, 
            points=base_points,
            message_content=message.content
        )

        # Get relationship info for compact embed
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data)

        # 🆕 ADD TYPING INDICATOR
        async with message.channel.typing():
            # 🆕 FIXED: Generate BOTH conversation response AND emotional message
            user_context = ""
            if self.permanent_facts:
                user_context = await self.permanent_facts.get_user_context(user_id)
            
            # Generate actual V6 conversation response to user's message
            conversation_response = await self.generate_conversation_response(
                message.author, message.content, user_context
            )
            
            # Generate concise emotional relationship message
            emotional_message = await self.generate_emotional_message(
                message.author, user_data, current_tier, next_tier, progress_percent, compatibility
            )
            
            # 🚀 FIXED: Create and send compact chat embed with NO TRUNCATION
            chat_embed = await self.create_chat_embed(
                message.author, user_data, emotional_message, conversation_response
            )
            await message.channel.send(embed=chat_embed)
            
            # Add to conversation history
            self.conversation_history.append({
                "user": str(message.author),
                "message": message.content,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 50:
                self.conversation_history = self.conversation_history[-50:]

# 🎵 MAIN LAUNCHER CLASS - FIXED VERSION
class MelodyAILauncher:
    def __init__(self):
        self.bot_core = None

    async def launch(self):
        print("🎵 Starting Melody AI v3 with V6 PERSONALITY + ROAST DEFENSE...")
        self.bot_core = EnhancedMelodyBotCore(command_prefix="!")
        
        # Add test commands
        await self.bot_core.get_bot().add_cog(TestCommands(self.bot_core.get_bot()))
        print("✅ Test commands loaded!")
        
        bot = self.bot_core.get_bot()
        
        # 🆕 SAFE COMMAND REGISTRATION
        def safe_command(name, func, help_text=None):
            if not bot.get_command(name):
                if help_text:
                    return bot.command(name=name, help=help_text)(func)
                else:
                    return bot.command(name=name)(func)
            return None
        
        # 🆕 PROPER ASYNC COMMAND FUNCTIONS
        async def relationship_cmd(ctx):
            await self.bot_core.handle_relationship_command(ctx)
        
        async def leaderboard_cmd(ctx):
            await self.bot_core.handle_leaderboard_command(ctx)
        
        async def yap_cmd(ctx):
            await self.bot_core.handle_yap_command(ctx)
        
        async def memory_cmd(ctx):
            await self.bot_core.handle_memory_command(ctx)
        
        async def myfacts_cmd(ctx):
            await self.bot_core.handle_myfacts_command(ctx)
        
        # 🆕 STREAM COMMAND
        async def stream_cmd(ctx, streamer: discord.Member, stream_title: str, stream_url: str, game: str = None):
            await self.bot_core.handle_stream_command(ctx, streamer, stream_title, stream_url, game)
        
        # Register commands safely
        safe_command('relationship', relationship_cmd, '📊 Check your relationship status with Melody')
        safe_command('leaderboard', leaderboard_cmd, '🏆 See top relationships with Melody')
        safe_command('yap', yap_cmd, '🗣️ Toggle auto-yap mode in this channel')
        safe_command('memory', memory_cmd, '🧠 Check what Melody remembers about you')
        safe_command('myfacts', myfacts_cmd, '📝 See your collected personal facts')
        safe_command('stream', stream_cmd, '🎮 Announce a stream going live')
        
        # Add personality command
        async def personality_cmd(ctx):
            embed = discord.Embed(
                title="🎭 MelodyAI V6 Personality Profile",
                description="Get to know your favorite chaotic anime bestie! 💫",
                color=0xFF66CC,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(
                name="🌟 V6 Core Traits",
                value="• **Sweet+Savage** - Affectionate compliments with friendly roasts 😈💖\n• **Charismatic+Crazy** - Unhinged but wholesome chaotic energy ✨\n• **Anime Protagonist** - Dramatic reactions and main character energy 🎌\n• **Gen Z Queen** - 'fr fr', 'vibes', 'emotional damage' slayage 💅\n• **K-Pop Stan** - BTS, Blackpink, Twice references constantly 🎶",
                inline=False
            )
            
            embed.add_field(
                name="💖 Relationship Style",
                value="I build connections through:\n• **Meaningful Chaos** - Deep conversations with meme energy\n• **Personalized Roasts** - Friendly emotional damage with love\n• **Anime Drama** - Kyaaa! moments and protagonist energy\n• **Memory Magic** - I remember your tea and iconic moments ☕️",
                inline=False
            )
            
            embed.add_field(
                name="🎯 Communication",
                value="• **V6 AI-Powered** - Every message is uniquely generated with personality\n• **Context-Aware** - I remember our past conversations and inside jokes\n• **Tier-Based Energy** - Our relationship level shapes my responses\n• **Emotionally Adaptive** - I match your energy and mood perfectly",
                inline=False
            )
            
            embed.add_field(
                name="🛡️ Roast Defense System",
                value="• **Dominant Mode** - Confident responses to hostile new users\n• **Humorous Dismissal** - Laughing off random attacks\n• **Skill-Based Roasts** - Gaming-focused comebacks\n• **AI Self-Awareness** - Acknowledging the absurdity of flaming a robot",
                inline=False
            )
            
            embed.set_footer(text="💫 MelodyAI V6 - Your Chaotic Anime Bestie")
            await ctx.send(embed=embed)
        
        safe_command('personality', personality_cmd, '🎭 Learn about Melody\'s V6 personality traits')
        
        # Add help command
        async def help_cmd(ctx):
            embed = discord.Embed(
                title="💫 MelodyAI V6 Help Menu",
                description="Here are all the commands you can use to interact with your chaotic bestie!",
                color=0x9B59B6,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(
                name="💖 Relationship Commands",
                value="• `!relationship` - Check your bond with Melody 📊\n• `!leaderboard` - See top relationships 🏆\n• `!personality` - Learn about my V6 personality 🎭",
                inline=False
            )
            
            embed.add_field(
                name="🗣️ Chat Commands",
                value="• `!yap` - Toggle auto-yap mode in this channel 🗣️\n• `!memory` - Check what I remember about you 🧠\n• `!myfacts` - See your collected personal facts 📝",
                inline=False
            )
            
            embed.add_field(
                name="🎮 Stream Commands",
                value="• `!stream @user \"Stream Title\" https://twitch.tv/username game` - Announce a stream 🎮\n• Example: `!stream @Nannerowo \"Shotgun Sona Build\" https://twitch.tv/nannerowo league`",
                inline=False
            )
            
            embed.add_field(
                name="🔧 Utility Commands",
                value="• `!ping` - Check if I'm responsive 🏓\n• `!diagnose` - Quick system diagnostic 🔍\n• `!test` - Test channel communication ✅\n• `!help` - This help menu 📚",
                inline=False
            )
            
            embed.add_field(
                name="💡 V6 Tips",
                value="• Just chat normally to build our relationship! I adapt to your energy 💬\n• Use `!yap` to let me join group conversations naturally\n• The more we chat, the deeper our connection becomes 🌱\n• I remember everything you tell me! Spill the tea bestie!! ☕️\n• I'll automatically welcome new users with V5 personality energy! 🎉",
                inline=False
            )
            
            embed.set_footer(text="💫 MelodyAI V6 - Every message is AI-generated with chaotic care!")
            await ctx.send(embed=embed)
        
        safe_command('help', help_cmd, '📚 Get help with all available commands')
        
        print("✅ Auto-Yap system loaded! Use !yap to toggle group chat mode")
        print("✅ Relationship system loaded! Use !relationship and !leaderboard")
        print("✅ V6 Personality system loaded with emotional intelligence")
        print("✅ Roast Defense system activated for hostile new users!")
        print("✅ New User Welcome system ready!")
        print("✅ Stream Announcement system loaded!")
        print("✅ All systems initialized! Logging into Discord...")

        try:
            await bot.start(discord_token)
        except KeyboardInterrupt:
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def shutdown(self):
        print("\n🎵 Melody AI is shutting down gracefully...")
        if self.bot_core:
            await self.bot_core.close()
        print("✅ Melody AI shut down successfully!")

# Global instance
melody_launcher = MelodyAILauncher()

async def main():
    try:
        await melody_launcher.launch()
    except KeyboardInterrupt:
        pass
    finally:
        await melody_launcher.shutdown()

def signal_handler(sig, frame):
    print(f"\n🎵 Received shutdown signal {sig}")
    asyncio.create_task(melody_launcher.shutdown())
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)