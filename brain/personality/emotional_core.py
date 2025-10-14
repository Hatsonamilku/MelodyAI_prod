# melody_ai_v2/🧠 brain/personality/emotional_core.py
import re
import random
import statistics
from typing import Dict, Tuple

class EmotionalCore:
    def __init__(self):
        # Modern slang sets
        self.positive_slang = {
            'w', 'based', 'fire', 'goated', 'slay', 'king', 'queen', 'valid',
            'no cap', 'fr', 'real', 'absolute win', 'banger', 'hits different'
        }
        self.negative_slang = {
            'mid', 'trash', 'garbage', 'terrible', 'awful', 'bad', 'horrible',
            'boring', 'dumb', 'stupid', 'useless', 'worthless', 'lame', 'cringe',
            'skill issue', 'l bot', 'ratio', 'touch grass', 'copium', 'delulu'
        }

        # Traditional word sets
        self.positive_words = {
            'love', 'like', 'good', 'great', 'awesome', 'amazing', 'wonderful',
            'fantastic', 'excellent', 'perfect', 'happy', 'joy', 'pleased',
            'best', 'favorite', 'beautiful', 'brilliant', 'outstanding'
        }
        self.negative_words = {
            'hate', 'dislike', 'bad', 'terrible', 'awful', 'horrible', 'worst',
            'angry', 'sad', 'upset', 'disappointed', 'frustrated',
            'annoying', 'stupid', 'dumb', 'useless', 'boring'
        }

        # Emoji groups
        self.positive_emojis = {'❤️', '😂', '😍', '🥰', '👍', '✨', '😎', '🤩', '🥳', '😊', '🙌', '💖'}
        self.negative_emojis = {'😡', '😢', '💀', '👎', '🤬', '😞', '😔', '😠', '😭', '🤮', '☠️'}

        # Context helpers
        self.negations = {'not', "don't", "didn't", 'never', 'no', 'hardly'}
        self.sarcasm_clues = {'yeah right', 'sure jan', 'as if', 'totally', 'uh huh', 'whatever'}

        # Memory
        self.recent_sentiments = {}
        self.user_sentiment_history = {}

    # ---------------------------------------------------------
    # 🔍 SENTIMENT ANALYSIS
    # ---------------------------------------------------------
    def analyze_sentiment(self, text: str) -> Tuple[str, int]:
        """Enhanced sentiment analysis with slang, intensity, and emoji scaling."""
        if not text:
            return 'neutral', 0

        text_lower = text.lower()
        score = 0

        # Count exclamation and capitalization intensity
        exclamations = text.count('!')
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        intensity_boost = 1 + min(exclamations * 0.1 + caps_ratio * 2, 1.5)

        # Slang scoring
        for slang in self.positive_slang:
            if slang in text_lower:
                score += 3
        for slang in self.negative_slang:
            if slang in text_lower:
                score -= 3

        # Emoji scoring (scale with intensity)
        for char in text:
            if char in self.positive_emojis:
                score += 2 * intensity_boost
            elif char in self.negative_emojis:
                score -= 2 * intensity_boost

        # Word-based sentiment (with negation)
        words = re.findall(r'\b\w+\b', text_lower)
        for i, word in enumerate(words):
            word_score = 0
            if word in self.positive_words:
                word_score = 2
            elif word in self.negative_words:
                word_score = -2
            if i > 0 and words[i - 1] in self.negations:
                word_score = -word_score
            score += word_score

        # Sarcasm deduction (if positive + sarcasm clues)
        if any(clue in text_lower for clue in self.sarcasm_clues) and score > 0:
            score *= 0.5  # soft sarcasm
            score -= 2     # adds slight negativity

        # Cap and categorize
        score = max(-20, min(20, round(score)))
        if score >= 6:
            return 'positive', score
        elif score <= -6:
            return 'negative', score
        else:
            return 'neutral', score

    # ---------------------------------------------------------
    # ⚡ DYNAMIC CONTEXT
    # ---------------------------------------------------------
    def detect_emotional_whiplash(self, user_id: str, current_message: str) -> bool:
        """Detect mood swings within the last few messages."""
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
        return any(slang in text_lower for slang in self.positive_slang | self.negative_slang)

    def get_last_sentiment(self, user_id: str):
        return (self.user_sentiment_history.get(user_id) or [50])[-1]

    def store_sentiment(self, user_id: str, score: int):
        history = self.user_sentiment_history.setdefault(user_id, [])
        history.append(score)
        if len(history) > 10:
            history.pop(0)

    # ---------------------------------------------------------
    # 🧠 EMOTIONAL CONTEXT BUILDER
    # ---------------------------------------------------------
    def get_emotional_context(self, user_id: str, current_message: str) -> Dict:
        sentiment, raw_score = self.analyze_sentiment(current_message)
        base_score = 50 + (raw_score * 2.5)
        last_score = self.get_last_sentiment(user_id)
        whiplash = self.detect_emotional_whiplash(user_id, current_message)
        gen_alpha = self.contains_gen_alpha_vibes(current_message)

        # Smooth emotional transitions
        smoothed_score = (0.6 * base_score) + (0.4 * last_score)

        # Emotional baseline correction
        baseline = statistics.mean(self.user_sentiment_history.get(user_id, [50]))
        adjusted = smoothed_score + ((baseline - 50) * 0.1)

        # Mood stabilization
        final_score = max(0, min(100, int(adjusted)))
        toxicity_level = abs(raw_score) if raw_score <= -8 else 0

        self.store_sentiment(user_id, final_score)

        return {
            'sentiment': sentiment,
            'score': final_score,
            'raw_score': raw_score,
            'emotional_whiplash': whiplash,
            'gen_alpha_vibes': gen_alpha,
            'toxicity_level': toxicity_level
        }

# 🌐 Global instance
emotional_core = EmotionalCore()
