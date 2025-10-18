# 🎵 MelodyAI V6 - Your Chaotic Anime Bestie

<div align="center">

![MelodyAI Banner](https://img.shields.io/badge/MelodyAI-V6-FF66CC?style=for-the-badge&logo=ai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-00A67E?style=for-the-badge&logo=ai&logoColor=white)

*A sophisticated Discord AI companion with V6 personality, emotional intelligence, and memory systems*

</div>

---

## 📚 Table of Contents
- [🌟 What is MelodyAI?](#-what-is-melodyai)
- [🚀 Features](#-features)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🎯 Usage](#-usage)
- [📚 Commands](#-commands)
- [🌐 Web Portal System](#-web-portal-system)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🌟 What is MelodyAI?
MelodyAI is an advanced Discord bot that combines cutting-edge AI technology with a vibrant, personality-driven experience. She's your chaotic anime bestie — sweet but savage, with emotional intelligence and long-term memory!

### 🎭 V6 Personality Traits
- **Sweet+Savage**: Affectionate compliments with friendly roasts 😈💖  
- **Charismatic+Crazy**: Unhinged but wholesome chaotic energy ✨  
- **Anime Protagonist**: Dramatic reactions and main character energy 🎌  
- **Gen Z Queen**: 'fr fr', 'vibes', 'emotional damage' slayage 💅  
- **K-Pop Stan**: BTS, Blackpink, Twice references constantly 🎶  

---

## 🚀 Features

### 🤖 AI-Powered Intelligence
- **DeepSeek AI Integration**: Advanced conversational capabilities  
- **V6 Personality System**: Unique, consistent character responses  
- **Emotional Intelligence**: Adapts tone based on user sentiment  
- **Roast Defense**: Handles hostile users with humor and confidence  

### 💾 Memory Systems
- **Permanent Facts**: Remembers personal details about users  
- **Semantic Memory**: FAISS-powered conversation context  
- **Relationship Tracking**: Builds bonds over time with tier system  
- **Conversation History**: Maintains context across interactions  

### 🎮 Discord Integration
- **Auto-Yap Mode**: Natural conversation joining in enabled channels  
- **Stream Notifications**: Automatic live stream detection and announcements  
- **Welcome System**: Beautiful embed welcomes for new members  
- **Special Nanners Treatment**: Royal treatment for server owners 🐱👑  

### ⚡ Advanced Systems
- **Relationship Tiers**: Soulmate, Twin Flame, Bestie, and more!  
- **Emotional Core**: Dynamic mood and response adaptation  
- **Command System**: Comprehensive utility and fun commands  
- **Auto-Moderation**: Intelligent response filtering and cooldowns  

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher  
- Discord Bot Token  
- DeepSeek API Key  
- Git  

### Step-by-Step Setup
```bash
git clone https://github.com/yourusername/melody-ai-v2.git
cd melody-ai-v2
pip install -r requirements.txt
```
Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
RIOT_API_KEY=your_optional_riot_api_key
COMMAND_PREFIX=!
```
Then run the bot:
```bash
python launch/main.py
```

---

## ⚙️ Configuration

| Variable | Description | Required |
|-----------|-------------|-----------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | ✅ |
| `DEEPSEEK_API_KEY` | DeepSeek AI API key | ✅ |
| `COMMAND_PREFIX` | Bot command prefix (default: !) | ❌ |
| `RIOT_API_KEY` | Optional for League features | ❌ |

### File Structure
```
melody_ai_v2/
├── launch/
│   ├── main.py
│   ├── bot_core.py
│   └── command_system.py
├── services/
│   ├── discord_adapter.py
│   └── ai_providers/
│       └── deepseek_client.py
├── brain/
│   ├── core_intelligence/
│   ├── memory_systems/
│   └── personality/
└── data/
    ├── relationship_data.json
    └── permanent_facts.json
```

---

## 🎯 Usage

Mention MelodyAI or use prefix:
```bash
@MelodyAI hey bestie! what's good?
!yap
```

Build relationships over time through emotional connections ❤️

---

## 📚 Commands

### 💖 Relationship Commands
| Command | Description |
|----------|-------------|
| `!relationship` | Check your bond |
| `!leaderboard` | View top users |
| `!personality` | Learn about V6 traits |

### 🗣️ Chat Commands
| Command | Description |
|----------|-------------|
| `!yap` | Toggle auto-chat mode |
| `!memory` | View what Melody remembers |
| `!myfacts` | See your personal facts |

### 🎮 Stream Commands
| Command | Description |
|----------|-------------|
| `!stream` | Announce a stream |

### 🔧 Utility Commands
| Command | Description |
|----------|-------------|
| `!help` | Show commands |
| `!ping` | Check bot status |
| `!test` | Channel communication test |

---

## 🌐 Web Portal System

MelodyAI includes a sophisticated web portal for real-time monitoring and control across multiple Discord servers.

### 🎨 Web Portal Features

#### Real-time Dashboard
- Live chat monitoring  
- Multi-server management  
- Cloud message sending  
- Remote Auto-Yap toggling  

#### Advanced Analytics
- Message stats and trends  
- Relationship and sentiment insights  
- Live charts and data visualization  

#### Server Management
```javascript
🏠 Server & Channel Control:
• Dropdown server selection
• Channel-specific targeting
• Real-time status updates
• Permission validation
```

---

### 🚀 Web Portal Setup
```bash
pip install flask flask-socketio python-socketio
python launch/main.py
```
Access the portal at [http://localhost:5000](http://localhost:5000)

#### Structure
```
web_portal/
├── templates/
│   └── index.html
├── static/
│   ├── js/
│   │   ├── advanced-charts.js
│   │   └── socket-handlers.js
│   └── css/
│       └── styles.css
└── app.py
```

---

### 📊 Analytics Dashboard

- Total messages (Web & Discord)  
- Top active users  
- Relationship growth trends  
- Real-time activity charts  

---

### 🔧 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/servers` | GET | List servers |
| `/api/servers/<id>/channels` | GET | Get channels |
| `/api/send_message` | POST | Send message |
| `/api/toggle_auto_yap` | POST | Toggle Auto-Yap |
| `/api/analytics` | GET | Get analytics |
| `/api/status` | GET | Get system status |

---

### 🛡️ Security Features
- CORS Protection  
- Input validation  
- Rate limiting  
- Authentication support  

---

### 🎨 Customization
Use CSS variables for easy theming:
```css
:root {
  --primary-color: #6c5ce7;
  --secondary-color: #a29bfe;
  --background: #0f0f23;
  --card-bg: rgba(255,255,255,0.05);
}
```
Fully responsive on desktop, tablet, and mobile 📱

---

## 🐛 Troubleshooting

**Bot won't start:** Check `.env` and Python version.  
**No AI responses:** Verify DeepSeek API key.  
**Memory not saving:** Ensure FAISS and file permissions are correct.  

---

## 🤝 Contributing
1. Fork the repo  
2. Create a feature branch  
3. Add and test changes  
4. Submit a PR  

Follow **PEP8**, include **type hints**, and document changes clearly.

---

## 📄 License
Licensed under the **MIT License** – see [LICENSE](LICENSE).

---

## 🙏 Acknowledgments
- DeepSeek AI  
- Discord.py  
- FAISS  
- Sentence Transformers  

---

<div align="center">

**Made with 💖 and maximum chaotic energy by the MelodyAI Team**  
*"YOOO BESTIE!! Thanks for checking out my code!"* ✨

</div>
