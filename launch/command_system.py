# melody_ai_v2/launch/command_system.py
import discord
from discord.ext import commands
from typing import Dict, List

# Import our systems
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from brain.memory_systems.permanent_facts import permanent_facts
from brain.memory_systems.semantic_memory import semantic_memory

class CommandSystem:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setup_commands()
        
    def setup_commands(self):
        """Setup all bot commands"""
        
        @self.bot.command(name='melody_help')  # 🆕 CHANGED: Unique name
        async def help_command(ctx):
            """Show help menu"""
            embed = discord.Embed(
                title="🎵 Melody AI Commands",
                description="Your intelligent anime-style companion! 💫",
                color=0x9370DB
            )
            
            embed.add_field(
                name="🧠 Memory & Personal",
                value="`!memory` - View your memory stats\n"
                      "`!myfacts` - See what I remember about you\n"
                      "`!forget` - Remove a specific memory",
                inline=False
            )
            
            embed.add_field(
                name="🎮 Gaming & Anime",
                value="`!champ <name>` - League champion info\n"
                      "`!anime <name>` - Anime information\n"
                      "`!game <name>` - Game details",
                inline=False
            )
            
            embed.add_field(
                name="💫 Utility",
                value="`!ping` - Check bot latency\n"
                      "`!stats` - Bot statistics\n"
                      "`!feedback <message>` - Send feedback",
                inline=False
            )
            
            embed.set_footer(text="Just mention me to chat! I remember our conversations~ 💖")
            await ctx.send(embed=embed)

        @self.bot.command(name='memory')
        async def memory_stats(ctx):
            """Show user's memory statistics"""
            user_id = str(ctx.author.id)
            
            insights = intelligence_orchestrator.get_user_insights(user_id)
            memory_stats = semantic_memory.get_memory_stats(user_id)
            
            embed = discord.Embed(
                title="🧠 Your Memory Profile",
                color=0x9370DB
            )
            
            embed.add_field(
                name="📊 Conversation Stats",
                value=f"Turns: {insights['conversation_turns']}\n"
                      f"Memories: {memory_stats['semantic_memories']}",
                inline=True
            )
            
            embed.add_field(
                name="🎯 Permanent Facts",
                value=f"Stored: {insights['permanent_facts']}\n"
                      f"Health Tracking: {insights['health_tracking']}",
                inline=True
            )
            
            # Show top remembered facts
            if insights['top_remembered_facts']:
                facts_text = "\n".join([
                    f"• {key.replace('_', ' ').title()}: {value}" 
                    for key, value, _ in insights['top_remembered_facts'][:3]
                ])
                embed.add_field(
                    name="💖 Things I Remember",
                    value=facts_text,
                    inline=False
                )
            
            await ctx.send(embed=embed)

        @self.bot.command(name='myfacts')
        async def show_facts(ctx):
            """Show all facts remembered about user"""
            user_id = str(ctx.author.id)
            
            cursor = permanent_facts.conn.cursor()
            cursor.execute('''
                SELECT category, fact_key, fact_value, confidence_score
                FROM user_permanent_facts 
                WHERE user_id = ? 
                ORDER BY confidence_score DESC
            ''', (user_id,))
            
            facts = cursor.fetchall()
            
            if not facts:
                await ctx.send("💫 I don't have any permanent facts about you yet! Just chat with me normally and I'll learn about you~")
                return
            
            embed = discord.Embed(
                title=f"💖 What I Know About {ctx.author.name}",
                color=0x9370DB
            )
            
            # Group facts by category
            categories = {}
            for category, key, value, confidence in facts:
                if category not in categories:
                    categories[category] = []
                
                emoji = "⭐" if confidence >= 3 else "🔹" if confidence >= 2 else "🔸"
                categories[category].append(f"{emoji} {key.replace('_', ' ').title()}: {value}")
            
            for category, items in categories.items():
                embed.add_field(
                    name=f"{category.title()}",
                    value="\n".join(items[:5]),  # Limit to 5 items per category
                    inline=True
                )
            
            embed.set_footer(text="I learn more about you every time we chat! 💫")
            await ctx.send(embed=embed)

        @self.bot.command(name='forget')
        async def forget_fact(ctx, category: str = None, key: str = None):
            """Forget a specific fact"""
            user_id = str(ctx.author.id)
            
            if not category or not key:
                await ctx.send("❌ Usage: `!forget <category> <key>`\nExample: `!forget personal age`")
                return
            
            success = permanent_facts.remove_fact(user_id, category, key)
            
            if success:
                await ctx.send(f"✅ Forgot your {key.replace('_', ' ')} from {category}! 💫")
            else:
                await ctx.send(f"❌ I couldn't find that fact to forget! 📝")

        @self.bot.command(name='ping')
        async def ping_command(ctx):
            """Check bot latency"""
            latency = round(self.bot.latency * 1000)
            
            if latency < 100:
                status = "🚀 Excellent"
                color = 0x00ff00
            elif latency < 200:
                status = "✅ Good"
                color = 0xffff00
            else:
                status = "⚠️ Slow"
                color = 0xff0000
            
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"**Latency:** {latency}ms\n**Status:** {status}",
                color=color
            )
            await ctx.send(embed=embed)

        @self.bot.command(name='stats')
        async def bot_stats(ctx):
            """Show bot statistics"""
            guild_count = len(self.bot.guilds)
            user_count = len(self.bot.users)
            
            # Get memory statistics
            total_memories = semantic_memory.index.ntotal if semantic_memory.index else 0
            
            embed = discord.Embed(
                title="📊 Melody AI Statistics",
                color=0x9370DB
            )
            
            embed.add_field(
                name="🤖 Bot Stats",
                value=f"Servers: {guild_count}\nUsers: {user_count}",
                inline=True
            )
            
            embed.add_field(
                name="🧠 Memory Stats", 
                value=f"Semantic Memories: {total_memories}\nFAISS Enabled: {semantic_memory.index is not None}",
                inline=True
            )
            
            embed.add_field(
                name="💫 System Status",
                value="AI: ✅ Connected\nMemory: ✅ Active\nPersonality: ✅ Online",
                inline=True
            )
            
            await ctx.send(embed=embed)

        @self.bot.command(name='feedback')
        async def feedback_command(ctx, *, message: str):
            """Send feedback to developers"""
            try:
                with open('feedback.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{ctx.author.name} ({ctx.author.id}): {message}\n")
                
                await ctx.send("💖 Thank you for your feedback! I'll make sure the developers see it! 📝")
            except Exception as e:
                await ctx.send("❌ Couldn't save feedback. Please try again later! 🔄")

        @self.bot.command(name='champ')
        async def champion_info(ctx, *, champion_name: str):
            """Get League of Legends champion information"""
            await ctx.send(f"🎮 Champion info for {champion_name} coming soon! Currently setting up the gaming systems~ 💫")

        print("✅ All commands registered!")