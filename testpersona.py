# melody_ai_v2/test_personality_v3.py (SAVE IN PROJECT ROOT, NOT IN TEST FOLDER)
import os
import asyncio
import sys
from dotenv import load_dotenv

# Add the current directory to Python path to find your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

async def quick_test():
    """Simple test that won't break on imports"""
    try:
        # Try to import your modules
        from services.ai_providers.deepseek_client import DeepSeekClient
        from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
        from brain.personality.emotional_core import emotional_core
        
        print("✅ All imports successful!")
        
        # Check API key
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("❌ DEEPSEEK_API_KEY not found in .env file!")
            return
        
        print("✅ API key found!")
        
        # Initialize AI client
        ai_client = DeepSeekClient(api_key=api_key)
        test_user = "test_user_123"
        
        # Simple test message
        test_message = "Hello Melody! How are you today?"
        print(f"\n🧪 Testing: '{test_message}'")
        
        # Get emotional context
        emotional_ctx = emotional_core.get_emotional_context(test_user, test_message)
        print(f"🎭 Emotional Context: {emotional_ctx}")
        
        # Generate response
        response = await intelligence_orchestrator.generate_response(
            test_user, test_message, ai_provider=ai_client
        )
        
        print(f"🤖 Melody Response: {response}")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure this script is in your PROJECT ROOT (melody_ai_v2 folder)")
        print("2. Check that all your module files exist")
        print("3. Verify folder structure matches imports")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def basic_sentiment_test():
    """Test just the emotional core without API calls"""
    try:
        from brain.personality.emotional_core import emotional_core
        
        print("\n🧪 BASIC SENTIMENT TEST")
        print("=" * 40)
        
        test_messages = [
            "I love you so much! 💖",
            "You're amazing!",
            "meh whatever",
            "you suck lol 💀",
            "bro that's fire no cap"
        ]
        
        test_user = "sentiment_test_user"
        
        for msg in test_messages:
            emotional_ctx = emotional_core.get_emotional_context(test_user, msg)
            personality_mode = "AFFECTIONATE" if emotional_ctx['score'] >= 80 else \
                             "PLAYFUL" if emotional_ctx['score'] >= 50 else \
                             "CHILL" if emotional_ctx['score'] >= 20 else "COLD"
            
            print(f"💬 '{msg}'")
            print(f"   🎯 Score: {emotional_ctx['score']} | Mode: {personality_mode}")
            print(f"   😊 Sentiment: {emotional_ctx['sentiment']}")
            print(f"   🔥 Gen Alpha: {emotional_ctx['gen_alpha_vibes']}")
            print()
            
    except ImportError as e:
        print(f"❌ Cannot import emotional_core: {e}")

async def main():
    print("🚀 Melody AI V3 Personality Test")
    print("=" * 50)
    
    # First test basic sentiment
    await basic_sentiment_test()
    
    # Then test full system
    await quick_test()

if __name__ == "__main__":
    asyncio.run(main())