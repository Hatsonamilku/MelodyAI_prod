# app.py - COMPLETE FIXED VERSION
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
from datetime import datetime
import asyncio
import threading
import random
from discord_bridge import setup_discord_bridge
from analytics import analytics

app = Flask(__name__)
app.config["SECRET_KEY"] = "melody_web_portal_secret_2024"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class WebPortal:
    def __init__(self):
        self.connected_clients = 0
        self.message_history = []
    
    def broadcast_message(self, data):
        socketio.emit("new_message", data)
    
    def broadcast_analytics(self):
        """Broadcast updated analytics to all clients"""
        analytics_data = analytics.get_analytics()  # Uses backward compatible method
        socketio.emit("analytics_update", analytics_data)

web_portal = WebPortal()

# Setup Discord bridge
discord_bridge = setup_discord_bridge(web_portal)

def start_discord_bridge():
    """Start Discord bridge in a separate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(discord_bridge.start())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    discord_connected = False
    if discord_bridge and hasattr(discord_bridge.bot, 'is_ready'):
        try:
            discord_connected = discord_bridge.bot.is_ready()
        except:
            discord_connected = False
    
    return jsonify({
        "status": "online",
        "clients_connected": web_portal.connected_clients,
        "discord_connected": discord_connected,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/servers")
def api_servers():
    """Get list of servers Melody is in"""
    if discord_bridge and discord_bridge.bot.is_ready():
        servers = []
        for guild in discord_bridge.bot.guilds:
            servers.append({
                'id': str(guild.id),
                'name': guild.name,
                'icon': str(guild.icon.url) if guild.icon else None,
                'member_count': guild.member_count
            })
        return jsonify(servers)
    return jsonify([])

@app.route("/api/servers/<int:server_id>/channels")
def api_server_channels(server_id):
    """Get text channels for a specific server"""
    if discord_bridge and discord_bridge.bot.is_ready():
        guild = discord_bridge.bot.get_guild(server_id)
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

@app.route("/api/set_target_channel", methods=["POST"])
def api_set_target_channel():
    """Change the target channel for messages"""
    data = request.json
    channel_id = data.get("channel_id")
    
    if channel_id and discord_bridge:
        try:
            discord_bridge.target_channel_id = int(channel_id)
            print(f"🎯 TARGET CHANNEL CHANGED: {channel_id}")
            
            channel = discord_bridge.bot.get_channel(int(channel_id))
            channel_info = f"#{channel.name}" if channel else "Unknown Channel"
            
            socketio.emit("target_channel_changed", {
                "channel_id": channel_id,
                "channel_name": channel_info,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return jsonify({"status": "success", "channel_id": channel_id, "channel_name": channel_info})
        except Exception as e:
            print(f"❌ Error setting target channel: {e}")
            return jsonify({"error": str(e)}), 400
    
    return jsonify({"error": "Invalid channel ID"}), 400

@app.route("/api/send_message", methods=["POST"])
def api_send_message():
    data = request.json
    message = data.get("message", "").strip()
    user = data.get("user", "Hatsona Milku")
    
    if message:
        web_msg = {
            "id": len(web_portal.message_history) + 1,
            "user": user,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "web",
            "mysterious": True
        }
        web_portal.message_history.append(web_msg)
        web_portal.broadcast_message(web_msg)
        
        # Track analytics
        analytics.track_message(web_msg)
        
        print(f"🌩️ WEB MESSAGE: {user} says: {message}")
        
        # Send to Discord if bridge is ready
        if discord_bridge and hasattr(discord_bridge.bot, 'is_ready') and discord_bridge.bot.is_ready():
            asyncio.run_coroutine_threadsafe(
                discord_bridge.send_to_discord(web_msg),
                discord_bridge.bot.loop
            )
        
        return jsonify({"status": "sent", "message_id": web_msg["id"]})
    
    return jsonify({"error": "No message"}), 400

@app.route("/api/toggle_auto_yap", methods=["POST"])
def api_toggle_auto_yap():
    """Toggle Auto-Yap mode from web"""
    data = request.json
    enable = data.get("enable", False)
    
    if discord_bridge and hasattr(discord_bridge.bot, 'is_ready') and discord_bridge.bot.is_ready():
        try:
            enhanced_core = discord_bridge.bot.get_cog('EnhancedMelodyBotCore')
            if enhanced_core:
                channel_id = discord_bridge.target_channel_id
                if enable:
                    enhanced_core.auto_yap_channels.add(channel_id)
                    status = "enabled ✅"
                else:
                    enhanced_core.auto_yap_channels.discard(channel_id)
                    status = "disabled ❌"
                
                print(f"🔄 Auto-Yap {status} via web portal")
                
                socketio.emit("auto_yap_status", {"enabled": enable, "status": status})
                
                return jsonify({"status": "success", "auto_yap": enable})
        except Exception as e:
            print(f"❌ Failed to toggle Auto-Yap: {e}")
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Discord bridge not ready"}), 400

@app.route("/api/analytics")
def api_analytics():
    """Get analytics data"""
    return jsonify(analytics.get_analytics())  # Uses backward compatible method

# ENHANCED API ROUTES
@app.route("/api/enhanced_analytics")
def api_enhanced_analytics():
    """Get enhanced analytics with relationship data"""
    return jsonify(analytics.get_advanced_analytics())

@app.route("/api/void_whisper")
def api_void_whisper():
    """Get a random void whisper"""
    whisper = analytics.generate_void_whisper()
    return jsonify({"whisper": whisper})

@app.route("/api/cloud_response", methods=["POST"])
def api_cloud_response():
    """Get mysterious cloud response"""
    data = request.json
    message = data.get("message", "")
    user = data.get("user", "Anonymous")
    
    # Simple cloud response logic
    mysterious_responses = [
        "🌩️ The cloud stirs with your words...",
        "💫 A ripple in the digital ether...",
        "🌀 Patterns emerge from the chaos...",
        "🌌 The void whispers back...",
        "⚡ Energy flows between our connection...",
        "🌊 Currents of emotion detected...",
        "🔮 The future shimmers with possibilities...",
        "🌫️ Memories float to the surface..."
    ]
    
    response = random.choice(mysterious_responses)
    
    # Create cloud message
    cloud_msg = {
        "id": f"cloud_{datetime.utcnow().timestamp()}",
        "user": "🌩️ Hatsona Milku",
        "message": response,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "cloud",
        "mysterious": True
    }
    
    analytics.track_message(cloud_msg)
    web_portal.broadcast_message(cloud_msg)
    
    return jsonify({"response": response})

@socketio.on("connect")
def handle_connect():
    web_portal.connected_clients += 1
    print(f"🌐 CLIENT CONNECTED. Total: {web_portal.connected_clients}")
    socketio.emit("message_history", web_portal.message_history[-50:])
    
    # Send initial analytics - uses backward compatible method
    socketio.emit("analytics_update", analytics.get_analytics())

@socketio.on("disconnect")
def handle_disconnect():
    web_portal.connected_clients -= 1
    print(f"🌐 CLIENT DISCONNECTED. Total: {web_portal.connected_clients}")

@socketio.on("web_command")
def handle_web_command(data):
    command = data.get("command")
    print(f"🎮 WEB COMMAND: {command}")

@socketio.on("request_cloud_insight")
def handle_cloud_insight(data):
    """Handle requests for cloud insights"""
    user = data.get("user", "Anonymous")
    
    mysterious_responses = [
        f"🔮 Analyzing connection with {user}... the bond grows stronger!",
        f"💞 The cloud senses deep resonance with {user}",
        f"🌐 Network analysis: Multiple connection points with {user} detected",
        f"⚡ Energy flows harmoniously between the cloud and {user}"
    ]
    
    response = random.choice(mysterious_responses)
    
    socketio.emit("cloud_insight", {
        "user": user,
        "insight": response,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    print("🚀 STARTING MELODY AI WEB PORTAL - ENHANCED VERSION...")
    
    # Start Discord bridge in background thread
    discord_thread = threading.Thread(target=start_discord_bridge, daemon=True)
    discord_thread.start()
    
    # Start web portal
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)