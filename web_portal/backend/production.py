# production.py - SUPER SIMPLE VERSION
from app import app, socketio

if __name__ == "__main__":
    print("🌐 MELODY AI - PRODUCTION MODE")
    print("=" * 50)
    print("✅ Internal: http://localhost:5000")
    print("🌍 External: Use ngrok to get public URL")
    print("🔒 Debug: DISABLED for security")
    print("=" * 50)
    print("💡 Discord bot will connect automatically")
    print("💡 May take 30 seconds to fully initialize")
    print("=" * 50)
    
    socketio.run(
        app,
        host='localhost',
        port=5000,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )