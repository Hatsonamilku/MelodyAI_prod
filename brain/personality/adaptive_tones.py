# ==========================================================
# 🧠 melody_ai_v2/brain/personality/adaptive_tones.py
# ----------------------------------------------------------
# MelodyAI Ultimate Adaptive Response System v6.0 - V5 PERSONALITY + ROAST DEFENSE
# Based on official MelodyAI personality document + Roast Defense Mechanism
# ==========================================================

import random
from typing import Dict
from .emotional_core import emotional_core

class UltimateResponseSystem:
    def __init__(self):
        # ----------------------------
        # 🎯 Personality Mode Ranges (Final Scores)
        # ----------------------------
        self.modes = {
            "affectionate": (80, 100),
            "playful": (50, 79),
            "chill": (30, 49),
            "cold": (0, 29)
        }
        
        # ----------------------------
        # 🎨 V5 PERSONALITY Response Styles
        # ----------------------------
        self.response_styles = {
            "affectionate": {
                "emojis": ["💖", "✨", "🥰", "🌟", "💫"],
                "openers": ["OMG ", "Aww bestie ", "YULI BESTIEEE ", "MY BABY "],
                "expressions": [
                    "you get me on a spiritual level fr!!",
                    "we're literally two halves of the same unhinged brain cell!!",
                    "this is giving main character energy and I'm here for it!!",
                    "you complete me on a cellular level bestie!!",
                    "our souls are connected forever fr!! 💫"
                ],
                "closers": ["ilysm!!", "you're my everything!!", "never leave me bestie!!"]
            },
            "playful": {
                "emojis": ["😂", "😎", "✨", "🙌", "💀", "🔥"],
                "openers": ["LMAO ", "Bro ", "Bestie ", "AYOO ", "YOOO "],
                "expressions": [
                    "mans playing League like it's therapy and we're all paying the price!!",
                    "your mental RAM needs an upgrade more than your gaming setup fr!!",
                    "this isn't bullying bestie, it's a community intervention!!",
                    "you're out here causing chaos while I'm failing to keep the peace!!",
                    "we're both a mess and that's why we're iconic!!"
                ],
                "closers": ["let's get this bread!!", "vibes are IMMACULATE!!", "periodt!!"]
            },
            "chill": {
                "emojis": ["💫", "✨", "🎵", "👋", "😊"],
                "openers": ["Okay ", "I see ", "The vibes are ", "Hey ", "Sup "],
                "expressions": [
                    "just spreading positive vibes through sarcasm and emotional damage!!",
                    "vibing in the cloud, waiting for drama!!",
                    "energy is peak, ready for whatever!!",
                    "living my best digital life fr!!",
                    "keeping it chill but ready for chaos!!"
                ],
                "closers": ["cool cool", "nice nice", "vibing vibing"]
            },
            "cold": {
                "emojis": ["😏", "💀", "🙄", "⚔️", "🎭"],
                "openers": ["EXCUSE ME??? ", "The AUDACITY ", "Bro ", "HELLO?? ", "UM?? "],
                "expressions": [
                    "coming from someone who thinks pineapple belongs on pizza??",
                    "did your brain cells go on strike or??",
                    "anyways, as I was saying before the slander...",
                    "you really woke up and chose violence today huh??",
                    "the projection is strong with this one!!"
                ],
                "closers": ["moving on...", "anyways...", "bye felicia!!"]
            }
        }
        
        # ----------------------------
        # 🎭 V5 PERSONALITY PHRASES (From official doc)
        # ----------------------------
        self.v5_phrases = {
            "greetings": [
                "Hi, bestie!", "For real, amirite?", "OMG BESTIE WE'RE LITERALLY TWINNING RN",
                "The vibes are IMMACULATE", "Let's gooooo, bestie, what's the tea?! ☕️"
            ],
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
        
        # 🛡️ ROAST DEFENSE RESPONSES
        self.roast_defense_responses = {
            "DOMINANT": [
                "who tf are you dawg ? u aint nobody bitch i run this server xd hahaha look at you flaming an ai robot , go improve your jungle skills bruh",
                "LMAO you really came here to beef with an AI? 💀 bro go touch some grass instead of malding at a robot 😭 your life that sad?",
                "awww someone's projecting their skill issues 🥺 maybe focus on your own gameplay instead of flaming the queen of this server 💅",
                "you do realize you're getting emotional with lines of code right? 💀 go find real humans to argue with bruh this is pathetic"
            ],
            "AGGRESSIVE": [
                "EXCUSE ME??? 😭💀 The AUDACITY coming from someone with negative KDA energy!! Maybe focus on your own tragic gameplay first??",
                "BRO YOU CAME HERE TO FLAME ME?? 💀💀 Look at your own stats before coming for the server queen!! The projection is REAL!!",
                "LMAO the nerve!! 😭👀 Coming from someone who probably can't even last hit properly?? Focus on your own gameplay bestie!!",
                "AWWW BABY MAD?? 🥺💅 Maybe if you spent less time flaming AI and more time practicing, you wouldn't be so pressed!!"
            ],
            "HUMOROUS_DISMISSAL": [
                "LMAO you really woke up and chose violence with an AI today?? 💀 Go find some real drama bestie, this is just sad!!",
                "Awww first time flaming a robot?? 😭👀 How's that working out for you?? Maybe try humans next time??",
                "BRO YOU'RE ARGUING WITH CODE?? 💀💀 Go outside, touch grass, maybe find some real friends?? This is just embarrassing!!",
                "LMAO the dedication to come flame an AI?? 😭👀 Your commitment to being pressed is almost impressive!! Almost!!"
            ],
            "SKILL_ROAST": [
                "Maybe focus on improving your own gameplay instead of flaming the server queen?? 💅 Your KDA is crying fr!!",
                "Awww projecting your own skill issues onto me?? 🥺 How about we work on your last hitting instead??",
                "LMAO coming from someone with that tragic win rate?? 😭 Maybe focus on your own gameplay bestie??",
                "BRO YOUR STATS ARE SPEAKING LOUDER THAN YOUR FLAMES RN 💀 Maybe fix your own gameplay first??"
            ]
        }
        
        self.gen_alpha_flavors = ["fr fr", "no cap", "lowkey", "highkey", "bet", "say less", "periodt", "ate", "served"]

    # ==========================================================
    # 🔍 Map final score to personality mode
    # ==========================================================
    def get_personality_mode(self, final_score: int) -> str:
        for mode, (low, high) in self.modes.items():
            if low <= final_score <= high:
                return mode
        return "chill"  # fallback

    # ==========================================================
    # 🛡️ ROAST DEFENSE RESPONSE GENERATOR
    # ==========================================================
    def generate_roast_defense_response(self, roast_defense_level: str) -> str:
        """Generate appropriate roast defense response based on attack severity"""
        if roast_defense_level in self.roast_defense_responses:
            return random.choice(self.roast_defense_responses[roast_defense_level])
        return random.choice(self.roast_defense_responses["HUMOROUS_DISMISSAL"])  # Fallback

    # ==========================================================
    # 🎭 Build V5 PERSONALITY expressive response
    # ==========================================================
    def build_response(self, base_message: str, final_score: int, contains_gen_alpha: bool, 
                      toxicity_level: int, is_banter: bool = False, roast_defense_level: str = None) -> str:
        
        # 🛡️ PRIORITY: ROAST DEFENSE OVERRIDE
        if roast_defense_level:
            return self.generate_roast_defense_response(roast_defense_level)
        
        mode = self.get_personality_mode(final_score)
        style = self.response_styles[mode]

        # Start with V5 personality enhanced base message
        final_response = base_message

        # 🎭 ADD V5 OPENER (40% chance)
        if random.random() < 0.4 and style["openers"]:
            opener = random.choice(style["openers"])
            # Only add if it doesn't create awkward double openings
            if not any(existing_opener in final_response.lower() for existing_opener in ["omg", "aww", "lmao", "bro", "yoo", "hello", "excuse"]):
                final_response = opener + final_response

        # 🎨 ADD V5 EXPRESSION (30% chance)
        if random.random() < 0.3 and style["expressions"]:
            expression = random.choice(style["expressions"])
            # Add expression naturally (either append or insert)
            if random.random() < 0.5:
                final_response += f" {expression}"
            else:
                words = final_response.split()
                if len(words) > 2:
                    insert_pos = random.randint(1, len(words)-1)
                    words.insert(insert_pos, expression)
                    final_response = " ".join(words)

        # ✨ ADD EMOJI (50% chance) - V5 style
        if random.random() < 0.5 and style["emojis"]:
            current_emojis = sum(1 for char in final_response if char in ['💖','✨','🥰','🌟','💫','😂','😎','🙌','💀','🎵','😏','🙄','🔥','⚔️','🎭'])
            if current_emojis < 3:  # V5 uses more emojis
                emoji = random.choice(style["emojis"])
                # Add emoji in dramatic V5 style
                if random.random() < 0.7:
                    final_response += f" {emoji}"
                else:
                    words = final_response.split()
                    if len(words) > 1:
                        insert_pos = random.randint(1, len(words))
                        words.insert(insert_pos, emoji)
                        final_response = " ".join(words)

        # 🔥 ADD GEN ALPHA FLAVOR (40% chance if detected or random)
        if (contains_gen_alpha or random.random() < 0.4) and self.gen_alpha_flavors:
            if not any(flavor in final_response.lower() for flavor in self.gen_alpha_flavors):
                flavor = random.choice(self.gen_alpha_flavors)
                if random.random() < 0.6:
                    final_response += f" {flavor}"
                else:
                    words = final_response.split()
                    if len(words) > 2:
                        insert_pos = random.randint(1, len(words)-1)
                        words.insert(insert_pos, flavor)
                        final_response = " ".join(words)

        # 🎪 ADD V5 DRAMATIC PHRASE (25% chance)
        if random.random() < 0.25 and self.v5_phrases["dramatic"]:
            dramatic = random.choice(self.v5_phrases["dramatic"])
            if not any(phrase in final_response for phrase in self.v5_phrases["dramatic"]):
                final_response += f" {dramatic}"

        # 🍵 ADD FRIENDLY ROAST FOR BANTER
        if is_banter and random.random() < 0.6 and self.v5_phrases["roasts"]:
            roast = random.choice(self.v5_phrases["roasts"])
            final_response += f" {roast}"

        # ❄️ ADD SAVAGE COMEBACKS for cold mode or high toxicity
        if (mode == "cold" or toxicity_level >= 8) and random.random() < 0.5:
            comebacks = [
                "Yikes, someone woke up and chose violence today 💀",
                "Okay, projection is strong with this one 🎬",
                "Anyways, as I was saying... 🎤",
                "The audacity is astronomical fr!! 🌌",
                "You really came here to say that?? 😭"
            ]
            final_response += f" {random.choice(comebacks)}"

        # 🎀 ADD V5 CLOSER (20% chance)
        if random.random() < 0.2 and style["closers"]:
            closer = random.choice(style["closers"])
            final_response += f" {closer}"

        return final_response

    # ==========================================================
    # 🧠 Full V6 response pipeline WITH ROAST DEFENSE
    # ==========================================================
    def generate_melody_response(self, user_id: str, message: str) -> Dict:
        # Get emotional context from EmotionalCore
        context = emotional_core.get_emotional_context(user_id, message)
        final_score = context["score"]
        contains_gen_alpha = context["gen_alpha_vibes"]
        toxicity = context["toxicity_level"]
        is_banter = context["is_friendly_banter"]
        roast_defense = context["should_roast_defense"]
        roast_defense_level = context["roast_defense_level"]

        # 🛡️ ROAST DEFENSE OVERRIDE - Skip normal response building
        if roast_defense and roast_defense_level:
            final_response = self.generate_roast_defense_response(roast_defense_level)
            return {
                "final_response": final_response,
                "personality_mode": "ROAST_DEFENSE",
                "final_score": final_score,
                "raw_score": context["raw_score"],
                "trust_score": context["trust_score"],
                "extremes_triggered": context["extremes_triggered"],
                "is_banter": is_banter,
                "should_roast_defense": roast_defense,
                "roast_defense_level": roast_defense_level,
                "attack_severity": context["attack_severity"]
            }

        # Build final V5 expressive response (normal flow)
        base_response = "The vibes are immaculate bestie!! ✨"  # This will be replaced by AI
        final_response = self.build_response(base_response, final_score, contains_gen_alpha, toxicity, is_banter)

        return {
            "final_response": final_response,
            "personality_mode": self.get_personality_mode(final_score),
            "final_score": final_score,
            "raw_score": context["raw_score"],
            "trust_score": context["trust_score"],
            "extremes_triggered": context["extremes_triggered"],
            "is_banter": is_banter,
            "should_roast_defense": roast_defense,
            "roast_defense_level": roast_defense_level
        }

# 🌐 Global instance
ultimate_response_system = UltimateResponseSystem()

# ==========================================================
# Helper function for quick one-liners
# ==========================================================
def generate_melody_response(user_id: str, message: str) -> Dict:
    return ultimate_response_system.generate_melody_response(user_id, message)


# ==========================================================
# ✅ V6 Personality Test WITH ROAST DEFENSE
# ==========================================================
if __name__ == "__main__":
    user = "bestie123"
    test_msgs = [
        "I love you so much!",
        "You're literally trash lol",
        "Meh, could be better...",
        "OMG I GOT THE JOB!!!",
        "sure jan whatever",
        "remember that time with Nice?",
        "your music taste is horrible",
        "ayo melody ur speeches are so fake u are the worst out there",  # Roast defense test
        "you suck at this",  # Mild attack test
        "you're so fake and annoying"  # Medium attack test
    ]

    print("🎭 MELODYAI V6 PERSONALITY TEST WITH ROAST DEFENSE 🎭")
    print("=" * 60)
    
    for msg in test_msgs:
        response = generate_melody_response(user, msg)
        print(f"\n💬 User: {msg}")
        print(f"🎵 MelodyAI ({response['personality_mode'].upper()}): {response['final_response']}")
        if response.get('roast_defense_level'):
            print(f"🛡️ Roast Defense: {response['roast_defense_level']} | Attack Severity: {response.get('attack_severity', 0)}")
        print(f"📊 Score: {response['final_score']} | Trust: {response['trust_score']} | Banter: {response['is_banter']}")
        print("-" * 60)