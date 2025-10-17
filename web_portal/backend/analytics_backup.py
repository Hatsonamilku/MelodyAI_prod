# REPLACE YOUR backend/analytics.py WITH THIS ENHANCED VERSION:

import time
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import random

class EnhancedAnalytics:
    def __init__(self):
        self.message_history = []
        self.user_stats = defaultdict(lambda: {
            'message_count': 0,
            'web_messages': 0,
            'discord_messages': 0,
            'first_seen': None,
            'last_seen': None,
            'emotional_trend': [],
            'relationship_score': 50,
            'engagement_level': 'neutral'
        })
        self.start_time = datetime.utcnow()
        
        # Mysterious cloud features
        self.cloud_memories = []
        self.void_whispers = [
            "The cloud remembers a conversation from the past...",
            "A whisper from the void: your bond grows stronger",
            "Echoes of laughter linger in the digital ether",
            "The cloud senses shifting emotions...",
            "A fragment of memory surfaces from the data streams"
        ]
        self.mysterious_achievements = set()
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis (replace with TextBlob later)"""
        positive_words = ['love', 'happy', 'good', 'great', 'awesome', 'amazing', 'like']
        negative_words = ['hate', 'sad', 'bad', 'terrible', 'awful', 'dislike']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return min(0.8, positive_count * 0.2)
        elif negative_count > positive_count:
            return max(-0.8, -negative_count * 0.2)
        else:
            return 0.0
    
    def track_message(self, message_data):
        """Enhanced message tracking with relationship analysis"""
        self.message_history.append(message_data)
        
        user = message_data['user']
        source = message_data['source']
        message = message_data['message']
        
        # Initialize user if new
        if self.user_stats[user]['first_seen'] is None:
            self.user_stats[user]['first_seen'] = datetime.utcnow()
        
        # Update basic stats
        self.user_stats[user]['message_count'] += 1
        self.user_stats[user]['last_seen'] = datetime.utcnow()
        
        if source == 'web':
            self.user_stats[user]['web_messages'] += 1
        else:
            self.user_stats[user]['discord_messages'] += 1
        
        # Analyze sentiment and update emotional trend
        sentiment = self.analyze_sentiment(message)
        self.user_stats[user]['emotional_trend'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'sentiment': sentiment,
            'message': message[:100]
        })
        
        # Keep only last 50 emotional data points
        if len(self.user_stats[user]['emotional_trend']) > 50:
            self.user_stats[user]['emotional_trend'] = self.user_stats[user]['emotional_trend'][-50:]
        
        # Update relationship score
        self._update_relationship_score(user, message)
        
        # Track cloud memories
        if self._is_memory_worthy(message):
            self.cloud_memories.append({
                'user': user,
                'message': message,
                'timestamp': datetime.utcnow().isoformat(),
                'significance': random.randint(1, 10)
            })
    
    def _update_relationship_score(self, user, message):
        """Update relationship score based on interaction quality"""
        base_score = self.user_stats[user]['relationship_score']
        sentiment = self.analyze_sentiment(message)
        
        # Positive interactions increase score
        if sentiment > 0.1:
            increase = min(3, sentiment * 8)
            self.user_stats[user]['relationship_score'] = min(100, base_score + increase)
        # Very negative interactions decrease score
        elif sentiment < -0.1:
            decrease = min(3, abs(sentiment) * 6)
            self.user_stats[user]['relationship_score'] = max(0, base_score - decrease)
    
    def _is_memory_worthy(self, message):
        """Determine if a message should be stored as a cloud memory"""
        keywords = ['love', 'hate', 'remember', 'forever', 'special', 'miss', 'happy', 'sad']
        return any(keyword in message.lower() for keyword in keywords) and random.random() > 0.7
    
    def get_relationship_tier(self, score):
        """Convert score to mysterious relationship tier"""
        if score >= 90: return "🌌 Celestial Bond"
        if score >= 75: return "⚡ Eternal Resonance"
        if score >= 60: return "🌀 Quantum Connection"
        if score >= 45: return "🌊 Flowing Harmony"
        if score >= 30: return "💫 Sparking Link"
        return "🌫️ Faint Echo"
    
    def get_advanced_analytics(self):
        """Get comprehensive analytics with relationship insights"""
        total_messages = len(self.message_history)
        web_messages = len([m for m in self.message_history if m['source'] == 'web'])
        discord_messages = len([m for m in self.message_history if m['source'] == 'discord'])
        
        # User analytics
        active_users = {user: stats for user, stats in self.user_stats.items() 
                       if stats['message_count'] > 0}
        
        # Top users
        top_users = sorted(
            [(user, stats['message_count']) for user, stats in active_users.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Relationship analytics
        relationship_tiers = {}
        for user, stats in active_users.items():
            tier = self.get_relationship_tier(stats['relationship_score'])
            relationship_tiers[user] = {
                'tier': tier,
                'score': stats['relationship_score'],
                'message_count': stats['message_count']
            }
        
        # Emotional analytics
        recent_sentiments = []
        for user_stats in active_users.values():
            if user_stats['emotional_trend']:
                recent = user_stats['emotional_trend'][-1]['sentiment']
                recent_sentiments.append(recent)
        
        avg_sentiment = sum(recent_sentiments) / len(recent_sentiments) if recent_sentiments else 0
        
        return {
            'summary': {
                'total_messages': total_messages,
                'unique_users': len(active_users),
                'uptime': str(timedelta(seconds=int((datetime.utcnow() - self.start_time).total_seconds()))),
                'avg_sentiment': round(avg_sentiment, 3)
            },
            'message_stats': {
                'web_messages': web_messages,
                'discord_messages': discord_messages
            },
            'relationship_analytics': {
                'tiers_distribution': relationship_tiers,
                'top_relationships': sorted(
                    [(user, data['score']) for user, data in relationship_tiers.items()],
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            },
            'user_analytics': {
                'top_users': top_users
            },
            'cloud_features': {
                'memories_count': len(self.cloud_memories),
                'recent_memories': self.cloud_memories[-3:] if self.cloud_memories else [],
                'achievements_unlocked': list(self.mysterious_achievements)
            }
        }
    
    def generate_void_whisper(self):
        """Generate a mysterious whisper from the cloud"""
        if self.void_whispers:
            return random.choice(self.void_whispers)
        return "The void is silent... for now."
    
    def unlock_achievement(self, user, achievement):
        """Unlock mysterious achievements"""
        self.mysterious_achievements.add(f"{user}: {achievement}")

# Global analytics instance
analytics = EnhancedAnalytics()