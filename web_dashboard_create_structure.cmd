@echo off
REM ===============================================
REM Create Melody Web Portal Project Structure
REM ===============================================

REM Create main directory
mkdir melody-web-portal
cd melody-web-portal

REM -------------------------------
REM Backend
REM -------------------------------
mkdir backend
cd backend
(
echo # Main Flask server
) > app.py
(
echo # Discord ↔ Web communication
) > discord_bridge.py
(
echo # Real-time connections
) > websocket_manager.py
(
echo flask
echo flask-socketio
echo requests
) > requirements.txt
cd ..

REM -------------------------------
REM Frontend
REM -------------------------------
mkdir frontend
cd frontend
mkdir src
mkdir src\components
mkdir src\pages
mkdir src\styles
mkdir public

(
echo {
echo   "name": "melody-frontend",
echo   "version": "1.0.0",
echo   "dependencies": {},
echo   "scripts": {}
echo }
) > package.json
cd ..

REM -------------------------------
REM Shared
REM -------------------------------
mkdir shared
cd shared
(
echo # Shared configuration
) > config.py
cd ..

echo.
echo ✅ Folder structure created successfully!
pause
