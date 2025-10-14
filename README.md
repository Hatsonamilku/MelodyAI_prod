# 🎵 MelodyAI_prod — Production-Ready Discord AI Bot

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Commit](https://img.shields.io/github/last-commit/Hatsonamilku/MelodyAI_prod)](https://github.com/Hatsonamilku/MelodyAI_prod/commits/main)
[![Stars](https://img.shields.io/github/stars/Hatsonamilku/MelodyAI_prod?style=social)](https://github.com/Hatsonamilku/MelodyAI_prod)

MelodyAI_prod is the **production version of the MelodyAI Discord bot**, a modular, personality-driven AI system featuring:
- Advanced **sentiment analysis**
- Persistent **user memory**
- Real-time **conversation adaptation**
- **DeepSeek API** integration for natural responses
- Modular architecture for easy expansion
- Secure async systems for scalable multi-server use

---

## 🧠 Overview

MelodyAI is designed to **feel alive** — blending emotional context, memory, and expressive dialogue into a seamless Discord experience.  
It’s built to run efficiently across **multiple servers**, maintaining **personalized memory** for each user while responding naturally and emotionally.

---

## ✨ Core Features

| Category | Description |
|-----------|-------------|
| 💬 **AI Conversation Engine** | DeepSeek API integration for natural, context-aware conversations |
| 🧠 **Memory System** | Stores user data persistently (preferences, emotional tone, context history) |
| 🎭 **Sentiment System** | Detects user mood and adjusts tone dynamically |
| 🎶 **Music System (Optional)** | Discord audio playback with emotional tagging |
| 🧩 **Modular Commands** | Separate systems for TTS, debug, and memory management |
| 🧾 **Logging & Error Handling** | Detailed production-safe logs for all system modules |
| ⚡ **Asynchronous Design** | Handles multiple Discord servers efficiently |
| 🔒 **Environment Isolation** | Secure API keys and config loading via `.env` |

---

## 🏗️ Project Structure

```
MelodyAI_prod/
├── brain/                   # AI personality & context processors
├── config/                  # Environment variables & runtime configuration
├── features/                # Core bot features (TTS, commands, sentiment, etc.)
├── launch/                  # Bot entry points & startup logic
├── services/                # DeepSeek, Discord, and API integrations
├── systems/                 # Memory system, helper modules, analytics, etc.
├── test/                    # Unit & integration tests
│
├── run_melody.py            # Main entry point for MelodyAI system
├── start_bot.py             # Discord bot launcher
├── setup.py                 # Installation script
├── requirements.txt         # Python dependencies
├── melody_memory.db         # Local memory database (SQLite)
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Hatsonamilku/MelodyAI_prod.git
cd MelodyAI_prod
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🔐 Configuration

Create a `.env` file in the root directory:

```
DISCORD_TOKEN=your_discord_bot_token
DEEPSEEK_API_KEY=your_deepseek_api_key
DATABASE_URL=sqlite:///melody_memory.db
LOG_LEVEL=INFO
```

---

## 🚀 Run MelodyAI

```bash
python start_bot.py
```

Optional:
```bash
python run_melody.py
python testpersona.py
```

---

## 🧠 Memory System

The memory system persists user-specific data such as emotional tone, preferences, and personality cues using SQLite.

```python
from systems.memory_system import UserMemory

memory = UserMemory()
memory.store("Alice", "likes cheerful replies")
print(memory.recall("Alice"))
```

---

## 💬 Sentiment System

MelodyAI detects emotional tone and adapts accordingly.

| Type | Example | Behavior |
|------|----------|-----------|
| Positive | "You're awesome!" | Responds warmly |
| Neutral | "Hey" | Normal tone |
| Negative | "You suck" | Empathetic or playful tone |

---

## 🌐 DeepSeek API

Used for all conversational logic and tone matching.

```json
{
  "user": "Alice",
  "context": "Positive",
  "message": "I had a great day!",
  "personality": "Melody"
}
```

---

## 🧩 Commands

| Command | Description |
|----------|-------------|
| `/memory recall` | Retrieve last memory |
| `/memory clear` | Clear stored data |
| `/tts` | Generate voice reply |
| `/debug info` | Show diagnostics |
| `/emotion check` | Display sentiment status |

---

## 📜 Logging

Uses structured logging for all systems:

```python
import logging
logger = logging.getLogger("melodyai")
logger.info("Bot started successfully.")
```

---

## 🧍 Maintainer

**Author:** [Hatsonamilku](https://github.com/Hatsonamilku)  
**License:** MIT  
**Version:** Production Build (v3.0)  
**Location:** Mauritius  

---

## ❤️ Credits

- [Discord.py](https://discordpy.readthedocs.io/)
- [DeepSeek API](https://deepseek.com/)
- [SQLite](https://www.sqlite.org/)

> “MelodyAI doesn’t just chat — she remembers, reacts, and feels.” 🎶  
> — *Hatsonamilku, 2025*
