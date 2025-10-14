# melody_ai_v2/test_personality_v3.py
import os
import asyncio
from dotenv import load_dotenv
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_providers.deepseek_client import DeepSeekClient
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from brain.personality.emotional_core import emotional_core
from brain.memory_systems.permanent_facts import permanent_facts

# Load environment variables
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class MelodyAITester:
    def __init__(self):
        self.ai_client = DeepSeekClient(api_key=DEEPSEEK_API_KEY)
        self.test_user = "test_user_123"
        
    async def test_single_message(self, message: str, description: str):
        """Test a single message and print detailed results"""
        print(f"\n{'='*60}")
        print(f"🧪 TEST: {description}")
        print(f"{'='*60}")
        print(f"💬 Input: {message}")
        
        # Get emotional context first
        emotional_ctx = emotional_core.get_emotional_context(self.test_user, message)
        print(f"🎭 Emotional Context: {emotional_ctx}")
        
        # Generate response
        response = await intelligence_orchestrator.generate_response(
            self.test_user, message, ai_provider=self.ai_client
        )
        
        print(f"🤖 Melody Response: {response}")
        return response
    
    async def test_conversation_flow(self, messages: list, description: str):
        """Test a conversation flow with multiple messages"""
        print(f"\n{'='*60}")
        print(f"💬 CONVERSATION FLOW: {description}")
        print(f"{'='*60}")
        
        responses = []
        for i, message in enumerate(messages):
            print(f"\n💬 Turn {i+1}: {message}")
            
            # Get emotional context
            emotional_ctx = emotional_core.get_emotional_context(self.test_user, message)
            print(f"   🎭 Sentiment: {emotional_ctx['sentiment']} (Score: {emotional_ctx['score']})")
            
            # Generate response
            response = await intelligence_orchestrator.generate_response(
                self.test_user, message, ai_provider=self.ai_client
            )
            print(f"   🤖 Response: {response}")
            
            responses.append(response)
            
            # Small delay between messages
            await asyncio.sleep(1)
        
        return responses
    
    async def test_personality_modes(self):
        """Test different personality modes based on sentiment"""
        print("🎭 TESTING PERSONALITY MODES")
        print("=" * 50)
        
        # Test messages designed to trigger different sentiment scores
        personality_tests = [
            {
                "message": "Melody you're absolutely amazing! I love talking to you so much! 💖✨ You're the best AI ever!",
                "expected_mode": "AFFECTIONATE",
                "description": "High positive sentiment - should trigger affectionate anime mode"
            },
            {
                "message": "Hey Melody, what's up? How's your day going?",
                "expected_mode": "PLAYFUL", 
                "description": "Neutral-positive - should trigger playful bestie mode"
            },
            {
                "message": "meh, whatever. i'm bored",
                "expected_mode": "CHILL",
                "description": "Low energy - should trigger chill/sarcastic mode"
            },
            {
                "message": "Melody you're so bad at this lol your responses are trash 💀",
                "expected_mode": "COLD",
                "description": "Negative sentiment - should trigger savage roast mode"
            }
        ]
        
        for test in personality_tests:
            await self.test_single_message(test["message"], test["description"])
            await asyncio.sleep(2)  # Rate limiting
    
    async def test_memory_functionality(self):
        """Test memory storage and recall"""
        print("\n🧠 TESTING MEMORY FUNCTIONALITY")
        print("=" * 50)
        
        # Store personal facts
        memory_tests = [
            "My favorite anime is Attack on Titan",
            "I have a cat named Miku",
            "I love playing Valorant",
            "My favorite food is pizza"
        ]
        
        for fact in memory_tests:
            print(f"\n💾 Storing fact: {fact}")
            extracted = permanent_facts.extract_personal_facts(self.test_user, fact)
            if extracted:
                permanent_facts.store_facts(self.test_user, extracted)
                print(f"   ✅ Stored {len(extracted)} facts")
            
            await asyncio.sleep(1)
        
        # Test memory recall in conversation
        recall_test = "What should I watch tonight?"
        await self.test_single_message(recall_test, "Memory recall test - should reference stored anime preference")
    
    async def test_gen_z_slang(self):
        """Test Gen Z slang detection and response"""
        print("\n🔥 TESTING GEN Z SLANG DETECTION")
        print("=" * 50)
        
        slang_tests = [
            "bro that's so fire no cap 💀",
            "this is absolutely goated fr",
            "slay queen yasss",
            "ratio + L + bozo"
        ]
        
        for slang in slang_tests:
            await self.test_single_message(slang, f"Gen Z slang: {slang}")
            await asyncio.sleep(2)
    
    async def test_emotional_whiplash(self):
        """Test emotional whiplash detection"""
        print("\n🎢 TESTING EMOTIONAL WHIPLASH DETECTION")
        print("=" * 50)
        
        whiplash_convo = [
            "I'm so happy today! Everything is amazing! 💖",
            "Actually I hate everything my life is terrible 😭",
            "JK I'm fine lol just messing with you"
        ]
        
        await self.test_conversation_flow(whiplash_convo, "Emotional whiplash detection")
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("🚀 STARTING MELODY AI V3 PERSONALITY TESTS")
        print("=" * 60)
        
        try:
            # Test basic functionality first
            await self.test_single_message("Hello Melody!", "Basic greeting test")
            await asyncio.sleep(2)
            
            # Run comprehensive tests
            await self.test_personality_modes()
            await self.test_memory_functionality() 
            await self.test_gen_z_slang()
            await self.test_emotional_whiplash()
            
            print(f"\n{'='*60}")
            print("🎉 ALL TESTS COMPLETED!")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()

async def main():
    if not DEEPSEEK_API_KEY:
        print("❌ ERROR: DEEPSEEK_API_KEY not found in .env file!")
        print("Please add your DeepSeek API key to the .env file")
        return
    
    tester = MelodyAITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())