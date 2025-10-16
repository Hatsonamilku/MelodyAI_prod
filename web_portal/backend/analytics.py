# analytics.py
from datetime import datetime, timedelta
import json

class Analytics:
    def __init__(self):
        self.message_stats = {
            "total_messages": 0,
            "web_messages": 0,
            "discord_messages": 0,
            "users": {},
            "hourly_activity": {},
            "daily_activity": {}
        }
        self.relationship_data = {}
    
    def track_message(self, message_data):
        """Track message statistics"""
        self.message_stats["total_messages"] += 1
        
        if message_data["source"] == "web":
            self.message_stats["web_messages"] += 1
        else:
            self.message_stats["discord_messages"] += 1
        
        # Track user activity
        user = message_data["user"]
        if user not in self.message_stats["users"]:
            self.message_stats["users"][user] = 0
        self.message_stats["users"][user] += 1
        
        # Track hourly activity
        hour = datetime.now().strftime("%H:00")
        if hour not in self.message_stats["hourly_activity"]:
            self.message_stats["hourly_activity"][hour] = 0
        self.message_stats["hourly_activity"][hour] += 1
        
        # Track daily activity
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.message_stats["daily_activity"]:
            self.message_stats["daily_activity"][today] = 0
        self.message_stats["daily_activity"][today] += 1
    
    def get_analytics(self):
        """Get comprehensive analytics"""
        return {
            "message_stats": self.message_stats,
            "top_users": sorted(
                self.message_stats["users"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            "activity_trends": {
                "hourly": dict(sorted(self.message_stats["hourly_activity"].items())),
                "daily": dict(sorted(self.message_stats["daily_activity"].items()))
            },
            "summary": {
                "total_messages": self.message_stats["total_messages"],
                "unique_users": len(self.message_stats["users"]),
                "web_ratio": round(
                    self.message_stats["web_messages"] / max(1, self.message_stats["total_messages"]) * 100, 
                    1
                ),
                "discord_ratio": round(
                    self.message_stats["discord_messages"] / max(1, self.message_stats["total_messages"]) * 100, 
                    1
                )
            }
        }

# Global analytics instance
analytics = Analytics()