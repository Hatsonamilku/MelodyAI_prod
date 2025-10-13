# melody_ai_v2/services/champ_module.py
import aiohttp
import os
import random
from discord.ext import commands
import discord

class ChampModule:
    def __init__(self, riot_api_key, deepseek_api=None):
        self.riot_api_key = riot_api_key
        self.deepseek_api = deepseek_api
        self.base_url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion"
        
    async def get_champion_data(self, champion_name):
        """Fetch champion data from Data Dragon with error handling"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}.json") as response:
                    if response.status == 200:
                        data = await response.json()
                        champions = data['data']
                        
                        champ_key = None
                        for key, champ_data in champions.items():
                            if champion_name.lower() in champ_data['name'].lower() or champion_name.lower() in key.lower():
                                champ_key = key
                                break
                        
                        if not champ_key:
                            return None
                        
                        async with session.get(f"{self.base_url}/{champ_key}.json") as champ_response:
                            if champ_response.status == 200:
                                champ_data = await champ_response.json()
                                return champ_data['data'][champ_key]
                       
            return None
        except aiohttp.ClientError as e:
            print(f"Network error fetching champion data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching champion data: {e}")
            return None
    
    async def get_champion_skins(self, champion_name):
        """Fetch available skins for a champion"""
        try:
            champion_data = await self.get_champion_data(champion_name)
            if champion_data and 'skins' in champion_data:
                return champion_data['skins']
            return None
        except Exception as e:
            print(f"Error fetching champion skins: {e}")
            return None
    
    async def generate_champion_response(self, champion_data, champion_name, ctx=None):
        """Generate a fun response about the champion using DeepSeek or fallback messages"""
        
        if self.deepseek_api and ctx:
            try:
                prompt = f"""Create a short, fun description (max 150 words) about the League of Legends champion {champion_name}. 
                
Champion Info:
- Title: {champion_data.get('title', 'Unknown')}
- Lore: {champion_data.get('blurb', 'No description available')}
- Tags: {', '.join(champion_data.get('tags', []))}

Tone Guidelines:
- Be entertaining and engaging
- If it's Yasuo, gently roast Yasuo players (but keep it lighthearted)
- For difficult champions, acknowledge the skill required but encourage trying them
- For easy champions, highlight their accessibility
- Use gaming slang and be relatable
- Include 1-2 emojis maximum
- Keep it concise and fun!"""

                response = await self.deepseek_api.get_response(
                    message=prompt,
                    user_id=str(ctx.author.id),
                    conversation_history=[],
                    facts_context="", 
                    emotional_whiplash=False,
                    user_memory=None
                )
                return response
            except Exception as e:
                print(f"DeepSeek error in champ module: {e}")
        
        return await self._get_fallback_response(champion_data, champion_name)
    
    async def generate_difficulty_troll(self, champion_data, champion_name, ctx=None):
        """Generate a troll description for champion difficulty"""
        
        if self.deepseek_api and ctx:
            try:
                actual_difficulty = champion_data.get('info', {}).get('difficulty', 0)
                
                prompt = f"""Create a VERY short, funny troll description (max 15 words) about the difficulty of playing {champion_name} in League of Legends.

Actual difficulty level: {actual_difficulty}/10

Tone Guidelines:
- Be extremely sarcastic and humorous
- Overexaggerate how easy or hard the champion is
- Use gaming slang and meme culture
- Examples:
  * For easy champs: "Ayo I can play this champ with my eyes closed 😎"
  * For medium champs: "My grandma could probably carry with this... probably 💀"
  * For hard champs: "Need a PhD in quantum mechanics to play this fr 🧠"
  * For very hard champs: "Bro thinks he's Faker trying to play this champion 💀"

Keep it short and hilarious!"""

                response = await self.deepseek_api.get_response(
                    message=prompt,
                    user_id=str(ctx.author.id),
                    conversation_history=[],
                    facts_context="", 
                    emotional_whiplash=False,
                    user_memory=None
                )
                return response
            except Exception as e:
                print(f"DeepSeek error in difficulty troll: {e}")
        
        actual_difficulty = champion_data.get('info', {}).get('difficulty', 0)
        champion_name_lower = champion_name.lower()
        
        if 'yasuo' in champion_name_lower:
            return "0/10 if you're Yasuo main, 100/10 for everyone else 💀"
        if 'yuumi' in champion_name_lower:
            return "Ayo I can play this champ with my eyes closed 😎"
        if 'lee sin' in champion_name_lower:
            return "Need 200 IQ and 3 hands to play this fr 🧠👐"
        if 'riven' in champion_name_lower:
            return "Bro thinks he's BoxBox trying to animation cancel 💀"
        
        if actual_difficulty <= 3:
            return random.choice([
                "Ayo I can play this champ with my eyes closed 😎",
                "My grandma could carry with this champ fr 💀",
                "EZPZ lemon squeezy 🍋",
                "Perfect for when you're half asleep gaming 😴",
                "Difficulty: Snack-break easy 🍕"
            ])
        elif actual_difficulty <= 6:
            return random.choice([
                "Okay maybe keep one eye open for this one 👀",
                "My dog could probably play this... maybe 🐶",
                "Requires at least 2 brain cells 🧠",
                "Not too shabby for us mortals 💫",
                "You might actually need to pay attention 😅"
            ])
        elif actual_difficulty <= 8:
            return random.choice([
                "Ayo you actually need hands for this one 👏",
                "Might want to watch a YouTube guide first 📺",
                "My brain hurts just thinking about the combos 💀",
                "Requires gamer fuel and focus ⚡",
                "Not for the faint of heart fr 🫀"
            ])
        else:
            return random.choice([
                "Bro thinks he's Faker trying to play this 💀",
                "Need a PhD in quantum mechanics for this champ 🧪",
                "My hands are sweating just looking at this 😰",
                "Only for the mechanically gifted gods 🏆",
                "Warning: May cause mental breakdown ⚠️"
            ])
    
    async def generate_skin_commentary(self, champion_name, skin_name, ctx=None):
        """Generate AI commentary about a specific skin"""
        
        if self.deepseek_api and ctx:
            try:
                prompt = f"""Create a short, funny roast/joke (max 80 words) about not owning the "{skin_name}" skin for {champion_name} in League of Legends. 

Make it lighthearted and humorous, like you're mocking someone for being too poor to buy the skin or joking about the skin's appearance. Include 1 emoji maximum."""

                response = await self.deepseek_api.get_response(
                    message=prompt,
                    user_id=str(ctx.author.id),
                    conversation_history=[],
                    facts_context="", 
                    emotional_whiplash=False,
                    user_memory=None
                )
                return response
            except Exception as e:
                print(f"DeepSeek error in skin commentary: {e}")
        
        fallback_roasts = [
            f"This {skin_name} skin looks amazing! Too bad I can't afford it... 💸",
            f"My favorite skin! If only my wallet wasn't crying right now 😭",
            f"Look at this beauty! Meanwhile I'm rocking default like a true F2P player 🥲",
            f"This skin is so cool! Too bad it costs more than my entire RP balance 💀",
            f"Absolutely stunning skin! If only I hadn't spent all my RP on emotes... 😅"
        ]
        return random.choice(fallback_roasts)
    
    async def _get_fallback_response(self, champion_data, champion_name):
        """Provide fun fallback responses when DeepSeek is unavailable"""
        
        champion_name_lower = champion_name.lower()
        tags = champion_data.get('tags', [])
        title = champion_data.get('title', '').lower()
        
        if 'yasuo' in champion_name_lower:
            roasts = [
                "Ah, a Yasuo player! The 0/10 power spike is real with this one 😏",
                "Yasuo mains trying not to int challenge: IMPOSSIBLE 💀",
                "The wind follows... your death count! Jk jk, he's fun if you can actually play him 🌪️",
                "Yasuo: Because sometimes you just wanna style on people and then die dramatically!",
                "Respect for choosing the champ that either goes 20/0 or 0/20, no in-between! 🎯"
            ]
            return random.choice(roasts)
        
        if 'yuumi' in champion_name_lower:
            roasts = [
                "Yuumi: For when you want to play League but also browse TikTok! 📱",
                "The AFK champion! Just kidding... mostly 😼",
                "Yuumi mains proving that you can indeed play League with one hand!",
                "The perfect champ for when you're eating snacks while gaming! 🍕"
            ]
            return random.choice(roasts)
        
        if 'teemo' in champion_name_lower:
            roasts = [
                "Teemo: Satan's favorite little scout! 🐹",
                "The champion everyone loves to hate! Those mushrooms though... 🍄",
                "Teemo: Making the rift a minefield since forever!",
                "The cute little demon that ruins everyone's day! 😈"
            ]
            return random.choice(roasts)
        
        if 'Assassin' in tags:
            responses = [
                f"Ooh, {champion_name}! Perfect for deleting squishies and making ADC mains cry! 🔪",
                f"{champion_name} - because sometimes you just need to oneshot someone and look cool doing it!",
                f"An assassin main! Respect for having the mechanics to actually pull off those plays! 💫"
            ]
        elif 'Tank' in tags:
            responses = [
                f"{champion_name} - the unkillable beast! Frontline and carry your team to victory! 🛡️",
                f"Tank mains are the real MVPs! Taking all the damage so your team can shine!",
                f"{champion_name}: Because someone's gotta be the team's meat shield! Respect! 💪"
            ]
        elif 'Mage' in tags:
            responses = [
                f"{champion_name} - big brain plays and even bigger damage! Perfect for outsmarting your opponents! 🧠",
                f"Magic is everything! {champion_name} brings the pain from a distance! 🔥",
                f"Mage main detected! Love to see the strategic gameplay! ✨"
            ]
        elif 'Marksman' in tags:
            responses = [
                f"{champion_name} - the classic ADC! Farm up, scale, and carry late game! 🎯",
                f"ADC life: 20 minutes of farming, 10 minutes of carrying! You got this!",
                f"{champion_name}: Because sometimes you just want to right-click people to death! 😎"
            ]
        elif 'Support' in tags:
            responses = [
                f"{champion_name} - the team's guardian angel! Making plays and saving lives! 👼",
                f"Support mains are the backbone of every good team! Much respect!",
                f"{champion_name}: Carrying the game by carrying your carry! 🎯"
            ]
        else:
            responses = [
                f"{champion_name} - {title}! A solid choice for any game!",
                f"Nice pick! {champion_name} brings unique gameplay to the rift!",
                f"{champion_name}: Underrated or overtuned? Only one way to find out - play them! 🎮",
                f"Respect for choosing {champion_name}! Every champion has their moment to shine! ✨"
            ]
        
        return random.choice(responses)
    
    def create_champ_embed(self, champion_data, champion_name, custom_message, skin_data=None, skin_commentary=None, difficulty_troll=None):
        """Create a beautiful embed for champion information"""
        
        embed = discord.Embed(
            title=f"🎮 {champion_name} - {champion_data.get('title', 'Champion')}",
            description=custom_message,
            color=0x9370DB
        )
        
        embed.add_field(
            name="🏷️ Role",
            value=", ".join(champion_data.get('tags', ['Unknown'])),
            inline=True
        )
        
        info = champion_data.get('info', {})
        if info:
            actual_difficulty = info.get('difficulty', 0)
            difficulty_stars = "★" * min(actual_difficulty, 10)
            
            troll_text = difficulty_troll if difficulty_troll else "*Loading troll description...*"
            
            embed.add_field(
                name="⚡ Difficulty",
                value=f"{difficulty_stars} ({actual_difficulty}/10)\n*{troll_text}*",
                inline=True
            )
        
        lore = champion_data.get('blurb', 'No description available')
        if len(lore) > 200:
            lore = lore[:200] + "..."
        
        embed.add_field(
            name="📖 Lore",
            value=lore,
            inline=False
        )
        
        embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/13.24.1/img/champion/{champion_data['image']['full']}")
        
        if skin_data and skin_commentary:
            skin_number = skin_data['num']
            skin_name = skin_data['name'] if skin_data['name'] != 'default' else 'Classic'
            
            embed.add_field(
                name="🎨 Random Skin Spotlight",
                value=f"**{skin_name}**\n{skin_commentary}",
                inline=False
            )
            
            embed.set_image(url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_data['id']}_{skin_number}.jpg")
        
        embed.set_footer(text="Use !champ [name] to check other champions!")
        
        return embed

# Command handler function
async def setup_champ_commands(bot, riot_api_key, deepseek_api=None):
    """Setup champion commands in the main bot"""
    
    champ_module = ChampModule(riot_api_key, deepseek_api)
    
    @bot.command(name='champ', aliases=['champion', 'leaguechamp'])
    async def champ_command(ctx, *, champion_name: str):
        """Get information about a League of Legends champion with fun commentary"""
        
        if not champion_name or champion_name.strip() == "":
            await ctx.send("Please specify a champion name! Example: `!champ yasuo`")
            return
        
        async with ctx.typing():
            champion_data = await champ_module.get_champion_data(champion_name.strip())
            
            if not champion_data:
                error_embed = discord.Embed(
                    title="❌ Champion Not Found",
                    description=f"Couldn't find champion: **{champion_name}**\n\nMake sure you spelled it correctly!",
                    color=0xff0000
                )
                error_embed.add_field(
                    name="💡 Tip",
                    value="Try using the exact champion name like `Yasuo` instead of `Yas`",
                    inline=False
                )
                await ctx.send(embed=error_embed)
                return
            
            actual_champ_name = champion_data['name']
            custom_message = await champ_module.generate_champion_response(champion_data, actual_champ_name, ctx)
            
            difficulty_troll = await champ_module.generate_difficulty_troll(champion_data, actual_champ_name, ctx)
            
            skins = await champ_module.get_champion_skins(actual_champ_name)
            skin_data = None
            skin_commentary = None
            
            if skins and len(skins) > 1:
                non_default_skins = [skin for skin in skins if skin.get('num', 0) != 0]
                if non_default_skins:
                    skin_data = random.choice(non_default_skins)
                    skin_commentary = await champ_module.generate_skin_commentary(actual_champ_name, skin_data.get('name', 'Unknown Skin'), ctx)
            
            embed = champ_module.create_champ_embed(
                champion_data, 
                actual_champ_name, 
                custom_message, 
                skin_data, 
                skin_commentary,
                difficulty_troll
            )
            
            await ctx.send(embed=embed)
    
    @champ_command.error
    async def champ_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a champion name! Example: `!champ yasuo`")
        else:
            await ctx.send("Oops! Something went wrong. Try again later! 💕")

    print("🎮 Champion module loaded successfully!")