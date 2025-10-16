# create_web_portal_fixed.py - NO UNICODE ERRORS
import os
import sys

def create_folder_structure():
    base_dir = "web_portal"
    
    folders = [
        f"{base_dir}/backend",
        f"{base_dir}/frontend/src/components",
        f"{base_dir}/frontend/src/pages", 
        f"{base_dir}/frontend/src/styles",
        f"{base_dir}/frontend/public",
        f"{base_dir}/shared",
        f"{base_dir}/backend/static",
        f"{base_dir}/backend/templates",
    ]
    
    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")
    
    # Create requirements.txt
    requirements_content = """Flask==2.3.0
Flask-SocketIO==5.3.0
python-socketio==5.8.0
eventlet==0.33.0
python-dotenv==1.0.0
discord.py==2.3.0
"""
    with open(f"{base_dir}/backend/requirements.txt", "w", encoding='utf-8') as f:
        f.write(requirements_content)
    
    # Create app.py (simplified version - NO EMOJIS)
    app_content = '''from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "melody_web_portal_secret_2024"
socketio = SocketIO(app, cors_allowed_origins="*")

class WebPortal:
    def __init__(self):
        self.connected_clients = 0
        self.message_history = []
    
    def broadcast_message(self, data):
        socketio.emit("new_message", data)

web_portal = WebPortal()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "online",
        "clients_connected": web_portal.connected_clients,
        "timestamp": datetime.utcnow().isoformat()
    })

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
        
        print(f"WEB MESSAGE: {user} says: {message}")
        return jsonify({"status": "sent", "message_id": web_msg["id"]})
    
    return jsonify({"error": "No message"}), 400

@socketio.on("connect")
def handle_connect():
    web_portal.connected_clients += 1
    print(f"CLIENT CONNECTED. Total: {web_portal.connected_clients}")
    socketio.emit("message_history", web_portal.message_history[-50:])

@socketio.on("disconnect")
def handle_disconnect():
    web_portal.connected_clients -= 1
    print(f"CLIENT DISCONNECTED. Total: {web_portal.connected_clients}")

@socketio.on("web_command")
def handle_web_command(data):
    command = data.get("command")
    print(f"WEB COMMAND: {command}")

if __name__ == "__main__":
    print("STARTING MELODY AI WEB PORTAL...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
'''
    with open(f"{base_dir}/backend/app.py", "w", encoding='utf-8') as f:
        f.write(app_content)

    # Create index.html (NO EMOJIS in Python strings)
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Melody AI Web Portal - Hatsona Milku</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #1a1a2e; 
            color: white; 
            margin: 0; 
            padding: 20px; 
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .cloud-title { 
            font-size: 2.5em; 
            color: #74b9ff; 
            margin-bottom: 10px; 
        }
        .messages { 
            height: 400px; 
            overflow-y: auto; 
            background: rgba(255,255,255,0.1); 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 20px; 
        }
        .message { 
            margin-bottom: 10px; 
            padding: 10px; 
            border-radius: 5px; 
            background: rgba(116, 185, 255, 0.2); 
        }
        .input-area { display: flex; gap: 10px; }
        .message-input { 
            flex: 1; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            background: rgba(255,255,255,0.1); 
            color: white; 
        }
        .send-btn { 
            padding: 10px 20px; 
            background: #6c5ce7; 
            border: none; 
            border-radius: 5px; 
            color: white; 
            cursor: pointer; 
        }
        .status { 
            padding: 10px; 
            border-radius: 5px; 
            margin-bottom: 15px; 
            text-align: center; 
        }
        .online { background: rgba(0, 184, 148, 0.3); }
        .offline { background: rgba(255, 118, 117, 0.3); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="cloud-title">Hatsona Milku</h1>
            <p>Melody AI Web Portal - The Cloud Speaks</p>
        </div>
        
        <div class="status offline" id="connectionStatus">
            Connecting to cloud...
        </div>
        
        <div class="messages" id="messages">
            <div class="message">
                <strong>The Cloud:</strong> The void awaits your words...
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" class="message-input" id="messageInput" 
                   placeholder="Whisper to the void..." maxlength="500">
            <button class="send-btn" onclick="sendMessage()">Send to Cloud</button>
        </div>
    </div>

    <script src="https://cdn.socket.io/4.7.0/socket.io.min.js"></script>
    <script>
        const socket = io();
        
        socket.on("connect", () => {
            document.getElementById("connectionStatus").className = "status online";
            document.getElementById("connectionStatus").textContent = "CONNECTED to cloud";
        });

        socket.on("disconnect", () => {
            document.getElementById("connectionStatus").className = "status offline";
            document.getElementById("connectionStatus").textContent = "DISCONNECTED from cloud";
        });

        socket.on("new_message", (data) => {
            const messages = document.getElementById("messages");
            const messageEl = document.createElement("div");
            messageEl.className = "message";
            messageEl.innerHTML = "<strong>" + data.user + ":</strong> " + data.message;
            messages.appendChild(messageEl);
            messages.scrollTop = messages.scrollHeight;
        });

        socket.on("message_history", (messages) => {
            const messagesContainer = document.getElementById("messages");
            messagesContainer.innerHTML = '<div class="message"><strong>The Cloud:</strong> The void awaits your words...</div>';
            messages.forEach(msg => {
                const messageEl = document.createElement("div");
                messageEl.className = "message";
                messageEl.innerHTML = "<strong>" + msg.user + ":</strong> " + msg.message;
                messagesContainer.appendChild(messageEl);
            });
            messagesContainer.scrollTop = messages.scrollHeight;
        });

        function sendMessage() {
            const input = document.getElementById("messageInput");
            const message = input.value.trim();
            
            if (message) {
                fetch("/api/send_message", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message, user: "Hatsona Milku" })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "sent") {
                        input.value = "";
                    }
                });
            }
        }

        document.getElementById("messageInput").addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
    </script>
</body>
</html>
'''
    with open(f"{base_dir}/backend/templates/index.html", "w", encoding='utf-8') as f:
        f.write(html_content)

    # Create environment file
    env_content = """# Melody AI Web Portal Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here
WEB_PORTAL_CHANNEL_ID=1337024526923595786
FLASK_SECRET_KEY=melody_web_portal_secret_2024
WEB_PORTAL_PORT=5000
WEB_PORTAL_HOST=0.0.0.0
FLASK_ENV=development
"""
    with open(f"{base_dir}/.env", "w", encoding='utf-8') as f:
        f.write(env_content)

    print("SUCCESS: Web Portal Structure Created!")
    print("")
    print("NEXT STEPS:")
    print("1. Install dependencies: pip install -r web_portal/backend/requirements.txt")
    print("2. Start web portal: cd web_portal/backend && python app.py")
    print("3. Open http://localhost:5000 in your browser")

if __name__ == "__main__":
    create_folder_structure()