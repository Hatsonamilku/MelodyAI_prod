# melody_ai_v2/start_bot.py
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now launch the bot
from launch.main import main

if __name__ == "__main__":
    main()