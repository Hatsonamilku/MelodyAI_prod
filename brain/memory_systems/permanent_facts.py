# melody_ai_v2/🧠 brain/memory_systems/permanent_facts.py
import sqlite3
import datetime
import re
from typing import List, Dict, Optional

class PermanentFactsSystem:
    def __init__(self, db_path='melody_memory.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup_tables()
    
    def _setup_tables(self):
        """Create tables for permanent user facts"""
        cursor = self.conn.cursor()
        
        # Main user facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_permanent_facts (
                user_id TEXT,
                category TEXT,
                fact_key TEXT,
                fact_value TEXT,
                confidence_score INTEGER DEFAULT 1,
                first_mentioned TEXT,
                last_mentioned TEXT,
                mention_count INTEGER DEFAULT 1,
                source_message TEXT,
                is_verified BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (user_id, category, fact_key)
            )
        ''')
        
        # Health tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_health_status (
                user_id TEXT,
                status TEXT,
                severity INTEGER DEFAULT 1,
                reported_at TEXT,
                follow_up_scheduled TEXT,
                is_resolved BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (user_id, reported_at)
            )
        ''')
        
        # Life events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_life_events (
                user_id TEXT,
                event_type TEXT,
                event_date TEXT,
                details TEXT,
                importance INTEGER DEFAULT 1,
                remembered_at TEXT,
                PRIMARY KEY (user_id, event_type, event_date)
            )
        ''')
        
        self.conn.commit()
        print("✅ Permanent Facts System initialized!")

    def extract_personal_facts(self, user_id: str, message: str) -> List[Dict]:
        """Extract personal facts from user messages with high confidence patterns"""
        facts = []
        message_lower = message.lower()
        
        # 🔍 NAME EXTRACTION (High Confidence)
        name_patterns = [
            (r'(?:my name is|i\'m called|call me) (\w+)', 3),
            (r'(?:i am|i\'m) (\w+)(?:\s|$)', 2),
        ]
        
        for pattern, confidence in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).title()
                facts.append({
                    'category': 'personal',
                    'key': 'name',
                    'value': name,
                    'confidence': confidence,
                    'source': message
                })
                break
        
        # 🎂 AGE EXTRACTION (High Confidence)
        age_patterns = [
            (r'(?:i am|i\'m) (\d{1,3}) years? old', 3),
            (r'my age is (\d{1,3})', 3),
            (r'i just turned (\d{1,3})', 3),
        ]
        
        for pattern, confidence in age_patterns:
            match = re.search(pattern, message_lower)
            if match:
                age = match.group(1)
                if 1 <= int(age) <= 120:
                    facts.append({
                        'category': 'personal',
                        'key': 'age',
                        'value': age,
                        'confidence': confidence,
                        'source': message
                    })
                break
        
        # 🌍 COUNTRY/LOCATION (Medium Confidence)
        location_patterns = [
            (r'(?:i live in|i\'m from) ([^,.!?]+)', 2),
            (r'(?:based in|located in) ([^,.!?]+)', 2),
        ]
        
        for pattern, confidence in location_patterns:
            match = re.search(pattern, message_lower)
            if match:
                location = match.group(1).strip().title()
                if len(location) > 2:
                    facts.append({
                        'category': 'location',
                        'key': 'country',
                        'value': location,
                        'confidence': confidence,
                        'source': message
                    })
                break
        
        # 🎮 FAVORITE GAMES (High Confidence when explicit)
        game_keywords = {
            'league of legends': 'League of Legends',
            'valorant': 'Valorant',
            'minecraft': 'Minecraft',
            'genshin impact': 'Genshin Impact',
            'overwatch': 'Overwatch',
            'apex legends': 'Apex Legends',
            'fortnite': 'Fortnite'
        }
        
        if 'favorite game' in message_lower:
            for game_key, game_name in game_keywords.items():
                if game_key in message_lower:
                    facts.append({
                        'category': 'gaming',
                        'key': 'favorite_game',
                        'value': game_name,
                        'confidence': 3,
                        'source': message
                    })
                    break
        
        # 📺 FAVORITE ANIME (High Confidence when explicit)
        anime_keywords = {
            'one piece': 'One Piece',
            'naruto': 'Naruto',
            'attack on titan': 'Attack on Titan',
            'demon slayer': 'Demon Slayer',
            'jujutsu kaisen': 'Jujutsu Kaisen',
            'my hero academia': 'My Hero Academia'
        }
        
        if 'favorite anime' in message_lower:
            for anime_key, anime_name in anime_keywords.items():
                if anime_key in message_lower:
                    facts.append({
                        'category': 'anime',
                        'key': 'favorite_anime',
                        'value': anime_name,
                        'confidence': 3,
                        'source': message
                    })
                    break
        
        # 🏥 HEALTH STATUS (High Confidence)
        health_patterns = [
            (r'(?:i am|i\'m) (sick|ill|not feeling well)', 'sick', 3),
            (r'(?:have|got) (covid|flu|cold)', 'sick', 3),
            (r'feeling (better|well|good)', 'recovered', 2),
        ]
        
        for pattern, status, confidence in health_patterns:
            if re.search(pattern, message_lower):
                self._update_health_status(user_id, status, confidence)
                break
        
        # 💍 LIFE EVENTS (High Confidence)
        life_event_patterns = [
            (r'(?:got|getting) married', 'marriage', 3),
            (r'(?:graduated|graduation)', 'graduation', 3),
            (r'(?:new job|got hired)', 'new_job', 3),
            (r'(?:moving to|moved to) (\w+)', 'relocation', 2),
        ]
        
        for pattern, event_type, confidence in life_event_patterns:
            if re.search(pattern, message_lower):
                facts.append({
                    'category': 'life_events',
                    'key': event_type,
                    'value': 'true',
                    'confidence': confidence,
                    'source': message
                })
                break
        
        return facts

    def _update_health_status(self, user_id: str, status: str, severity: int):
        """Update user health status and schedule follow-up"""
        cursor = self.conn.cursor()
        
        # Schedule follow-up if sick
        follow_up = None
        if status == 'sick':
            follow_up = (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()
        
        cursor.execute('''
            INSERT INTO user_health_status 
            (user_id, status, severity, reported_at, follow_up_scheduled)
            VALUES (?, ?, ?, datetime('now'), ?)
        ''', (user_id, status, severity, follow_up))
        
        self.conn.commit()

    def store_facts(self, user_id: str, facts: List[Dict]):
        """Store extracted facts with confidence-based merging"""
        cursor = self.conn.cursor()
        
        for fact in facts:
            cursor.execute('''
                SELECT fact_value, mention_count, confidence_score
                FROM user_permanent_facts 
                WHERE user_id = ? AND category = ? AND fact_key = ?
            ''', (user_id, fact['category'], fact['key']))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing fact - use higher confidence value
                existing_value, mention_count, old_confidence = existing
                new_confidence = max(old_confidence, fact.get('confidence', 1))
                
                cursor.execute('''
                    UPDATE user_permanent_facts 
                    SET mention_count = mention_count + 1,
                        last_mentioned = datetime('now'),
                        confidence_score = ?
                    WHERE user_id = ? AND category = ? AND fact_key = ?
                ''', (new_confidence, user_id, fact['category'], fact['key']))
                
            else:
                # Insert new fact
                cursor.execute('''
                    INSERT INTO user_permanent_facts 
                    (user_id, category, fact_key, fact_value, confidence_score, 
                     first_mentioned, last_mentioned, mention_count, source_message)
                    VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'), 1, ?)
                ''', (user_id, fact['category'], fact['key'], fact['value'], 
                      fact.get('confidence', 1), fact.get('source', '')))
        
        self.conn.commit()

    def get_user_context(self, user_id: str) -> str:
        """Get comprehensive user context for AI responses"""
        cursor = self.conn.cursor()
        
        # Get high-confidence facts
        cursor.execute('''
            SELECT category, fact_key, fact_value, confidence_score
            FROM user_permanent_facts 
            WHERE user_id = ? AND confidence_score >= 2
            ORDER BY confidence_score DESC, mention_count DESC
        ''', (user_id,))
        
        facts = cursor.fetchall()
        
        # Get current health status
        cursor.execute('''
            SELECT status, reported_at 
            FROM user_health_status 
            WHERE user_id = ? AND is_resolved = FALSE
            ORDER BY reported_at DESC LIMIT 1
        ''', (user_id,))
        
        health_status = cursor.fetchone()
        
        # Build context string
        context_parts = []
        
        if facts:
            context_parts.append("📝 USER FACTS:")
            for category, key, value, confidence in facts[:8]:  # Limit to 8 facts
                context_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        if health_status:
            status, reported_at = health_status
            context_parts.append(f"🏥 HEALTH: Currently {status} (since {reported_at[:10]})")
        
        return "\n".join(context_parts) if context_parts else ""

    def check_health_follow_ups(self) -> List[tuple]:
        """Check for health follow-ups needed"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_id, status, reported_at 
            FROM user_health_status 
            WHERE follow_up_scheduled < datetime('now') 
            AND is_resolved = FALSE
        ''')
        
        return cursor.fetchall()

    def mark_health_resolved(self, user_id: str):
        """Mark user's health issue as resolved"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE user_health_status 
            SET is_resolved = TRUE 
            WHERE user_id = ? AND is_resolved = FALSE
        ''', (user_id,))
        self.conn.commit()

# Global instance
permanent_facts = PermanentFactsSystem()