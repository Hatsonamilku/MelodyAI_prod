# predictive_analytics.py - AI-Powered Insights
import random
from datetime import datetime, timedelta
from collections import defaultdict

class PredictiveAnalytics:
    def __init__(self, analytics_ref):
        self.analytics = analytics_ref
        self.prediction_history = []
        
    def predict_relationship_trend(self, user):
        """Predict relationship trend for a user"""
        user_stats = self.analytics.user_stats.get(user, {})
        if not user_stats.get('emotional_trend'):
            return {
                'user': user,
                'trend': "📊 Gathering data...",
                'confidence': "Low",
                'predicted_score_change': 0,
                'next_milestone': "Need more interactions",
                'interaction_frequency': "Just getting started"
            }
        
        trends = user_stats['emotional_trend'][-10:]  # Last 10 interactions
        if len(trends) < 3:
            return {
                'user': user,
                'trend': "📈 Analyzing patterns...",
                'confidence': "Medium",
                'predicted_score_change': 5,
                'next_milestone': "Building connection",
                'interaction_frequency': "Establishing rhythm"
            }
        
        # Simple trend analysis
        recent_sentiments = [t['sentiment'] for t in trends]
        avg_sentiment = sum(recent_sentiments) / len(recent_sentiments)
        
        if avg_sentiment > 0.3:
            trend = "📈 Strong positive trend"
            confidence = "High"
            predicted_change = 15
        elif avg_sentiment > 0.1:
            trend = "↗️ Mild positive trend" 
            confidence = "Medium"
            predicted_change = 8
        elif avg_sentiment < -0.3:
            trend = "📉 Strong negative trend"
            confidence = "High"
            predicted_change = -12
        elif avg_sentiment < -0.1:
            trend = "↘️ Mild negative trend"
            confidence = "Medium"
            predicted_change = -6
        else:
            trend = "➡️ Stable trend"
            confidence = "Medium"
            predicted_change = 2
            
        return {
            'user': user,
            'trend': trend,
            'confidence': confidence,
            'predicted_score_change': predicted_change,
            'next_milestone': self.predict_next_milestone(user_stats),
            'interaction_frequency': self.analyze_interaction_pattern(user_stats)
        }
    
    def predict_next_milestone(self, user_stats):
        """Predict next relationship milestone"""
        score = user_stats.get('relationship_score', 50)
        milestones = {
            25: "🌱 First Connection",
            50: "💫 Meaningful Bond", 
            75: "⚡ Deep Connection",
            90: "🌌 Celestial Bond"
        }
        
        for threshold, milestone in sorted(milestones.items()):
            if score < threshold:
                points_needed = threshold - score
                return f"{milestone} ({points_needed} points away)"
        
        return "🏆 Maximum bond achieved!"
    
    def analyze_interaction_pattern(self, user_stats):
        """Analyze user interaction patterns"""
        if not user_stats.get('emotional_trend'):
            return "No pattern data yet"
            
        trends = user_stats['emotional_trend']
        if len(trends) < 5:
            return "Learning patterns..."
            
        # Simple pattern analysis
        positive_count = sum(1 for t in trends if t['sentiment'] > 0.1)
        negative_count = sum(1 for t in trends if t['sentiment'] < -0.1)
        
        positivity_ratio = positive_count / len(trends)
        
        if positivity_ratio > 0.7:
            return "😊 Highly positive interactions"
        elif positivity_ratio > 0.4:
            return "🙂 Balanced interactions"
        else:
            return "😐 Reserved interactions"
    
    def generate_weekly_forecast(self):
        """Generate weekly relationship forecast"""
        forecasts = [
            "This week will bring deeper connections and meaningful conversations. The cloud senses increased emotional resonance across all servers.",
            "Expect increased engagement and emotional depth in interactions. New bonds may form while existing ones strengthen.",
            "A week of stable growth and strengthening bonds. The digital ether hums with positive energy.",
            "New connections may form, existing ones will deepen. Look for unexpected moments of emotional resonance.",
            "Emotional intelligence will be key this week. The cloud predicts heightened sensitivity and understanding."
        ]
        return random.choice(forecasts)
    
    def get_engagement_heatmap(self):
        """Generate engagement heatmap data"""
        # Simulate engagement data for different times
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = list(range(24))
        
        heatmap_data = []
        for day in days:
            for hour in hours:
                # Simulate peak engagement during evening hours
                base_engagement = random.randint(1, 10)
                if 18 <= hour <= 22:  # Evening peak
                    base_engagement += random.randint(5, 15)
                elif 12 <= hour <= 14:  # Lunch peak
                    base_engagement += random.randint(2, 8)
                    
                heatmap_data.append({
                    'day': day,
                    'hour': hour,
                    'engagement': base_engagement
                })
                
        return heatmap_data

# Global instance
predictive_analytics = None

def setup_predictive_analytics(analytics_ref):
    global predictive_analytics
    predictive_analytics = PredictiveAnalytics(analytics_ref)
    return predictive_analytics