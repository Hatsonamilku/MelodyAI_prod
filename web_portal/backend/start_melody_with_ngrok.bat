@echo off
echo 🚀 Starting Melody AI with Ngrok Tunnel...
echo.

cd /d C:\Users\roven\Desktop\melody_ai\melody_ai_v2\web_portal\backend

echo Starting Melody AI on port 5000...
start python production.py

echo Waiting for services to start...
timeout 20

echo Starting Ngrok tunnel...
C:\ngrok\ngrok.exe http 5000

echo.
echo ✅ Melody AI is now running!
echo 🌐 Internal: http://localhost:5000
echo 🌍 External: Check ngrok output above for public URL
echo.
echo 💡 Discord bot may take 30 seconds to connect fully
echo 💡 If servers don't load, wait 30 seconds and refresh the page
pause