# ==========================================================
# 🧠 melody_ai_v2/brain/personality/emotional_core.py
# ----------------------------------------------------------
# MelodyAI Emotional Core v3.0 - WITH ROAST DEFENSE MECHANISM
# Semantic + Predictable Extremes + Gen Alpha slang + Reduced Smoothing + Roast Defense
# ==========================================================

import re
import statistics
from typing import Dict, List, Tuple

class EmotionalCore:
    """Advanced emotional reasoning system for MelodyAI v3.0 with roast defense."""
    
    def __init__(self):
        # ----------------------------
        # 🎯 MODERN SLANG VOCABULARY
        # ----------------------------
        self.positive_slang = {
            'w', 'based', 'fire', 'goated', 'slay', 'king', 'queen', 'valid', 'no cap', 'fr', 'real',
            'absolute win', 'banger', 'hits different', 'peak', 'vibe', 'cooking', 'clean', 'chill', 'sigma', 'alpha'
        }
        
        self.negative_slang = {
            'mid', 'trash', 'garbage', 'terrible', 'awful', 'bad', 'horrible', 'boring', 'dumb', 'stupid',
            'useless', 'worthless', 'lame', 'cringe', 'skill issue', 'l bot', 'ratio', 'touch grass',
            'copium', 'delulu', 'malding', 'cry about it', 'down bad'
        }
        
        # ----------------------------
        # 💬 TRADITIONAL WORD SETS
        # ----------------------------
        self.positive_words = {
            'love', 'like', 'good', 'great', 'awesome', 'amazing', 'wonderful', 'fantastic', 'excellent',
            'perfect', 'happy', 'joy', 'pleased', 'best', 'favorite', 'beautiful', 'brilliant', 'outstanding',
            'fun', 'cool', 'sweet', 'cute'
        }
        
        self.negative_words = {
            'hate', 'dislike', 'bad', 'terrible', 'awful', 'horrible', 'worst', 'angry', 'sad', 'upset',
            'disappointed', 'frustrated', 'annoying', 'stupid', 'dumb', 'useless', 'boring', 'disgusting', 'gross'
        }
        
        # ----------------------------
        # 😃 EMOJI SENTIMENTS
        # ----------------------------
        self.positive_emojis = {'❤️', '😂', '😍', '🥰', '👍', '✨', '😎', '🤩', '🥳', '😊', '🙌', '💖', '💪'}
        self.negative_emojis = {'😡', '😢', '💀', '👎', '🤬', '😞', '😔', '😠', '😭', '🤮', '☠️', '😤', '😩'}
        
        # ----------------------------
        # 🧩 CONTEXT HELPERS
        # ----------------------------
        self.negations = {'not', "don't", "didn't", 'never', 'no', 'hardly', 'rarely', "can't"}
        self.sarcasm_clues = {'yeah right', 'sure jan', 'as if', 'totally', 'uh huh', 'whatever', 'ok buddy', 'lmao sure'}
        
        # 🎯 ROAST DEFENSE TRIGGERS
        self.personal_attacks = {
            'fake', 'worst', 'suck', 'trash', 'garbage', 'useless', 'stupid', 'ugly', 'dumb', 'shit', 'bitch',
            'annoying', 'cringe', 'lame', 'pathetic', 'worthless', 'terrible', 'awful', 'horrible', 'disgusting'
        }
        
        # ----------------------------
        # 🧠 MEMORY SYSTEM
        # ----------------------------
        self.recent_sentiments: Dict[str, List[Tuple[str, int]]] = {}
        self.user_sentiment_history: Dict[str, List[int]] = {}
        self.user_trust_scores: Dict[str, float] = {}
        self.user_interaction_count: Dict[str, int] = {}
        self.user_mood_baseline: Dict[str, int] = {}
        self.user_attack_history: Dict[str, List[str]] = {}  # Track repeated attacks
        
        # 🧮 Precompiled patterns for speed
        self.word_splitter = re.compile(r'\b\w+\b')

    # ==========================================================
    # 🔍 SENTIMENT ANALYSIS
    # ==========================================================
    def analyze_sentiment(self, text: str) -> Tuple[str, int]:
        text_lower = text.lower()
        words = self.word_splitter.findall(text_lower)
        score = 0
        intensity_boost = 1.0 + (len(text) / 120)
        
        # Slang
        for slang in self.positive_slang:
            if slang in text_lower:
                score += 8
                
        for slang in self.negative_slang:
            if slang in text_lower:
                score -= 8
                
        # Emojis
        for char in text:
            if char in self.positive_emojis:
                score += 5 * intensity_boost
            elif char in self.negative_emojis:
                score -= 5 * intensity_boost
                
        # Words + negations
        for i, word in enumerate(words):
            word_score = 0
            if word in self.positive_words:
                word_score = 4
            elif word in self.negative_words:
                word_score = -4
                
            if i > 0 and words[i - 1] in self.negations:
                word_score *= -1.2
                
            score += word_score
            
        # Sarcasm
        if any(phrase in text_lower for phrase in self.sarcasm_clues):
            score *= -0.5
            
        # Clamp raw score
        score = max(-40, min(40, round(score)))
        
        if score >= 12:
            return 'positive', score
        elif score <= -12:
            return 'negative', score
        return 'neutral', score

    # ==========================================================
    # ⚡ CONTEXT DETECTION
    # ==========================================================
    def detect_emotional_whiplash(self, user_id: str, current_message: str) -> bool:
        sentiment, score = self.analyze_sentiment(current_message)
        self.recent_sentiments.setdefault(user_id, []).append((sentiment, score))
        self.recent_sentiments[user_id] = self.recent_sentiments[user_id][-5:]
        
        if len(self.recent_sentiments[user_id]) >= 3:
            recent = [s[0] for s in self.recent_sentiments[user_id][-3:]]
            changes = sum(1 for i in range(1, len(recent)) if recent[i] != recent[i - 1])
            return changes >= 2
            
        return False

    def contains_gen_alpha_vibes(self, text: str) -> bool:
        text_lower = text.lower()
        return any(slang in text_lower for slang in (self.positive_slang | self.negative_slang))

    # ==========================================================
    # 💾 MEMORY + RELATIONSHIP
    # ==========================================================
    def get_last_sentiment(self, user_id: str):
        return (self.user_sentiment_history.get(user_id) or [50])[-1]

    def store_sentiment(self, user_id: str, score: int):
        history = self.user_sentiment_history.setdefault(user_id, [])
        history.append(score)
        if len(history) > 15:
            history.pop(0)
            
        self.user_interaction_count[user_id] = self.user_interaction_count.get(user_id, 0) + 1
        self.user_mood_baseline[user_id] = score

    def calculate_trust_score(self, user_id: str) -> float:
        history = self.user_sentiment_history.get(user_id, [])
        if not history:
            return 0
            
        positive_count = sum(1 for s in history if s > 60)
        ratio = positive_count / len(history)
        consistency = 100 - statistics.pstdev(history) if len(history) > 3 else 60
        duration_bonus = min(len(history) * 2, 30)
        
        trust = (ratio * 60) + (consistency * 0.2) + duration_bonus
        trust_score = max(0, min(100, trust))
        self.user_trust_scores[user_id] = trust_score
        return trust_score

    # ==========================================================
    # 🧃 SOCIAL INTELLIGENCE - ENHANCED ROAST DEFENSE
    # ==========================================================
    def is_friendly_banter(self, user_id: str, raw_score: int, message: str) -> bool:
        trust = self.calculate_trust_score(user_id)
        playful_words = {'game', 'music', 'playlist', 'fortnite', 'suck at', 'bad at', 'terrible', 'noob', 'lol', 'lmao', 'xd'}
        return trust > 80 and -15 <= raw_score <= -5 and any(w in message.lower() for w in playful_words)

    def should_activate_roast_defense(self, user_id: str, raw_score: int, message: str) -> bool:
        """Enhanced roast defense with attack severity detection"""
        trust = self.calculate_trust_score(user_id)
        interactions = self.user_interaction_count.get(user_id, 0)
        
        # Detect personal attacks
        is_attack = any(p in message.lower() for p in self.personal_attacks)
        attack_severity = self._calculate_attack_severity(message)
        
        # Track attack history
        if is_attack:
            self.user_attack_history.setdefault(user_id, []).append(message)
            if len(self.user_attack_history[user_id]) > 5:
                self.user_attack_history[user_id] = self.user_attack_history[user_id][-5:]
        
        # 🎯 ROAST DEFENSE CONDITIONS:
        # 1. New user (low interactions) OR low trust
        # 2. Highly negative sentiment
        # 3. Contains personal attacks
        # 4. Not friendly banter
        return ((trust < 30 or interactions < 3) and 
                raw_score <= -8 and 
                is_attack and 
                attack_severity >= 2 and
                not self.is_friendly_banter(user_id, raw_score, message))

    def _calculate_attack_severity(self, message: str) -> int:
        """Calculate how severe the personal attack is"""
        severity = 0
        message_lower = message.lower()
        
        # Mild attacks (1 point)
        mild_attacks = {'bad', 'suck', 'lame', 'cringe', 'annoying'}
        if any(attack in message_lower for attack in mild_attacks):
            severity += 1
            
        # Medium attacks (2 points)
        medium_attacks = {'trash', 'garbage', 'stupid', 'dumb', 'useless', 'worst'}
        if any(attack in message_lower for attack in medium_attacks):
            severity += 2
            
        # Severe attacks (3 points)
        severe_attacks = {'fake', 'pathetic', 'worthless', 'disgusting', 'ugly', 'shit', 'bitch'}
        if any(attack in message_lower for attack in severe_attacks):
            severity += 3
            
        return severity

    def get_roast_defense_level(self, user_id: str, message: str) -> str:
        """Determine appropriate roast defense level"""
        trust = self.calculate_trust_score(user_id)
        interactions = self.user_interaction_count.get(user_id, 0)
        attack_history = self.user_attack_history.get(user_id, [])
        attack_severity = self._calculate_attack_severity(message)
        
        # 🎯 DEFENSE LEVELS:
        if len(attack_history) >= 3:  # Repeat offender
            return "DOMINANT"
        elif attack_severity >= 3:  # Severe attack
            return "AGGRESSIVE" 
        elif trust < 15 or interactions == 1:  # Brand new hostile user
            return "HUMOROUS_DISMISSAL"
        else:  # Mild attack from low-trust user
            return "SKILL_ROAST"

    # ==========================================================
    # 🧠 EMOTIONAL CONTEXT BUILDER (v3.0 WITH ROAST DEFENSE)
    # ==========================================================
    def get_emotional_context(self, user_id: str, current_message: str) -> Dict:
        sentiment, raw_score = self.analyze_sentiment(current_message)
        trust = self.calculate_trust_score(user_id)
        is_banter = self.is_friendly_banter(user_id, raw_score, current_message)
        roast_defense = self.should_activate_roast_defense(user_id, raw_score, current_message)
        roast_defense_level = self.get_roast_defense_level(user_id, current_message) if roast_defense else None
        
        adjusted_raw = raw_score * (0.5 if is_banter else 1.0)
        
        # 🚀 PREDICTABLE EXTREMES MAPPING
        extremes_triggered = None
        if adjusted_raw <= -12:
            base_score = 15
            extremes_triggered = 'COLD EXTREME'
        elif adjusted_raw >= 25:
            base_score = 95  
            extremes_triggered = 'AFFECTION EXTREME'
        else:
            base_score = 50 + (adjusted_raw * 2)
            
        # 🚀 REDUCED SMOOTHING TO LET EXTREMES SHINE
        baseline = self.user_mood_baseline.get(user_id, 50)
        weight = 0.9 if abs(adjusted_raw) >= 12 else 0.95
        smoothed = int((weight * base_score) + ((1 - weight) * baseline))
        final_score = max(0, min(100, smoothed))
        
        # Clamp for banter / roast defense
        if is_banter and final_score < 35:
            final_score = 35
        if roast_defense and final_score > 70:
            final_score = 70
            
        self.store_sentiment(user_id, final_score)
        
        extremes_info = f" | EXTREMES={extremes_triggered}" if extremes_triggered else ""
        roast_info = f" | ROAST_DEFENSE={roast_defense_level}" if roast_defense else ""
        
        print(f"🎭 Emotional Debug | User={user_id} | Raw={raw_score} | Final={final_score} | "
              f"Trust={trust:.1f} | Banter={is_banter} | Defense={roast_defense}{roast_info}{extremes_info}")
        
        return {
            'sentiment': sentiment,
            'score': final_score,
            'raw_score': raw_score,
            'emotional_whiplash': self.detect_emotional_whiplash(user_id, current_message),
            'gen_alpha_vibes': self.contains_gen_alpha_vibes(current_message),
            'toxicity_level': abs(raw_score) if raw_score <= -8 else 0,
            'trust_score': trust,
            'is_friendly_banter': is_banter,
            'should_roast_defense': roast_defense,
            'roast_defense_level': roast_defense_level,
            'interaction_count': self.user_interaction_count.get(user_id, 0),
            'extremes_triggered': extremes_triggered,
            'attack_severity': self._calculate_attack_severity(current_message) if roast_defense else 0
        }
        
    def get_emotional_state(self, user_id: str) -> Dict[str, any]:
        """Get current emotional state for a user"""
        return {
            'trust_score': self.calculate_trust_score(user_id),
            'interaction_count': self.user_interaction_count.get(user_id, 0),
            'recent_sentiments': self.user_sentiment_history.get(user_id, [])[-5:],
            'mood_baseline': self.user_mood_baseline.get(user_id, 50),
            'attack_history': len(self.user_attack_history.get(user_id, []))
        }

# 🌐 Global Singleton
emotional_core = EmotionalCore()