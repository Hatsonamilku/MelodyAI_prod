# main.py - ULTIMATE LAUNCHER WITH BUILT-IN WEB DASHBOARD
import asyncio
import os
import signal
import sys
import random
import json
import time
import threading
from datetime import datetime
from dotenv import load_dotenv

# 🎯 WEB DASHBOARD IMPORTS
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import re

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

# 🆕 SIMPLE ANALYTICS FOR WEB DASHBOARD
class Analytics:
    def __init__(self):
        self.message_count = 0
        self.web_messages = 0
        self.discord_messages = 0
        self.users = set()
        self.message_history = []
    
    def track_message(self, message_data):
        self.message_count += 1
        self.users.add(message_data.get('user', 'Unknown'))
        
        if message_data.get('source') == 'web':
            self.web_messages += 1
        else:
            self.discord_messages += 1
        
        self.message_history.append(message_data)
        if len(self.message_history) > 100:
            self.message_history = self.message_history[-100:]
    
    def get_analytics(self):
        return {
            'summary': {
                'total_messages': self.message_count,
                'unique_users': len(self.users),
                'web_messages': self.web_messages,
                'discord_messages': self.discord_messages
            },
            'message_stats': {
                'web_messages': self.web_messages,
                'discord_messages': self.discord_messages
            },
            'top_users': self._get_top_users()
        }
    
    def _get_top_users(self):
        user_counts = {}
        for msg in self.message_history:
            user = msg.get('user', 'Unknown')
            user_counts[user] = user_counts.get(user, 0) + 1
        
        return sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:5]

# 🆕 WEB DASHBOARD INTEGRATION
class WebPortal:
    def __init__(self, melody_bot):
        self.melody_bot = melody_bot
        self.connected_clients = 0
        self.message_history = []
        self.analytics = Analytics()
        
        # Flask app setup
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "melody_ultimate_launcher_2024"
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        @self.app.route("/api/status")
        def api_status():
            discord_connected = False
            if self.melody_bot and hasattr(self.melody_bot.bot, 'is_ready'):
                try:
                    discord_connected = self.melody_bot.bot.is_ready()
                except:
                    discord_connected = False
            
            return jsonify({
                "status": "online",
                "clients_connected": self.connected_clients,
                "discord_connected": discord_connected,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        @self.app.route("/api/servers")
        def api_servers():
            """Get list of servers Melody is in"""
            if self.melody_bot and self.melody_bot.bot.is_ready():
                servers = []
                for guild in self.melody_bot.bot.guilds:
                    servers.append({
                        'id': str(guild.id),
                        'name': guild.name,
                        'icon': str(guild.icon.url) if guild.icon else None,
                        'member_count': guild.member_count
                    })
                return jsonify(servers)
            return jsonify([])
        
        @self.app.route("/api/servers/<int:server_id>/channels")
        def api_server_channels(server_id):
            """Get text channels for a specific server"""
            if self.melody_bot and self.melody_bot.bot.is_ready():
                guild = self.melody_bot.bot.get_guild(server_id)
                if guild:
                    channels = []
                    for channel in guild.text_channels:
                        permissions = channel.permissions_for(guild.me)
                        if permissions.send_messages:
                            channels.append({
                                'id': str(channel.id),
                                'name': channel.name,
                                'topic': channel.topic or "",
                                'position': channel.position
                            })
                    channels.sort(key=lambda x: x['position'])
                    return jsonify(channels)
            return jsonify([])
        
        @self.app.route("/api/set_target_channel", methods=["POST"])
        def api_set_target_channel():
            """Change the target channel for messages"""
            data = request.json
            channel_id = data.get("channel_id")
            
            if channel_id and self.melody_bot:
                try:
                    self.melody_bot.web_target_channel_id = int(channel_id)
                    channel = self.melody_bot.bot.get_channel(int(channel_id))
                    channel_info = f"#{channel.name}" if channel else "Unknown Channel"
                    
                    self.socketio.emit("target_channel_changed", {
                        "channel_id": channel_id,
                        "channel_name": channel_info,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    
                    return jsonify({"status": "success", "channel_id": channel_id, "channel_name": channel_info})
                except Exception as e:
                    return jsonify({"error": str(e)}), 400
            
            return jsonify({"error": "Invalid channel ID"}), 400
        
        @self.app.route("/api/send_message", methods=["POST"])
        def api_send_message():
            data = request.json
            message = data.get("message", "").strip()
            user = data.get("user", "Hatsona Milku")
            
            if message:
                web_msg = {
                    "id": len(self.message_history) + 1,
                    "user": user,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "web",
                    "mysterious": True
                }
                self.message_history.append(web_msg)
                self.broadcast_message(web_msg)
                
                # Track analytics
                self.analytics.track_message(web_msg)
                
                print(f"🌩️ WEB MESSAGE: {user} says: {message}")
                
                # Send to Discord via the main bot
                if self.melody_bot:
                    asyncio.run_coroutine_threadsafe(
                        self.melody_bot.send_web_message_to_discord(web_msg),
                        self.melody_bot.bot.loop
                    )
                
                return jsonify({"status": "sent", "message_id": web_msg["id"]})
            
            return jsonify({"error": "No message"}), 400
        
        @self.app.route("/api/toggle_auto_yap", methods=["POST"])
        def api_toggle_auto_yap():
            """Toggle Auto-Yap mode from web"""
            data = request.json
            enable = data.get("enable", False)
            
            if self.melody_bot:
                try:
                    channel_id = self.melody_bot.web_target_channel_id
                    if enable:
                        self.melody_bot.auto_yap_channels.add(channel_id)
                        status = "enabled ✅"
                    else:
                        self.melody_bot.auto_yap_channels.discard(channel_id)
                        status = "disabled ❌"
                    
                    self.socketio.emit("auto_yap_status", {"enabled": enable, "status": status})
                    return jsonify({"status": "success", "auto_yap": enable})
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            
            return jsonify({"error": "Melody bot not ready"}), 400
        
        @self.app.route("/api/analytics")
        def api_analytics():
            """Get analytics data"""
            return jsonify(self.analytics.get_analytics())
        
        # SocketIO events
        @self.socketio.on("connect")
        def handle_connect():
            self.connected_clients += 1
            print(f"🌐 WEB CLIENT CONNECTED. Total: {self.connected_clients}")
            self.socketio.emit("message_history", self.message_history[-50:])
            self.socketio.emit("analytics_update", self.analytics.get_analytics())
        
        @self.socketio.on("disconnect")
        def handle_disconnect():
            self.connected_clients -= 1
            print(f"🌐 WEB CLIENT DISCONNECTED. Total: {self.connected_clients}")
    
    def broadcast_message(self, data):
        """Broadcast message to all web clients"""
        self.socketio.emit("new_message", data)
    
    def start_web_server(self):
        """Start the web server in a separate thread"""
        print("🌐 Starting Web Dashboard on http://localhost:5000")
        self.socketio.run(self.app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# 🆕 RELATIONSHIP SYSTEM CONFIGURATION
RELATIONSHIP_DATA_FILE = "relationship_data.json"
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
        default_data = {
            "points": 100, "likes": 0, "dislikes": 0, "neutral_interactions": 0,
            "gifts_received": 0, "gifts_given": 0, "conversation_depth": 0,
            "interactions": 0, "last_sync": datetime.utcnow().isoformat(),
            "compatibility_history": [], "trust_score": 50,
            "onboarding_complete": False, "collected_facts": []
        }
        for key, value in user_data.items():
            default_data[key] = value
        return default_data
    
    def save_relationships(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.relationships, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving relationship data: {e}")
    
    def get_user_data(self, user_id):
        if user_id not in self.relationships:
            self.relationships[user_id] = {
                "points": 100, "likes": 0, "dislikes": 0, "neutral_interactions": 0,
                "gifts_received": 0, "gifts_given": 0, "conversation_depth": 0,
                "interactions": 0, "last_sync": datetime.utcnow().isoformat(),
                "compatibility_history": [], "trust_score": 50,
                "onboarding_complete": False, "collected_facts": []
            }
        else:
            self.relationships[user_id] = self._migrate_user_data(self.relationships[user_id])
        return self.relationships[user_id]
    
    def add_interaction(self, user_id, interaction_type="neutral", points=10, message_content=""):
        user_data = self.get_user_data(user_id)
        user_data["interactions"] += 1
        user_data["last_sync"] = datetime.utcnow().isoformat()
        
        if interaction_type == "positive":
            user_data["likes"] += 1
            user_data["points"] += points
            user_data["trust_score"] = min(100, user_data["trust_score"] + 2)
        elif interaction_type == "negative":
            user_data["dislikes"] += 1
            user_data["points"] -= points // 2
            user_data["trust_score"] = max(0, user_data["trust_score"] - 5)
        else:
            user_data["neutral_interactions"] += 1
            user_data["points"] += points // 2
        
        self.save_relationships()
        return user_data
    
    def get_tier_info(self, points):
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
    
    def get_busy_response(self, points):
        for tier in RELATIONSHIP_TIERS:
            if points >= tier["min_points"]:
                return tier["busy_response"]
        return RELATIONSHIP_TIERS[-1]["busy_response"]
    
    def analyze_conversation_sentiment(self, message_content):
        content_lower = message_content.lower()
        positive_keywords = ["love", "like", "awesome", "amazing", "great", "good", "best", "cute", "beautiful"]
        negative_keywords = ["hate", "dislike", "stupid", "dumb", "ugly", "bad", "worst", "annoying"]
        
        positive_count = sum(1 for word in positive_keywords if word in content_lower)
        negative_count = sum(1 for word in negative_keywords if word in content_lower)
        
        if negative_count > positive_count:
            return "negative"
        elif positive_count > negative_count:
            return "positive"
        else:
            return "neutral"

# 🎯 ENHANCED BOT CORE WITH WEB DASHBOARD INTEGRATION
class EnhancedMelodyBotCore(MelodyBotCore):
    def __init__(self, command_prefix="!"):
        super().__init__(command_prefix)
        
        # 🆕 WEB DASHBOARD INTEGRATION
        self.web_target_channel_id = int(os.getenv('WEB_PORTAL_CHANNEL_ID', 1337024526923595786))
        self.web_portal = None
        
        # AI Services
        try:
            from services.ai_providers.deepseek_client import DeepSeekClient
            from brain.memory_systems.permanent_facts import permanent_facts
            if deepseek_key:
                self.ai_provider = DeepSeekClient(api_key=deepseek_key)
                print("✅ DeepSeek AI Client configured!")
            else:
                self.ai_provider = None
            
            self.permanent_facts = permanent_facts
            print("✅ Permanent Facts imported successfully!")
        except ImportError as e:
            print(f"⚠️ Could not import AI services: {e}")
            class FallbackDeepSeekClient:
                async def get_response(self, message, user_id, context=""):
                    fallbacks = [
                        "OMG HII BESTIE!! 💫✨ My AI brain is taking a quick nap but I'm still here!",
                        "YOOO I'm here! 💫✨ (AI system offline but I've got your back!)",
                        "Hey there! 👋 My deep thoughts are resting but I'm still listening! 💖"
                    ]
                    return random.choice(fallbacks)
                async def close(self): pass
            self.ai_provider = FallbackDeepSeekClient(api_key=deepseek_key)
            self.permanent_facts = None
        
        self.relationship_system = RelationshipSystem()
        self.conversation_history = []
        
        # AUTO-YAP SYSTEM
        self.auto_yap_channels = set()
        self.user_cooldowns = {}
        self.last_auto_yap_time = 0
        
        print("✅ Enhanced Melody Bot Core initialized with Web Dashboard support!")
    
    def setup_web_portal(self):
        """Setup the web portal for this bot instance"""
        self.web_portal = WebPortal(self)
        web_thread = threading.Thread(target=self.web_portal.start_web_server, daemon=True)
        web_thread.start()
        print("🌐 Web Dashboard integrated and starting...")
        return self.web_portal
    
    async def send_web_message_to_discord(self, message_data):
        """Send web portal messages to Discord with League troll names"""
        try:
            channel = self.bot.get_channel(self.web_target_channel_id)
            if channel:
                message_content = message_data['message']
                
                # Convert Discord user IDs to proper mentions
                user_id_pattern = r'@(\d{17,19})'
                message_content = re.sub(user_id_pattern, r'<@\1>', message_content)
                
                # LEAGUE OF LEGENDS TROLL NAMES
                league_troll_names = [
                    "😨 Fiddle Me Mommy says:", "🍺 Gragas the Rizzler says:",
                    "💅 Evelynn Your Mom says:", "🦀 Urgot My Up says:",
                    "🗡️ Yasuo Mad Bro says:", "🎻 Jhin and Tonic says:",
                    "🌙 Diana Ross says:", "🎯 Ashe Your Questions says:",
                    "⚡ Kennen You Handle This says:", "🎭 Shaco's Clone says:"
                ]
                
                selected_name = random.choice(league_troll_names)
                discord_message = f"**{selected_name}** {message_content}"
                
                await channel.send(
                    discord_message,
                    allowed_mentions=discord.AllowedMentions(users=True)
                )
                print(f"📤 WEB → DISCORD: {selected_name}: {message_content}")
                return True
        except Exception as e:
            print(f"❌ Failed to send web message to Discord: {e}")
        return False
    
    # 🎯 OVERRIDE MESSAGE HANDLER TO SUPPORT WEB DASHBOARD
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Handle commands first
        if message.content.startswith('!'):
            await self.bot.process_commands(message)
            return
        
        # 🆕 SEND DISCORD MESSAGES TO WEB DASHBOARD
        if self.web_portal and message.channel.id == self.web_target_channel_id:
            discord_msg = {
                'id': f"discord_{message.id}",
                'user': message.author.display_name,
                'message': message.content,
                'timestamp': message.created_at.isoformat(),
                'source': 'discord',
                'mysterious': False
            }
            self.web_portal.broadcast_message(discord_msg)
            self.web_portal.analytics.track_message(discord_msg)
            print(f"📥 DISCORD → WEB: {message.author.display_name}: {message.content}")
        
        # Process Auto-Yap
        yap_responded = await self.process_auto_yap(message)
        if yap_responded:
            return
        
        # Normal message processing (your existing code)
        user_id = str(message.author.id)
        user_data = self.relationship_system.get_user_data(user_id)
        
        # Extract facts
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

        # Generate responses and send embed (your existing code)
        current_tier, next_tier, progress_percent = self.relationship_system.get_tier_info(user_data["points"])
        compatibility = self.relationship_system.calculate_compatibility(user_data)

        user_context = ""
        if self.permanent_facts:
            user_context = await self.permanent_facts.get_user_context(user_id)
        
        conversation_response = await self.generate_conversation_response(
            message.author, message.content, user_context
        )
        
        emotional_message = await self.generate_emotional_message(
            message.author, user_data, current_tier, next_tier, progress_percent, compatibility
        )
        
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
        
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    # 🎯 YOUR EXISTING METHODS (keep all your current functionality)
    async def process_auto_yap(self, message):
        """Process messages for auto-yap responses"""
        if message.channel.id not in self.auto_yap_channels:
            return False
        
        current_time = time.time()
        if current_time - self.last_auto_yap_time < 30:
            return False
        
        user_id = str(message.author.id)
        if user_id in self.user_cooldowns:
            if current_time - self.user_cooldowns[user_id] < 30:
                return False
        
        # Your existing auto-yap logic here
        should_respond = random.random() < 0.25
        if not should_respond:
            return False
        
        user_data = self.relationship_system.get_user_data(user_id)
        response_text = await self.generate_natural_response(message, 'neutral')
        
        self.user_cooldowns[user_id] = current_time
        self.last_auto_yap_time = current_time
        
        await message.channel.send(response_text)
        return True
    
    async def generate_natural_response(self, message, response_tier):
        """Generate natural conversation responses"""
        try:
            if self.ai_provider:
                response = await self.ai_provider.get_response(
                    message=message.content,
                    user_id=f"yap_{message.author.id}",
                    context="Continuing conversation naturally"
                )
                return response
            else:
                return "Hey there! 👋"
        except:
            return "Interesting! 🤔"
    
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
            response = "Yapping mode activated! I'll join conversations naturally 🗣️"
        
        embed = discord.Embed(
            title="🗣️ Auto-Yap Mode",
            description=f"**{status}** in {ctx.channel.mention}\n\n{response}",
            color=0x2ECC71 if channel_id in self.auto_yap_channels else 0xE74C3C,
            timestamp=datetime.utcnow()
        )
        await ctx.send(embed=embed)
    
    # Include all your other existing methods:
    # create_chat_embed, generate_conversation_response, generate_emotional_message,
    # handle_relationship_command, handle_leaderboard_command, etc.
    # ... (Keep all your existing methods from the original main.py)

# 🎵 ULTIMATE LAUNCHER WITH WEB DASHBOARD
class UltimateMelodyLauncher:
    def __init__(self):
        self.bot_core = None
        self.web_portal = None

    async def launch(self):
        print("🎵 Starting ULTIMATE MELODY AI with Built-in Web Dashboard...")
        self.bot_core = EnhancedMelodyBotCore(command_prefix="!")
        
        # 🆕 SETUP WEB DASHBOARD
        self.web_portal = self.bot_core.setup_web_portal()
        
        # Add test commands
        from discord.ext import commands
        
        class TestCommands(commands.Cog):
            def __init__(self, bot):
                self.bot = bot

            @commands.command()
            async def test_send(self, ctx):
                await ctx.send("✅ Test message received! Bot can send messages here.")

            @commands.command()
            async def test_web(self, ctx):
                embed = discord.Embed(
                    title="🌐 Web Dashboard Status",
                    description=f"Web Dashboard: **{'✅ Online' if self.bot.web_portal else '❌ Offline'}**\nURL: http://localhost:5000",
                    color=0x9B59B6
                )
                await ctx.send(embed=embed)
        
        await self.bot_core.get_bot().add_cog(TestCommands(self.bot_core.get_bot()))
        
        # Register commands
        bot = self.bot_core.get_bot()
        
        @bot.command(name='yap')
        async def yap_cmd(ctx):
            await self.bot_core.handle_yap_command(ctx)
        
        @bot.command(name='webstatus')
        async def webstatus_cmd(ctx):
            embed = discord.Embed(
                title="🌐 Ultimate Melody Launcher",
                description="**All Systems Integrated!**\n\n• 🤖 AI Bot: ✅ Running\n• 🌐 Web Dashboard: ✅ Running\n• 🗣️ Auto-Yap: ✅ Available\n• 💖 Relationships: ✅ Active",
                color=0x00FF00
            )
            embed.add_field(
                name="Web Dashboard",
                value="Visit: http://localhost:5000\nControl Melody from your browser!",
                inline=False
            )
            embed.add_field(
                name="Features",
                value="• Send messages to Discord\n• Multi-server channel selection\n• Real-time chat bridge\n• Analytics dashboard\n• Auto-Yap control",
                inline=False
            )
            await ctx.send(embed=embed)
        
        print("✅ Ultimate Melody Launcher ready!")
        print("🌐 Web Dashboard: http://localhost:5000")
        print("🤖 Discord Bot: Logging in...")
        
        try:
            await bot.start(discord_token)
        except KeyboardInterrupt:
            return True
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            return False

    async def shutdown(self):
        print("\n🎵 Ultimate Melody AI shutting down gracefully...")
        if self.bot_core:
            await self.bot_core.close()
        print("✅ All systems shut down successfully!")

# Global instance
ultimate_launcher = UltimateMelodyLauncher()

async def main():
    try:
        await ultimate_launcher.launch()
    except KeyboardInterrupt:
        pass
    finally:
        await ultimate_launcher.shutdown()

def signal_handler(sig, frame):
    print(f"\n🎵 Received shutdown signal {sig}")
    asyncio.create_task(ultimate_launcher.shutdown())
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