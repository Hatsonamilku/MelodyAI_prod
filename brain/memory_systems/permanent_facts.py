# permanent_facts_universal.py
import json
import threading
import os
from datetime import datetime, timedelta
import re
from typing import List, Dict, Optional

class PermanentFacts:
    """Thread-safe, universal permanent facts storage with life events & health tracking."""

    def __init__(self, file_path: str = "permanent_facts.json"):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.data = {"users": {}}

        # Load existing data if available
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"users": {}}

    # --------------------------
    # Internal save
    # --------------------------
    def _save(self):
        with self.lock:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

    # --------------------------
    # Facts
    # --------------------------
    def add_fact(self, user_id: str, key: str, value: str,
                 category: str = "general", confidence: int = 1):
        """Add or update a fact for a user."""
        with self.lock:
            user_data = self.data["users"].setdefault(user_id, {})
            facts = user_data.setdefault("facts", [])

            # Check if fact exists
            for fact in facts:
                if fact["key"] == key and fact["category"] == category:
                    fact["value"] = value
                    fact["confidence"] = max(fact.get("confidence", 1), confidence)
                    fact["last_mentioned"] = datetime.now().isoformat()
                    fact["mention_count"] = fact.get("mention_count", 1) + 1
                    self._save()
                    return

            # Add new fact
            facts.append({
                "key": key,
                "value": value,
                "category": category,
                "confidence": confidence,
                "first_mentioned": datetime.now().isoformat(),
                "last_mentioned": datetime.now().isoformat(),
                "mention_count": 1
            })
            self._save()

    def search_facts(self, user_id: str, min_confidence: int = 1) -> List[tuple]:
        with self.lock:
            user_data = self.data["users"].get(user_id, {})
            facts = user_data.get("facts", [])
            return [
                (fact["category"], fact["key"], fact["value"])
                for fact in facts if fact.get("confidence", 1) >= min_confidence
            ]

    def get_all_facts(self, user_id: Optional[str] = None) -> Dict:
        with self.lock:
            if user_id:
                return self.data["users"].get(user_id, {}).get("facts", [])
            return self.data

    # --------------------------
    # Health
    # --------------------------
    def update_health(self, user_id: str, status: str, severity: int = 1):
        with self.lock:
            user_data = self.data["users"].setdefault(user_id, {})
            health = user_data.setdefault("health_status", [])
            follow_up = None
            if status.lower() == "sick":
                follow_up = (datetime.now() + timedelta(hours=24)).isoformat()
            health.append({
                "status": status,
                "severity": severity,
                "reported_at": datetime.now().isoformat(),
                "follow_up_scheduled": follow_up,
                "is_resolved": False
            })
            self._save()

    def check_health_follow_ups(self) -> List[tuple]:
        with self.lock:
            results = []
            now = datetime.now()
            for user_id, udata in self.data["users"].items():
                for entry in udata.get("health_status", []):
                    follow_up_time = entry.get("follow_up_scheduled")
                    if follow_up_time and not entry.get("is_resolved", False):
                        if datetime.fromisoformat(follow_up_time) < now:
                            results.append((user_id, entry["status"], entry["reported_at"]))
            return results

    def mark_health_resolved(self, user_id: str):
        with self.lock:
            user_data = self.data["users"].get(user_id, {})
            for entry in user_data.get("health_status", []):
                if not entry.get("is_resolved", False):
                    entry["is_resolved"] = True
            self._save()

    # --------------------------
    # Life Events
    # --------------------------
    def add_life_event(self, user_id: str, event_type: str,
                       details: str = "", importance: int = 1, event_date: Optional[str] = None):
        with self.lock:
            user_data = self.data["users"].setdefault(user_id, {})
            life_events = user_data.setdefault("life_events", [])
            if event_date is None:
                event_date = datetime.now().isoformat()
            life_events.append({
                "event_type": event_type,
                "details": details,
                "importance": importance,
                "event_date": event_date,
                "remembered_at": datetime.now().isoformat()
            })
            self._save()

# --------------------------
# Adapter for backward compatibility
# --------------------------
class PermanentFactsAdapter:
    """Adapter to match old orchestrator interface"""
    def __init__(self):
        self.storage = PermanentFacts()

    def extract_personal_facts(self, user_id: str, message: str) -> List[Dict]:
        """Extract personal facts from a message"""
        facts = []
        msg = message.lower()

        # Name
        name_match = re.search(r"(?:my name is|i'm called|call me) (\w+)", msg)
        if name_match:
            facts.append({"category": "personal", "key": "name", "value": name_match.group(1).title(), "confidence": 3})

        # Age
        age_match = re.search(r"(?:i am|i'm) (\d{1,3}) years? old", msg)
        if age_match:
            facts.append({"category": "personal", "key": "age", "value": age_match.group(1), "confidence": 3})

        # Location
        loc_match = re.search(r"(?:i live in|i'm from) ([^,.!?]+)", msg)
        if loc_match:
            facts.append({"category": "location", "key": "country", "value": loc_match.group(1).title(), "confidence": 2})

        # Favorite game
        games = ['league of legends','valorant','minecraft','genshin impact','overwatch','apex legends','fortnite']
        for game in games:
            if f"favorite game {game}" in msg:
                facts.append({"category":"gaming","key":"favorite_game","value":game.title(),"confidence":3})
                break

        # Favorite anime
        animes = ['one piece','naruto','attack on titan','demon slayer','jujutsu kaisen','my hero academia']
        for anime in animes:
            if f"favorite anime {anime}" in msg:
                facts.append({"category":"anime","key":"favorite_anime","value":anime.title(),"confidence":3})
                break

        # Health
        if "sick" in msg or "ill" in msg or "not feeling well" in msg:
            self.storage.update_health(user_id, "sick", 3)
        elif "better" in msg or "well" in msg or "good" in msg:
            self.storage.update_health(user_id, "recovered", 2)

        # Life events
        events = {
            "got married": "marriage",
            "graduated": "graduation",
            "new job": "new_job",
            "got hired": "new_job",
            "moving to": "relocation",
            "moved to": "relocation"
        }
        for phrase, evt in events.items():
            if phrase in msg:
                self.storage.add_life_event(user_id, evt)
                facts.append({"category":"life_events","key":evt,"value":"true","confidence":3})

        return facts

    def store_facts(self, user_id: str, facts: list):
        for fact in facts:
            self.storage.add_fact(
                user_id,
                fact['key'],
                fact['value'],
                fact.get('category', 'general'),
                fact.get('confidence', 1)
            )

    def get_user_context(self, user_id: str) -> str:
        facts = self.storage.search_facts(user_id, min_confidence=2)
        if not facts:
            return ""
        context = "📝 USER FACTS:\n"
        for category, key, value in facts[:5]:
            context += f"- {key.replace('_',' ').title()}: {value}\n"
        return context

    def check_health_follow_ups(self):
        return self.storage.check_health_follow_ups()

    def mark_health_resolved(self, user_id: str):
        self.storage.mark_health_resolved(user_id)

# Global instance
permanent_facts = PermanentFactsAdapter()
