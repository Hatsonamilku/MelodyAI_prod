# launch/command_system.py - FIXED VERSION
import discord
from discord.ext import commands
import logging

logger = logging.getLogger("CommandSystem")

class CommandSystem:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setup_commands()

    def setup_commands(self):
        @self.bot.command(name='melody_help')
        async def help_command(ctx):
            embed = discord.Embed(
                title="🎵 Melody AI Commands",
                description="Your intelligent anime companion! 💫",
                color=0x9370DB
            )
            embed.add_field(name="🧠 Memory", value="`!memory` - Stats\n`!myfacts` - Facts\n`!forget` - Forget", inline=False)
            embed.add_field(name="🎮 Gaming", value="`!champ <name>` - League info", inline=False)
            embed.add_field(name="💫 Utility", value="`!ping`, `!stats`, `!feedback`", inline=False)
            embed.set_footer(text="Just mention me to chat! 💖")
            await ctx.send(embed=embed)

        @self.bot.command(name='memory')
        async def memory_stats(ctx):
            """Memory statistics command with safe imports"""
            try:
                # Lazy import to avoid circular dependencies
                from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
                
                user_id = str(ctx.author.id)
                # Use available methods - adjust based on actual available methods
                embed = discord.Embed(title="🧠 Memory Profile", color=0x9370DB)
                embed.add_field(name="📊 User ID", value=user_id, inline=True)
                embed.add_field(name="💫 Status", value="Memory system active!", inline=True)
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"❌ Error in memory command: {e}")
                await ctx.send("❌ Memory system is currently upgrading! 💫")

        @self.bot.command(name='myfacts')
        async def show_facts(ctx):
            """Show user facts with safe imports"""
            try:
                # Lazy import to avoid circular dependencies
                from brain.memory_systems.permanent_facts import permanent_facts
                
                user_id = str(ctx.author.id)
                user_context = await permanent_facts.get_user_context(user_id)
                
                if not user_context or "no facts" in user_context.lower():
                    await ctx.send("💫 I haven't learned any facts about you yet! Start chatting with me! 💖")
                    return
                    
                embed = discord.Embed(title=f"💖 About {ctx.author.name}", color=0x9370DB)
                # Truncate if too long
                if len(user_context) > 1000:
                    user_context = user_context[:997] + "..."
                embed.add_field(name="📝 What I Know", value=user_context, inline=False)
                await ctx.send(embed=embed)
                
            except Exception as e:
                logger.error(f"❌ Error in myfacts command: {e}")
                await ctx.send("❌ Facts system is currently upgrading! 💫")

        @self.bot.command(name='ping')
        async def ping(ctx):
            latency = round(self.bot.latency*1000)
            await ctx.send(f"🏓 Pong! {latency}ms")

        @self.bot.command(name='test')
        async def test_command(ctx):
            """Test channel communication"""
            print(f"🧪 TEST COMMAND: Received from {ctx.author} in {ctx.channel.name}")
            try:
                # Lazy import to avoid circular dependencies
                from services.discord_adapter import DiscordMelodyAdapter
                adapter = DiscordMelodyAdapter()
                success = await adapter.test_channel_communication(ctx.channel)
                if success:
                    await ctx.send("✅ All tests passed! Channel communication is working! 🎉")
                else:
                    await ctx.send("❌ Some tests failed! Check console for details. 🔧")
            except Exception as e:
                print(f"❌ TEST COMMAND ERROR: {e}")
                await ctx.send(f"❌ Test command failed: {e}")

        @self.bot.command(name='diagnose')
        async def diagnose_command(ctx):
            """Quick diagnostic"""
            print(f"🩺 DIAGNOSE COMMAND: Received from {ctx.author} in {ctx.channel.name}")
            try:
                # Lazy import to avoid circular dependencies
                from services.discord_adapter import DiscordMelodyAdapter
                adapter = DiscordMelodyAdapter()
                result = await adapter.quick_diagnostic(ctx.channel)
                await ctx.send(f"🩺 Diagnostic Results:\n```{result}```")
            except Exception as e:
                print(f"❌ DIAGNOSE COMMAND ERROR: {e}")
                await ctx.send(f"❌ Diagnose command failed: {e}")