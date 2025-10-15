# brain/memory_systems/permanent_facts.py - FIXED VERSION (NO DEADLOCKS)
import json
import asyncio
import os
from datetime import datetime, timedelta
import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger("MelodyBotCore")

# --------------------------
# Permanent Facts Storage
# --------------------------
class PermanentFacts:
    """Ultra-optimized async permanent facts storage with caching and health tracking"""

    CACHE_DURATION = 5  # seconds

    def __init__(self, file_path: str = "permanent_facts.json"):
        self.file_path = file_path
        self.lock = asyncio.Lock()
        self.data: Dict = {"users": {}}
        self._cache: Dict[str, str] = {}
        self._cache_time: Dict[str, float] = {}

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)
                self.data = self._convert_to_new_structure(loaded_data)
                logger.info(f"✅ Loaded permanent facts: {len(self.data['users'])} users")
                print(f"✅ DEBUG: Loaded {len(self.data['users'])} users from permanent_facts.json")
            except Exception as e:
                logger.error(f"❌ Failed to load permanent facts: {e}")
                print(f"❌ DEBUG: Failed to load permanent facts: {e}")
                self.data = {"users": {}}
        else:
            logger.info("🆕 No existing permanent_facts.json - starting fresh")
            print("🆕 DEBUG: No existing permanent_facts.json - starting fresh")

    # --------------------------
    # Data Conversion
    # --------------------------
    @staticmethod
    def _convert_to_new_structure(old_data: Dict) -> Dict:
        new_data = {"users": {}}
        print("🔄 DEBUG: Converting old JSON structure to new facts array format")
        for user_id, user_data in old_data.get("users", {}).items():
            facts = []
            for category, items in user_data.items():
                if isinstance(items, dict):
                    for key, value in items.items():
                        facts.append({
                            "key": key,
                            "value": str(value),
                            "category": category,
                            "confidence": 2,
                            "first_mentioned": datetime.now().isoformat(),
                            "last_mentioned": datetime.now().isoformat(),
                            "mention_count": 1
                        })
                        print(f"   🔄 Converted: {user_id}.{category}.{key} = {value}")
                elif category == "health_status" and isinstance(items, list):
                    new_data["users"][user_id] = {"facts": facts, "health_status": items}
                    print(f"   🔄 Preserved health status for {user_id}")
                    continue
            new_data["users"][user_id] = {"facts": facts}
            print(f"✅ DEBUG: Converted {user_id} - {len(facts)} facts")
        return new_data

    # --------------------------
    # Internal Async Save
    # --------------------------
    async def _save(self):
        """Save data without lock (lock should be handled by caller)"""
        try:
            # 🆕 REMOVED the lock here - caller should handle locking
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print("💾 DEBUG: Saved permanent_facts.json")
        except Exception as e:
            logger.error(f"❌ Failed to save permanent facts: {e}")
            print(f"❌ DEBUG: Save failed: {e}")

    # --------------------------
    # Facts Management - FIXED VERSION
    # --------------------------
    async def store_facts(self, user_id: str, facts: List[Dict]):
        """Store multiple facts efficiently with single save - FIXED DEADLOCK"""
        print(f"💾 DEBUG: Storing {len(facts)} facts for {user_id}")
        
        if not facts:
            return
            
        async with self.lock:  # 🆕 SINGLE LOCK for all operations
            user_data = self.data["users"].setdefault(user_id, {"facts": []})
            existing_facts = user_data["facts"]
            
            for fact in facts[:5]:  # Limit per message
                key = fact["key"]
                value = fact["value"]
                category = fact.get("category", "general")
                confidence = fact.get("confidence", 1)
                
                # Check if fact already exists
                found = False
                for existing_fact in existing_facts:
                    if existing_fact["key"] == key and existing_fact["category"] == category:
                        old_value = existing_fact["value"]
                        old_confidence = existing_fact.get("confidence", 1)
                        existing_fact.update({
                            "value": value,
                            "confidence": max(old_confidence, confidence),
                            "last_mentioned": datetime.now().isoformat(),
                            "mention_count": existing_fact.get("mention_count", 1) + 1
                        })
                        print(f"🔄 DEBUG: Updated fact {user_id}.{category}.{key}: '{old_value}' -> '{value}' (conf: {old_confidence}->{existing_fact['confidence']})")
                        found = True
                        break
                
                if not found:
                    existing_facts.append({
                        "key": key,
                        "value": value,
                        "category": category,
                        "confidence": confidence,
                        "first_mentioned": datetime.now().isoformat(),
                        "last_mentioned": datetime.now().isoformat(),
                        "mention_count": 1
                    })
                    print(f"✅ DEBUG: Added new fact {user_id}.{category}.{key} = '{value}' (conf: {confidence})")
            
            # 🆕 SINGLE SAVE after all facts are processed
            self._invalidate_cache(user_id)
            await self._save()
            print(f"✅ DEBUG: All facts stored successfully for {user_id}")

    async def add_fact(self, user_id: str, key: str, value: str,
                       category: str = "general", confidence: int = 1):
        """Add or update a single fact - COMPATIBILITY METHOD"""
        print(f"🔧 DEBUG: add_fact called for {user_id}.{category}.{key}")
        await self.store_facts(user_id, [{
            "key": key, 
            "value": value, 
            "category": category, 
            "confidence": confidence
        }])

    async def search_facts(self, user_id: str, min_confidence: int = 1) -> List[tuple]:
        async with self.lock:
            facts = self.data.get("users", {}).get(user_id, {}).get("facts", [])
            result = [(f["category"], f["key"], f["value"]) for f in facts if f.get("confidence", 1) >= min_confidence]
            print(f"🔍 DEBUG: Search for {user_id} (min_conf: {min_confidence}) -> {len(result)} facts")
            return result

    # --------------------------
    # Ultra-fast User Context
    # --------------------------
    async def get_user_context(self, user_id: str) -> str:
        now = asyncio.get_event_loop().time()
        if user_id in self._cache and now - self._cache_time.get(user_id, 0) < self.CACHE_DURATION:
            print(f"⚡ DEBUG: Using cached context for {user_id}")
            return self._cache[user_id]

        facts = self.data.get("users", {}).get(user_id, {}).get("facts", [])
        if not facts:
            self._cache[user_id] = ""
            self._cache_time[user_id] = now
            print(f"📭 DEBUG: No facts for {user_id} - empty context")
            return ""

        context_parts = []

        # High confidence facts
        high_facts = [f for f in facts if f.get("confidence", 1) >= 2]
        personal_facts = [f for f in high_facts if f["category"] in ["personal", "location"]][:3]
        media_facts = [f for f in high_facts if f["category"] in ["media_knowledge", "anime_characters"]][:2]

        print(f"🔧 DEBUG: Building context for {user_id} - {len(personal_facts)} personal, {len(media_facts)} media facts")

        for f in personal_facts + media_facts:
            value = f["value"] if len(f["value"]) <= 80 else f["value"][:77] + "..."
            context_parts.append(f"- {f['key'].replace('_',' ').title()}: {value}")

        context = f"📝 USER FACTS:\n" + "\n".join(context_parts) if context_parts else ""
        
        self._cache[user_id] = context
        self._cache_time[user_id] = now
        print(f"📋 DEBUG: Context built for {user_id} ({len(context)} chars)")
        return context

    # --------------------------
    # Extract Facts with ENHANCED DEBUG
    # --------------------------
    async def extract_personal_facts(self, user_id: str, message: str) -> List[Dict]:
        """Extract personal facts from a message with COMPLETE DEBUG"""
        facts = []
        msg = message.lower()
        
        print(f"\n🔍 FACT DEBUG: Analyzing message: '{message}'")
        print(f"🔍 FACT DEBUG: Lowercase version: '{msg}'")
        
        patterns_checked = []
        facts_found = []

        # Name detection with more patterns
        name_patterns = [
            r"my name is (\w+)", r"i'm called (\w+)", r"call me (\w+)",
            r"name's (\w+)", r"you can call me (\w+)", r"i am (\w+)",
            r"this is (\w+)", r"it's (\w+)", r"everyone calls me (\w+)"
        ]
        
        for pat in name_patterns:
            patterns_checked.append(f"name: {pat}")
            match = re.search(pat, msg)
            if match:
                name = match.group(1).title()
                facts.append({"category": "personal", "key": "name", "value": name, "confidence": 3})
                facts_found.append(f"name: {name}")
                print(f"✅ FACT DEBUG: Found name: {name} using pattern: {pat}")
                break
        else:
            print(f"❌ FACT DEBUG: No name patterns matched")

        # Location with more patterns
        location_patterns = [
            r"i live in (\w+)", r"i'm from (\w+)", r"based in (\w+)",
            r"located in (\w+)", r"from (\w+)"
        ]
        
        for pat in location_patterns:
            patterns_checked.append(f"location: {pat}")
            match = re.search(pat, msg)
            if match:
                location = match.group(1).title()
                facts.append({"category": "location", "key": "location", "value": location, "confidence": 2})
                facts_found.append(f"location: {location}")
                print(f"✅ FACT DEBUG: Found location: {location} using pattern: {pat}")
                break
        else:
            print(f"❌ FACT DEBUG: No location patterns matched")

        # Age detection
        age_patterns = [
            r"i am (\d+) years old", r"i'm (\d+)", r"age is (\d+)",
            r"(\d+) years old"
        ]
        
        for pat in age_patterns:
            patterns_checked.append(f"age: {pat}")
            match = re.search(pat, msg)
            if match:
                age = match.group(1)
                age_value = f"{age} years old"
                facts.append({"category": "personal", "key": "age", "value": age_value, "confidence": 2})
                facts_found.append(f"age: {age_value}")
                print(f"✅ FACT DEBUG: Found age: {age_value} using pattern: {pat}")
                break
        else:
            print(f"❌ FACT DEBUG: No age patterns matched")

        # Favorites with better categorization
        fav_patterns = [
            r"my favorite (.*?) is (.*?)", r"i love (.*?)", r"i like (.*?)",
            r"i enjoy (.*?)"
        ]
        
        for pat in fav_patterns:
            patterns_checked.append(f"favorite: {pat}")
            match = re.search(pat, msg)
            if match:
                if "favorite" in pat:
                    category = match.group(1)
                    item = match.group(2)
                    facts.append({"category": "preferences", "key": f"favorite_{category}", "value": item, "confidence": 2})
                    facts_found.append(f"favorite_{category}: {item}")
                    print(f"✅ FACT DEBUG: Found favorite: {category} = {item} using pattern: {pat}")
                else:
                    item = match.group(1)
                    facts.append({"category": "preferences", "key": f"likes_{item}", "value": "yes", "confidence": 1})
                    facts_found.append(f"likes_{item}: yes")
                    print(f"✅ FACT DEBUG: Found likes: {item} using pattern: {pat}")
                break
        else:
            print(f"❌ FACT DEBUG: No favorite/like patterns matched")

        # Anime character detection
        if "nice" in msg and "to be hero" in msg:
            facts.append({
                "category": "anime_characters", 
                "key": "nice_to_be_hero_x", 
                "value": "15th ranked hero, chaotic king",
                "confidence": 3
            })
            facts_found.append("anime: Nice from To Be Hero")
            print(f"✅ FACT DEBUG: Found anime reference: Nice from To Be Hero")

        # Health detection
        health_updated = False
        if any(x in msg for x in ["sick", "ill", "not feeling well"]):
            await self.update_health(user_id, "sick", 2)
            print(f"🏥 FACT DEBUG: Detected health issue - marked as sick")
            health_updated = True
        elif any(x in msg for x in ["better", "well", "good", "recovered"]):
            await self.update_health(user_id, "recovered", 1)
            print(f"🏥 FACT DEBUG: Detected health improvement - marked as recovered")
            health_updated = True
        
        if not health_updated:
            print(f"❌ FACT DEBUG: No health patterns matched")

        # COMPREHENSIVE DEBUG SUMMARY
        if facts:
            print(f"🎉 FACT DEBUG: SUCCESS! Extracted {len(facts)} facts: {facts_found}")
        else:
            print(f"🔍 FACT DEBUG: NO FACTS EXTRACTED - Checked {len(patterns_checked)} patterns:")
            for i, pattern in enumerate(patterns_checked[:12], 1):
                print(f"   {i:2d}. {pattern}")
            if len(patterns_checked) > 12:
                print(f"   ... and {len(patterns_checked) - 12} more patterns")

        # Invalidate cache when new facts are added
        if facts and user_id in self._cache:
            del self._cache[user_id]
            print(f"🔄 FACT DEBUG: Invalidated cache for {user_id}")

        return facts

    # --------------------------
    # Health Management
    # --------------------------
    async def update_health(self, user_id: str, status: str, severity: int = 1):
        async with self.lock:
            user_data = self.data["users"].setdefault(user_id, {"facts": []})
            health = user_data.setdefault("health_status", [])
            health.append({
                "status": status,
                "severity": severity,
                "reported_at": datetime.now().isoformat(),
                "is_resolved": False
            })
            await self._save()
            print(f"🏥 DEBUG: Updated health for {user_id}: {status} (severity: {severity})")

    async def check_health_follow_ups(self) -> List[tuple]:
        async with self.lock:
            now = datetime.now()
            results = []
            for uid, udata in self.data["users"].items():
                for entry in udata.get("health_status", []):
                    if not entry.get("is_resolved", False) and datetime.fromisoformat(entry["reported_at"]) + timedelta(hours=1) < now:
                        results.append((uid, entry["status"], entry["reported_at"]))
            print(f"🏥 DEBUG: Health follow-ups check: {len(results)} pending")
            return results[:10]

    async def mark_health_resolved(self, user_id: str):
        async with self.lock:
            resolved_count = 0
            for entry in self.data.get("users", {}).get(user_id, {}).get("health_status", []):
                if not entry.get("is_resolved", False):
                    entry["is_resolved"] = True
                    resolved_count += 1
            await self._save()
            print(f"🏥 DEBUG: Marked {resolved_count} health entries as resolved for {user_id}")

    # --------------------------
    # Cache Helper
    # --------------------------
    def _invalidate_cache(self, user_id: str):
        if user_id in self._cache:
            del self._cache[user_id]
            del self._cache_time[user_id]
            print(f"🔄 DEBUG: Invalidated cache for {user_id}")


# --------------------------
# Adapter for Backward Compatibility
# --------------------------
class PermanentFactsAdapter:
    def __init__(self):
        self.storage = PermanentFacts()
        print("🔧 DEBUG: PermanentFactsAdapter initialized")

    async def extract_personal_facts(self, user_id: str, message: str) -> List[Dict]:
        print(f"🔧 ADAPTER DEBUG: extract_personal_facts({user_id}, '{message}')")
        return await self.storage.extract_personal_facts(user_id, message)

    async def store_facts(self, user_id: str, facts: List[Dict]):
        print(f"🔧 ADAPTER DEBUG: store_facts({user_id}, {len(facts)} facts)")
        await self.storage.store_facts(user_id, facts)

    async def get_user_context(self, user_id: str) -> str:
        print(f"🔧 ADAPTER DEBUG: get_user_context({user_id})")
        return await self.storage.get_user_context(user_id)

    async def get_media_knowledge(self, user_id: str) -> str:
        print(f"🔧 ADAPTER DEBUG: get_media_knowledge({user_id})")
        context = await self.get_user_context(user_id)
        if "anime_characters" in context or "media_knowledge" in context:
            return context
        return ""

    async def check_health_follow_ups(self):
        print("🔧 ADAPTER DEBUG: check_health_follow_ups()")
        return await self.storage.check_health_follow_ups()

    async def mark_health_resolved(self, user_id: str):
        print(f"🔧 ADAPTER DEBUG: mark_health_resolved({user_id})")
        await self.storage.mark_health_resolved(user_id)


# Global instance
permanent_facts = PermanentFactsAdapter()
print("🎯 DEBUG: Global permanent_facts instance created")