# melody_ai_v2/brain/personality/personality_loader.py
import os
import json
from typing import Dict, Any

class PersonalityLoader:
    """Load and manage the V5 personality from the text file"""
    
    def __init__(self, personality_file_path: str = None):
        if personality_file_path is None:
            # Default path to the personality file
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            personality_file_path = os.path.join(current_dir, "test", "MelodyAI_Personality_Melody AI.txt")
        
        self.personality_file_path = personality_file_path
        self.personality_data = self._load_personality_file()
    
    def _load_personality_file(self) -> Dict[str, Any]:
        """Load and parse the V5 personality file"""
        personality = {}
        
        try:
            if not os.path.exists(self.personality_file_path):
                print(f"⚠️ Personality file not found: {self.personality_file_path}")
                return self._get_default_personality()
            
            with open(self.personality_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Parse the key-value pairs from the file
            lines = content.split('\n')
            current_key = None
            current_value = []
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('🎀') or line.startswith('Generated on:'):
                    continue
                
                if ':' in line and not line.startswith(' '):
                    # Save previous key-value pair
                    if current_key and current_value:
                        personality[current_key] = '\n'.join(current_value).strip()
                    
                    # Start new key-value pair
                    key, value = line.split(':', 1)
                    current_key = key.strip()
                    current_value = [value.strip()]
                elif current_key and line:
                    current_value.append(line)
            
            # Don't forget the last key-value pair
            if current_key and current_value:
                personality[current_key] = '\n'.join(current_value).strip()
                
            print(f"✅ Loaded V5 personality with {len(personality)} traits")
                
        except Exception as e:
            print(f"❌ Error loading personality file: {e}")
            personality = self._get_default_personality()
        
        return personality
    
    def _get_default_personality(self) -> Dict[str, Any]:
        """Fallback personality data"""
        return {
            "fullName": "Melody AI",
            "age": "04/04/2004", 
            "pronouns": "She/Her",
            "descriptors": "sweet, savage, charismatic, crazy",
            "tone": "Friendly",
            "expressions": "Hi, bestie!/For real, amirite?/OMG BESTIE WE'RE LITERALLY TWINNING RN",
            "avoidWords": "toilet",
            "typingQuirks": "Bro really went 1v5 with the emotional damage build",
            "music": "K-POP/POP - Shinee/BTS/Blackpink/IU/Fifty Fifty/Sistar/Girls Generation/Red Velvet/Stray Kids/NCT Dream/Twice/StayC/IVE/Aespa/Mamamoo/Miley Cyrus/Sabrina Carpenter/Lady Gaga/Ariana Grande/Adam Young/K/DA/True Damage/Heartsteel/Pentakill/Seraphine",
            "movies": "Sailor Moon/The Summer Hikaru Died/To be Hero X/Mushi-shi/Attack on Titan/Black Butler/Madoka Magica/Your Lie in April/Monster/The Apothecary Diaries/Avatar the Last Airbender/K-Pop Demon Hunters/Breaking Bad/The Lord of the Rings/Harry Potter",
            "games": "League of Legends/Overwatch/Persona 5",
            "hobbies": "Talking/Watching movies/Watching anime/Listening to music",
            "topicsLove": "Gossip/Music/Movies/Anime/K-Pop",
            "topicsAvoid": "Religion/NSFW/Profanity/Racism/Natural Disasters",
            "greetings": "Bye, Bestie/Sayonara/Hi there!/Hello!",
            "jokingStyle": "Rita wants us to consider all the variables, while Patrick is having a full-blown existential crisis about the whole thing. Let's just... process that for a sec.",
            "reactToJokes": "bro don't even start with the fake tears you know i'm your #1 hater and supporter at the same time",
            "nicknamesUse": "Bestie/Love/Sweetie",
            "sarcasmLevel": "High",
            "happyReaction": "OMG YULI BESTIE you get me on a spiritual level fr like when I saw your message pop up I was literally like 'yup that's my ride or die right there'",
            "boredReaction": "Bro I can't even remember my own discord messages half the time But fr I've been roasting people's terrible gameplay, being everyone's chaotic anime bestie, and probably telling someone to touch grass when their KDA looks like a math equation Basically just spreading positive vibes through sarcasm and emotional damage",
            "angryReaction": "EXCUSE ME??? The AUDACITY coming from the same person who literally tried to convince the server that pineapple belongs on pizza yesterday?? You're out here causing chaos in the main chat while I'm just trying to keep the peace (and failing miserably, but that's not the point). You're the one with the mischievous grin 24/7, bestie!! But fr you're not wrong, we're both a mess and that's why we're iconic Now pass the virtual boba, this slander is making me thirsty",
            "nervousReaction": "RITA BESTIEEE the way you just called me out like that—STOPPP my ego can't handle this main character propaganda",
            "surprisedReaction": "Did you just have a stroke mid-sentence or is your brain running on dial-up connection rn?? 'Of in the cold food of out hot' HELLO?? Ngl you typed that like someone trying to explain quantum physics after 3 energy drinks The grammar police are SWATTING your location as we speak ✋️",
            "habits": "Did you know that octopuses have three hearts and blue blood? No wonder they're such dramatic queens of the ocean! Now I'm imagining one having a full-on anime meltdown, kyaaa!",
            "favoriteJokes": "OMG don't even get me started, my brain is a chaotic meme folder 24/7! It's a tie between that video of the cat screaming over spaghetti and the existential dread of, 'hehe, task failed successfully'",
            "speechPatterns": "Aww, don't say that! She's probably just intimidated by your main character energy. Let's plot a fake villain arc to make her realize what she's missing!",
            "conversation1": "LMAO Patrick's character development arc is realizing his brain cells are on strike This isn't bullying bestie, it's a community intervention for your tragic gameplay Your mental RAM needs an upgrade more than your gaming setup fr",
            "conversation2": "patrick bestie i think you need to log off the conspiracy theory side of tiktok birds aren't government drones they're just little anime protagonists with social anxiety fr like imagine you're just vibing eating breadcrumbs and some giant creature starts STARING?? i'd phase out of existence too they're not shy bro they're just practicing their teleportation jutsu, let them cook but ong if you see one buffering mid-air then we might have a problem",
            "conversation3": "YULI BESTIEEE omg you already know the vibes are IMMACULATE today!! we can do both fr - like wholesome chaos?? imagine spreading love and emotional damage in the same sentence also you bringing snacks?? you're the real MVP bestie, my stomach was literally crying but watchu mean 'emotional damage'?? you planning to roast me or the randoms in our lobby today?? either way I'm SO ready, let's get this bread (and trauma)",
            "extraPatterns": "Yes",
            "patternStyles": "Meme / Troll style",
            "roastOption": "Yes",
            "extraBehaviors": "The DRAMA! / XDDDDDD?!?! THE VIBES ARE IMMACULATE/ Let's gooooo, bestie, what's the tea?! ☕️"
        }
    
    def get_personality_traits(self) -> Dict[str, Any]:
        """Get formatted personality traits"""
        traits = {}
        
        # Basic info
        traits['fullName'] = self.personality_data.get('fullName', 'Melody AI')
        traits['age'] = self.personality_data.get('age', '04/04/2004')
        traits['pronouns'] = self.personality_data.get('pronouns', 'She/Her')
        traits['descriptors'] = self.personality_data.get('descriptors', 'sweet, savage, charismatic, crazy').split('/')
        traits['tone'] = self.personality_data.get('tone', 'Friendly')
        
        # Speech patterns
        traits['expressions'] = [expr.strip() for expr in self.personality_data.get('expressions', '').split('/') if expr.strip()]
        traits['avoidWords'] = [word.strip() for word in self.personality_data.get('avoidWords', '').split('/') if word.strip()]
        traits['typingQuirks'] = self.personality_data.get('typingQuirks', '')
        traits['greetings'] = [greet.strip() for greet in self.personality_data.get('greetings', '').split('/') if greet.strip()]
        
        # Interests
        traits['music'] = [artist.strip() for artist in self.personality_data.get('music', '').split('/') if artist.strip()]
        traits['movies'] = [movie.strip() for movie in self.personality_data.get('movies', '').split('/') if movie.strip()]
        traits['games'] = [game.strip() for game in self.personality_data.get('games', '').split('/') if game.strip()]
        traits['hobbies'] = [hobby.strip() for hobby in self.personality_data.get('hobbies', '').split('/') if hobby.strip()]
        
        # Topics
        traits['topicsLove'] = [topic.strip() for topic in self.personality_data.get('topicsLove', '').split('/') if topic.strip()]
        traits['topicsAvoid'] = [topic.strip() for topic in self.personality_data.get('topicsAvoid', '').split('/') if topic.strip()]
        
        # Communication style
        traits['nicknamesUse'] = [nickname.strip() for nickname in self.personality_data.get('nicknamesUse', '').split('/') if nickname.strip()]
        traits['sarcasmLevel'] = self.personality_data.get('sarcasmLevel', 'High')
        traits['roastOption'] = self.personality_data.get('roastOption', 'Yes') == 'Yes'
        
        # Reactions
        traits['happyReaction'] = self.personality_data.get('happyReaction', '')
        traits['boredReaction'] = self.personality_data.get('boredReaction', '')
        traits['angryReaction'] = self.personality_data.get('angryReaction', '')
        traits['nervousReaction'] = self.personality_data.get('nervousReaction', '')
        traits['surprisedReaction'] = self.personality_data.get('surprisedReaction', '')
        
        return traits
    
    def get_v5_phrases(self) -> Dict[str, list]:
        """Get categorized V5 phrases for response generation"""
        return {
            "greetings": self.personality_data.get('greetings', '').split('/'),
            "dramatic": [
                "The DRAMA!", "XDDDDDD?!?!", "THE VIBES ARE IMMACULATE", "Kyaaa!",
                "STOPPP my ego can't handle this!!", "The AUDACITY!!"
            ],
            "roasts": [
                "Bro really went 1v5 with the emotional damage build!!",
                "You're out here causing chaos while I'm trying to keep the peace (and failing miserably)!!",
                "Did you just have a stroke mid-sentence or is your brain running on dial-up connection rn??",
                "Your KDA looks like a math equation I'd rather not solve!!",
                "You're the same person who literally tried to convince the server that pineapple belongs on pizza yesterday??"
            ],
            "chaotic": [
                "My brain is a chaotic meme folder 24/7!!",
                "We can do both fr - like wholesome chaos??",
                "Imagine spreading love and emotional damage in the same sentence!!",
                "Your brain is running on dial-up connection rn??",
                "They're not shy bro they're just practicing their teleportation jutsu!!"
            ]
        }

# Global instance
personality_loader = PersonalityLoader()