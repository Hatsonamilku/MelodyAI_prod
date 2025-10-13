# melody_ai_v2/🧠 brain/personality/emotional_core.py
import re
import random
from typing import Dict, List, Tuple

class EmotionalCore:
    def __init__(self):
        # Modern slang sentiment detection
        self.positive_slang = {
            'w', 'based', 'fire', 'goated', 'slay', 'king', 'queen', 'valid',
            'no cap', 'fr', 'real', 'absolute win', 'banger', 'hits different'
        }
        
        self.negative_slang = {
            'mid', 'trash', 'garbage', 'terrible', 'awful', 'bad', 'horrible',
            'boring', 'dumb', 'stupid', 'useless', 'worthless', 'lame', 'cringe',
            'skill issue', 'l bot', 'ratio', 'touch grass', 'copium', 'delulu'
        }
        
        # Traditional sentiment words
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
        
        # Emoji sentiment
        self.positive_emojis = {'❤️', '😂', '😍', '🥰', '👍', '✨', '😎', '🤩', '🥳', '😊', '🙌'}
        self.negative_emojis = {'😡', '😢', '💀', '👎', '🤬', '😞', '😔', '😠', '😭', '🤮'}
        
        # Negation handling
        self.negations = {'not', "don't", "didn't", 'never', 'no', 'hardly'}
        
        # Emotional whiplash detection
        self.emotional_keywords = ['love', 'hate', 'angry', 'happy', 'sad', 'excited', 'disappointed']
        self.recent_sentiments = {}

    def analyze_sentiment(self, text: str) -> Tuple[str, int]:
        """Advanced sentiment analysis with modern slang support"""
        if not text:
            return 'neutral', 0
            
        text_lower = text.lower()
        score = 0
        
        # Modern slang scoring
        for slang in self.positive_slang:
            if slang in text_lower:
                score += 2
                
        for slang in self.negative_slang:
            if slang in text_lower:
                score -= 2
        
        # Emoji scoring
        for char in text:
            if char in self.positive_emojis:
                score += 1
            elif char in self.negative_emojis:
                score -= 1
        
        # Traditional word scoring with negation handling
        words = re.findall(r'\b\w+\b', text_lower)
        for i, word in enumerate(words):
            word_score = 0
            if word in self.positive_words:
                word_score = 1
            elif word in self.negative_words:
                word_score = -1
            
            # Check for negation
            if i > 0 and words[i-1] in self.negations:
                word_score = -word_score  # Flip sentiment
            
            score += word_score
        
        # Cap the score
        score = max(-10, min(10, score))
        
        # Determine category
        if score >= 3:
            return 'positive', score
        elif score <= -3:
            return 'negative', score
        else:
            return 'neutral', score

    def detect_emotional_whiplash(self, user_id: str, current_message: str) -> bool:
        """Detect rapid emotional changes in conversation"""
        if user_id not in self.recent_sentiments:
            self.recent_sentiments[user_id] = []
        
        current_sentiment, current_score = self.analyze_sentiment(current_message)
        
        # Store current sentiment
        self.recent_sentiments[user_id].append((current_sentiment, current_score))
        
        # Keep only last 5 sentiments
        if len(self.recent_sentiments[user_id]) > 5:
            self.recent_sentiments[user_id] = self.recent_sentiments[user_id][-5:]
        
        # Check for whiplash (rapid changes between positive/negative)
        if len(self.recent_sentiments[user_id]) >= 3:
            sentiments = [s[0] for s in self.recent_sentiments[user_id][-3:]]
            changes = sum(1 for i in range(1, len(sentiments)) 
                       if sentiments[i] != sentiments[i-1])
            
            # Whiplash if more than 1 change in last 3 messages
            return changes >= 2
        
        return False

    def contains_gen_alpha_vibes(self, text: str) -> bool:
        """Check if message contains Gen Alpha slang"""
        text_lower = text.lower()
        return any(slang in text_lower for slang in self.positive_slang.union(self.negative_slang))

    def get_emotional_context(self, user_id: str, current_message: str) -> Dict:
        """Get comprehensive emotional context for response generation"""
        sentiment, score = self.analyze_sentiment(current_message)
        whiplash = self.detect_emotional_whiplash(user_id, current_message)
        gen_alpha = self.contains_gen_alpha_vibes(current_message)
        
        return {
            'sentiment': sentiment,
            'score': score,
            'emotional_whiplash': whiplash,
            'gen_alpha_vibes': gen_alpha,
            'toxicity_level': abs(score) if score < -5 else 0
        }

# Global instance
emotional_core = EmotionalCore()