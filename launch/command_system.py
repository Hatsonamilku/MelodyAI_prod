import discord
from discord.ext import commands
from brain.core_intelligence.intelligence_orchestrator import intelligence_orchestrator
from brain.memory_systems.permanent_facts import permanent_facts
from brain.memory_systems.semantic_memory import semantic_memory

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
            user_id = str(ctx.author.id)
            insights = await intelligence_orchestrator.get_user_insights(user_id)
            memory_stats = await semantic_memory.get_memory_stats(user_id)
            embed = discord.Embed(title="🧠 Memory Profile", color=0x9370DB)
            embed.add_field(name="📊 Conversation Turns", value=insights["conversation_turns"], inline=True)
            embed.add_field(name="🎯 Permanent Facts", value=insights["permanent_facts"], inline=True)
            await ctx.send(embed=embed)

        @self.bot.command(name='myfacts')
        async def show_facts(ctx):
            user_id = str(ctx.author.id)
            facts = await permanent_facts.get_all_facts(user_id)
            if not facts:
                await ctx.send("💫 I have no permanent facts yet!")
                return
            embed = discord.Embed(title=f"💖 Facts About {ctx.author.name}", color=0x9370DB)
            for category, key, value, conf in facts:
                embed.add_field(name=category, value=f"{key}: {value} ({conf})", inline=False)
            await ctx.send(embed=embed)

        @self.bot.command(name='ping')
        async def ping(ctx):
            latency = round(self.bot.latency*1000)
            await ctx.send(f"🏓 Pong! {latency}ms")

        # 🆕 ADDED TEST COMMANDS
        @self.bot.command(name='test')
        async def test_command(ctx):
            """Test channel communication"""
            print(f"🧪 TEST COMMAND: Received from {ctx.author} in {ctx.channel.name}")
            try:
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
                from services.discord_adapter import DiscordMelodyAdapter
                adapter = DiscordMelodyAdapter()
                result = await adapter.quick_diagnostic(ctx.channel)
                await ctx.send(f"🩺 Diagnostic Results:\n```{result}```")
            except Exception as e:
                print(f"❌ DIAGNOSE COMMAND ERROR: {e}")
                await ctx.send(f"❌ Diagnose command failed: {e}")