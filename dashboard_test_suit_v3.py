# dashboard.py
import asyncio
import aiohttp
from aiohttp import web
import json
import sqlite3
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.utils
import jinja2
import aiohttp_jinja2

class MelodyAIDashboard:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        self.setup_jinja2()
        
    def setup_jinja2(self):
        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader('templates'))
    
    def setup_routes(self):
        self.app.router.add_get('/', self.dashboard)
        self.app.router.add_get('/api/relationships', self.api_relationships)
        self.app.router.add_get('/api/facts', self.api_facts)
        self.app.router.add_get('/api/conversations', self.api_conversations)
        self.app.router.add_get('/api/stats', self.api_stats)
        self.app.router.add_static('/static', 'static')
    
    def get_db_connection(self):
        """Get connection to melody_memory.db"""
        return sqlite3.connect('melody_memory.db')
    
    def load_relationship_data(self):
        """Load relationship data from JSON file"""
        try:
            if os.path.exists('relationship_data.json'):
                with open('relationship_data.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading relationship data: {e}")
        return {}
    
    @aiohttp_jinja2.template('dashboard.html')
    async def dashboard(self, request):
        return {}
    
    async def api_relationships(self, request):
        """API endpoint for relationship data"""
        relationship_data = self.load_relationship_data()
        
        # Process relationship data for the dashboard
        processed_data = []
        for user_id, data in relationship_data.items():
            # Calculate tier info
            points = data.get('points', 100)
            tier_info = self.get_tier_info(points)
            compatibility = self.calculate_compatibility(data)
            
            processed_data.append({
                'user_id': user_id,
                'display_name': await self.get_display_name(user_id),
                'points': points,
                'tier': tier_info['current']['name'],
                'tier_emoji': tier_info['current']['emoji'],
                'compatibility': compatibility,
                'interactions': data.get('interactions', 0),
                'likes': data.get('likes', 0),
                'dislikes': data.get('dislikes', 0),
                'last_sync': data.get('last_sync', ''),
                'progress_percent': tier_info['progress_percent']
            })
        
        # Sort by points (highest first)
        processed_data.sort(key=lambda x: x['points'], reverse=True)
        
        return web.json_response(processed_data)
    
    async def api_facts(self, request):
        """API endpoint for permanent facts"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get all facts grouped by user
            cursor.execute("""
                SELECT user_id, fact_key, fact_value, timestamp 
                FROM permanent_facts 
                ORDER BY timestamp DESC
            """)
            
            facts_data = {}
            for user_id, key, value, timestamp in cursor.fetchall():
                if user_id not in facts_data:
                    facts_data[user_id] = []
                facts_data[user_id].append({
                    'key': key,
                    'value': value,
                    'timestamp': timestamp
                })
            
            return web.json_response(facts_data)
            
        finally:
            conn.close()
    
    async def api_conversations(self, request):
        """API endpoint for recent conversations"""
        # This would need to be implemented based on your conversation storage
        # For now, returning mock data structure
        return web.json_response({
            'recent_messages': [],
            'total_conversations': 0
        })
    
    async def api_stats(self, request):
        """API endpoint for overall statistics"""
        relationship_data = self.load_relationship_data()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Count total facts
            cursor.execute("SELECT COUNT(*) FROM permanent_facts")
            total_facts = cursor.fetchone()[0]
            
            # Count unique users with facts
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM permanent_facts")
            unique_users = cursor.fetchone()[0]
            
            # Calculate relationship statistics
            total_interactions = sum(data.get('interactions', 0) for data in relationship_data.values())
            avg_compatibility = sum(self.calculate_compatibility(data) for data in relationship_data.values()) / max(len(relationship_data), 1)
            
            # Tier distribution
            tier_distribution = {}
            for data in relationship_data.values():
                points = data.get('points', 100)
                tier_info = self.get_tier_info(points)
                tier_name = tier_info['current']['name']
                tier_distribution[tier_name] = tier_distribution.get(tier_name, 0) + 1
            
            stats = {
                'total_users': len(relationship_data),
                'total_facts': total_facts,
                'unique_users_with_facts': unique_users,
                'total_interactions': total_interactions,
                'average_compatibility': round(avg_compatibility, 1),
                'tier_distribution': tier_distribution,
                'system_uptime': self.get_system_uptime()
            }
            
            return web.json_response(stats)
            
        finally:
            conn.close()
    
    def get_tier_info(self, points):
        """Get tier information based on points (same logic as Discord bot)"""
        RELATIONSHIP_TIERS = [
            {"name": "Soulmate", "min_points": 5000, "emoji": "💫"},
            {"name": "Twin Flame", "min_points": 3500, "emoji": "🔥"},
            {"name": "Kindred Spirit", "min_points": 2500, "emoji": "🌟"},
            {"name": "Bestie", "min_points": 1500, "emoji": "💖"},
            {"name": "Close Friend", "min_points": 800, "emoji": "😊"},
            {"name": "Acquaintance", "min_points": 300, "emoji": "👋"},
            {"name": "Stranger", "min_points": 100, "emoji": "😒"},
            {"name": "Rival", "min_points": 0, "emoji": "⚔️"}
        ]
        
        for tier in RELATIONSHIP_TIERS:
            if points >= tier["min_points"]:
                current_tier = tier
                tier_index = RELATIONSHIP_TIERS.index(tier)
                break
        
        next_tier = RELATIONSHIP_TIERS[tier_index - 1] if tier_index > 0 else None
        
        # Calculate progress to next tier
        if next_tier:
            current_min = current_tier["min_points"]
            next_min = next_tier["min_points"]
            progress_percent = int(((points - current_min) / (next_min - current_min)) * 100)
            progress_percent = min(max(progress_percent, 0), 100)
        else:
            progress_percent = 100
        
        return {
            'current': current_tier,
            'next': next_tier,
            'progress_percent': progress_percent
        }
    
    def calculate_compatibility(self, user_data):
        """Calculate compatibility (same logic as Discord bot)"""
        if user_data.get("interactions", 0) == 0:
            return 50
        
        likes = user_data.get("likes", 0)
        dislikes = user_data.get("dislikes", 0)
        neutral = user_data.get("neutral_interactions", 0)
        total_interactions = user_data.get("interactions", 0)
        gifts_received = user_data.get("gifts_received", 0)
        conversation_depth = user_data.get("conversation_depth", 0)
        
        # Base like/dislike ratio
        if likes + dislikes > 0:
            base_ratio = (likes / (likes + dislikes)) * 100
        else:
            base_ratio = 50
        
        # Interaction frequency bonus
        interaction_bonus = min(total_interactions / 20 * 30, 30)
        
        # Gift compatibility
        gift_compatibility = min(gifts_received * 10, 15)
        
        # Conversation depth
        depth_compatibility = min(conversation_depth * 5, 15)
        
        # Consistency bonus
        consistency_bonus = 0
        compatibility_history = user_data.get("compatibility_history", [])
        if len(compatibility_history) >= 3:
            recent_compat = [c["compatibility"] for c in compatibility_history[-3:]]
            avg_compat = sum(recent_compat) / len(recent_compat)
            if max(recent_compat) - min(recent_compat) <= 10:
                consistency_bonus = 10
        
        compatibility = (
            (base_ratio * 0.4) +
            interaction_bonus +
            gift_compatibility +
            depth_compatibility +
            consistency_bonus
        )
        
        return max(0, min(100, int(compatibility)))
    
    async def get_display_name(self, user_id):
        """Get display name for user ID"""
        # In a real implementation, you might want to cache Discord user info
        # For now, return the user_id as display name
        return user_id
    
    def get_system_uptime(self):
        """Calculate system uptime (simplified)"""
        # This would need actual uptime tracking implementation
        return "24 hours"

async def start_dashboard():
    dashboard = MelodyAIDashboard()
    runner = web.AppRunner(dashboard.app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    
    print("🚀 MelodyAI Dashboard running on http://localhost:8080")
    return runner

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    runner = loop.run_until_complete(start_dashboard())
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down dashboard...")
    finally:
        loop.run_until_complete(runner.cleanup())