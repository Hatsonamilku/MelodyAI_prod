# melody_ai_v2/services/discord_adapter.py - FIXED VERSION
from typing import List, Dict, Optional
import asyncio
import discord
from datetime import datetime
import logging

# ✅ Absolute imports
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from brain.personality.emotional_core import EmotionalCore
from brain.memory_systems.permanent_facts import permanent_facts

logger = logging.getLogger(__name__)

class DiscordMelodyAdapter:
    def __init__(self):
        self.emotional_core = EmotionalCore()
        self.active_conversations: Dict[int, List[Dict]] = {}  # channel_id -> messages
        self.user_last_active: Dict[int, Dict[str, datetime]] = {}  # channel_id -> {user_id: last_active}
        self.summary_threshold = 10  # summarize every 10 messages

    async def debug_send_message(self, channel: discord.TextChannel, message: str) -> bool:
        """Debug method to test channel sending"""
        try:
            print(f"🔍 DEBUG SEND: Attempting to send to channel '{channel.name}' (ID: {channel.id})")
            print(f"🔍 DEBUG SEND: Message content: '{message}'")
            
            # Test basic message send
            sent_message = await channel.send(message)
            print(f"✅ DEBUG SEND: SUCCESS - Message sent with ID: {sent_message.id}")
            return True
            
        except discord.Forbidden:
            print("❌ DEBUG SEND: FORBIDDEN - Bot lacks permissions to send messages")
            return False
        except discord.HTTPException as e:
            print(f"❌ DEBUG SEND: HTTP ERROR - {e}")
            return False
        except Exception as e:
            print(f"❌ DEBUG SEND: UNKNOWN ERROR - {e}")
            return False

    async def debug_channel_permissions(self, channel: discord.TextChannel):
        """Debug channel permissions"""
        print(f"🔍 CHANNEL DEBUG: {channel.name} (ID: {channel.id})")
        print(f"🔍 CHANNEL DEBUG: Type: {type(channel)}")
        
        # Check bot permissions
        bot_perms = channel.permissions_for(channel.guild.me)
        print(f"🔍 CHANNEL DEBUG: Send Messages: {bot_perms.send_messages}")
        print(f"🔍 CHANNEL DEBUG: Read Messages: {bot_perms.read_messages}")
        print(f"🔍 CHANNEL DEBUG: View Channel: {bot_perms.view_channel}")
        print(f"🔍 CHANNEL DEBUG: Read Message History: {bot_perms.read_message_history}")

    async def test_channel_communication(self, channel: discord.TextChannel):
        """Test the complete communication flow in a channel"""
        print(f"🧪 COMPREHENSIVE CHANNEL TEST: {channel.name}")
        
        # 1. Test permissions
        await self.debug_channel_permissions(channel)
        
        # 2. Test basic message send
        success = await self.debug_send_message(channel, "🧪 Test 1: Basic message send")
        if not success:
            print("❌ TEST FAILED: Basic message send")
            return False
        
        # 3. Test fact extraction
        test_message = "My name is TestUser and I live in Tokyo"
        print(f"🧪 Testing fact extraction: '{test_message}'")
        facts = await permanent_facts.extract_personal_facts("test_user", test_message)
        print(f"🧪 Facts extracted: {len(facts)}")
        
        # 4. Test AI response
        try:
            response = await intelligence_orchestrator.generate_response(
                user_id="test_user", 
                user_message="Hello!",
                ai_provider=None
            )
            print(f"🧪 AI Response: {response}")
            
            # 5. Send AI response
            await channel.send(f"🧪 AI Test Response: {response}")
            print("✅ ALL TESTS PASSED!")
            return True
            
        except Exception as e:
            print(f"❌ AI TEST FAILED: {e}")
            return False

    async def process_discord_message(self, message: discord.Message, ai_provider=None, respond: bool = True) -> Optional[str]:
        if message.author.bot or not message.content:
            print("❌ DEBUG: Ignoring bot message or empty content")
            return None

        user_id = str(message.author.id)
        channel_id = message.channel.id
        user_message = message.content

        print(f"🔍 DEBUG: Processing message from {user_id} in channel {channel_id}")
        print(f"🔍 DEBUG: Message content: '{user_message}'")

        # 🆕 CRITICAL: Debug channel permissions FIRST
        print(f"🔍 DEBUG: Checking channel permissions...")
        await self.debug_channel_permissions(message.channel)

        # 🆕 CRITICAL FIX: Extract facts from user message FIRST
        print(f"🔍 DEBUG: Extracting facts from user message: '{user_message}'")
        extracted_facts = await permanent_facts.extract_personal_facts(user_id, user_message)
        
        if extracted_facts:
            print(f"🎉 DEBUG: Storing {len(extracted_facts)} extracted facts")
            await permanent_facts.store_facts(user_id, extracted_facts)
        else:
            print("ℹ️ DEBUG: No facts extracted from this message")

        # Track conversation
        self.active_conversations.setdefault(channel_id, []).append({
            "user_id": user_id,
            "message": user_message,
            "timestamp": datetime.now().isoformat()
        })
        self.user_last_active.setdefault(channel_id, {})[user_id] = datetime.now()

        if len(self.active_conversations[channel_id]) >= self.summary_threshold:
            await self._summarize_conversation(channel_id, ai_provider)

        # 🆕 CRITICAL FIX: Get UPDATED user context (with newly extracted facts)
        print(f"🔍 DEBUG: Getting user context for {user_id}")
        user_context = await permanent_facts.get_user_context(user_id)
        conversation_summary = permanent_facts.storage.data["users"].get(user_id, {}).get("conversation_summary", "")
        if conversation_summary:
            user_context += f"\n\n📝 Previous chat summary:\n{conversation_summary}"

        final_prompt = user_message
        if user_context:
            final_prompt = f"{user_context}\n\nUser says: {user_message}"
            print(f"🔍 DEBUG: Enhanced prompt with context: {len(user_context)} chars")

        try:
            print(f"🔍 DEBUG: Generating AI response for user {user_id}")
            response = await intelligence_orchestrator.generate_response(
                user_id=user_id,
                user_message=final_prompt,
                ai_provider=ai_provider
            )
            
            # 🆕 CRITICAL: Check if response is valid
            if not response or response.strip() == "":
                print("❌ DEBUG: Empty response from AI")
                response = "Hmm, I'm having trouble thinking of a response right now! 💫"
            
            print(f"✅ DEBUG: AI response generated: '{response}'")
            
            # 🆕 CRITICAL FIX: If respond=False, RETURN the response instead of sending
            if not respond:
                print(f"🔧 DEBUG: Returning response (not sending): '{response}'")
                return response  # 🚀 THIS IS THE FIX!
            
            # 🆕 CRITICAL: Test channel access FIRST
            print(f"🚀 DEBUG: Testing channel access...")
            test_success = await self.debug_send_message(message.channel, "🔄 Testing channel access...")
            
            if not test_success:
                print("❌ DEBUG: Channel test failed - cannot send messages")
                return "I can't send messages in this channel! Check my permissions! 🔒"
            
            # 🆕 ACTUAL MESSAGE SEND with better error handling
            print(f"🚀 DEBUG: Sending actual response to Discord...")
            try:
                # Truncate if too long for Discord
                if len(response) > 2000:
                    response = response[:1997] + "..."
                
                sent_message = await message.channel.send(response)
                print(f"🎉 DEBUG: SUCCESS! Message sent with ID: {sent_message.id}")
                print(f"🎉 DEBUG: Channel: {message.channel.name} (ID: {message.channel.id})")
                return response
                
            except discord.Forbidden:
                print("❌ DEBUG: FORBIDDEN - No permission to send messages")
                return "I don't have permission to send messages here! 🔒"
            except discord.HTTPException as e:
                print(f"❌ DEBUG: HTTP ERROR - {e}")
                return "Message sending failed due to network issues! 📡"
            except Exception as e:
                print(f"❌ DEBUG: UNKNOWN SEND ERROR - {e}")
                return "Oops! Message delivery failed! 💫"
                
        except Exception as e:
            logger.error(f"❌ Error in generate_response: {e}")
            print(f"❌ DEBUG: Error in AI response generation: {e}")
            return "My brain glitched! Try again? 💫"

    async def _summarize_conversation(self, channel_id: int, ai_provider=None):
        messages = self.active_conversations.get(channel_id, [])
        if not messages:
            return

        summaries = {}
        for msg in messages:
            uid = msg["user_id"]
            summaries.setdefault(uid, "")
            # FIXED: Use different quotes to avoid f-string parsing issues
            summaries[uid] += f"{msg['message']} "

        for uid, full_text in summaries.items():
            try:
                summary_prompt = f"Summarize this conversation concisely for memory storage:\n{full_text}"
                summary_text = await intelligence_orchestrator.generate_response(
                    user_id=uid,
                    user_message=summary_prompt,
                    ai_provider=ai_provider
                )
                await permanent_facts.store_facts(uid, [{
                    "key": "conversation_summary",
                    "value": summary_text,
                    "category": "general",
                    "confidence": 3
                }])
            except Exception as e:
                logger.error(f"❌ Error summarizing conversation for user {uid}: {e}")

        self.active_conversations[channel_id] = []

    async def handle_mention(self, message: discord.Message, ai_provider=None) -> str:
        user_id = str(message.author.id)
        user_message = message.content.replace(f"<@{message.client.user.id}>", "").strip()
        
        print(f"🔍 MENTION DEBUG: User {user_id} mentioned me: '{user_message}'")
        
        if not user_message:
            return "Hey! You mentioned me? 💫 What's up?"
            
        return await self.process_discord_message(message, ai_provider, respond=True)

    def get_user_emotional_state(self, user_id: str) -> Dict[str, any]:
        return self.emotional_core.get_emotional_state(user_id)

    def get_user_facts(self, user_id: str) -> str:
        return permanent_facts.get_user_context(user_id)

    async def send_test_message(self, channel: discord.TextChannel) -> bool:
        """Test method to send a simple message"""
        print(f"🧪 TEST: Sending test message to {channel.name}")
        try:
            test_msg = await channel.send("🧪 Test message from MelodyAI! If you see this, bot can send messages.")
            print(f"✅ TEST: Success! Message ID: {test_msg.id}")
            return True
        except Exception as e:
            print(f"❌ TEST: Failed to send test message: {e}")
            return False

    async def quick_diagnostic(self, channel: discord.TextChannel) -> str:
        """Quick diagnostic to identify the exact issue"""
        print(f"🩺 QUICK DIAGNOSTIC: Starting for channel {channel.name}")
        
        results = []
        
        # 1. Check permissions
        bot_perms = channel.permissions_for(channel.guild.me)
        results.append(f"📊 Permissions: Send={bot_perms.send_messages}, Read={bot_perms.read_messages}")
        
        # 2. Test basic send
        try:
            test_msg = await channel.send("🩺 Diagnostic test message")
            results.append("✅ Basic message send: WORKING")
            await test_msg.delete()  # Clean up
        except Exception as e:
            results.append(f"❌ Basic message send: FAILED - {e}")
        
        # 3. Test fact extraction
        try:
            facts = await permanent_facts.extract_personal_facts("diagnostic_user", "My name is Diagnostic and I'm 25 years old")
            results.append(f"✅ Fact extraction: WORKING ({len(facts)} facts)")
        except Exception as e:
            results.append(f"❌ Fact extraction: FAILED - {e}")
        
        # 4. Test AI response
        try:
            response = await intelligence_orchestrator.generate_response(
                user_id="diagnostic_user",
                user_message="Hello diagnostic test",
                ai_provider=None
            )
            if response and response.strip():
                results.append("✅ AI response: WORKING")
            else:
                results.append("❌ AI response: EMPTY")
        except Exception as e:
            results.append(f"❌ AI response: FAILED - {e}")
        
        diagnostic_result = "\n".join(results)
        print(f"🩺 DIAGNOSTIC RESULTS:\n{diagnostic_result}")
        
        return diagnostic_result