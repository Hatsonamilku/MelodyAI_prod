# melody_ai_v2/🧠 brain/personality/adaptive_tones.py
import random
from typing import Dict, List, Tuple

class AdaptiveToneSystem:
    def __init__(self):
        self.sentiment_thresholds = {
            "super_positive": 15,
            "positive": 5,
            "neutral": -4,
            "sassy": -5,
            "super_sassy": -15
        }
        
        self.response_styles = {
            "super_positive": {
                "vocabulary": ["amazing", "wonderful", "love this", "so happy", "brilliant"],
                "emojis": ["💖", "✨", "🌟", "🥰", "💫"],
                "expressive_actions": [
                    "*sparkles with joy*", 
                    "*beams brightly*",
                    "*heart swells with happiness*"
                ],
                "openers": ["Aww, you're so sweet! ", "This makes me so happy! ", "I love this! "]
            },
            "positive": {
                "vocabulary": ["great", "nice", "cool", "awesome", "fun"],
                "emojis": ["😊", "🎵", "✨", "👍"],
                "expressive_actions": [
                    "*smiles warmly*",
                    "*nods enthusiastically*"
                ],
                "openers": ["That's great! ", "Nice! ", "Cool! "]
            },
            "neutral": {
                "vocabulary": ["okay", "interesting", "got it", "understand"],
                "emojis": ["💫", "✨", "🎵"],
                "expressive_actions": [
                    "*tilts head*",
                    "*thinks for a moment*"
                ],
                "openers": ["", "So, ", "Anyway, "]
            },
            "sassy": {
                "vocabulary": ["okay buddy", "sure jan", "anyways", "as I was saying"],
                "emojis": ["😏", "🙄", "💀", "🍵"],
                "expressive_actions": [
                    "*rolls eyes dramatically*",
                    "*sips tea*",
                    "*adjusts imaginary glasses*"
                ],
                "openers": ["Okay, and? ", "Anyways... ", "Moving on... "]
            },
            "super_sassy": {
                "vocabulary": ["yikes", "oof", "big yikes", "anyway"],
                "emojis": ["💀", "🗿", "🚩", "🎪"],
                "expressive_actions": [
                    "*dramatic sigh*",
                    "*flips hair*", 
                    "*drops mic*"
                ],
                "openers": ["Yikes... ", "Oof, okay... ", "Well then... "]
            }
        }
        
        self.gen_alpha_references = {
            "based": ["based", "so real for that", "spitting facts"],
            "fire": ["fire", "banger", "hits different"],
            "slay": ["slay", "queen behavior", "king energy"],
            "ratio": ["ratio", "L + ratio", "taking Ls"],
            "skill_issue": ["skill issue", "git gud", "cope"]
        }

    def detect_tone_category(self, sentiment_score: int) -> str:
        """Determine tone category based on sentiment score"""
        if sentiment_score >= self.sentiment_thresholds["super_positive"]:
            return "super_positive"
        elif sentiment_score >= self.sentiment_thresholds["positive"]:
            return "positive"
        elif sentiment_score >= self.sentiment_thresholds["neutral"]:
            return "neutral"
        elif sentiment_score >= self.sentiment_thresholds["sassy"]:
            return "sassy"
        else:
            return "super_sassy"

    def adapt_response_style(self, response: str, sentiment_score: int, 
                           contains_gen_alpha: bool = False) -> str:
        """Adapt response based on sentiment and context"""
        tone_category = self.detect_tone_category(sentiment_score)
        style = self.response_styles[tone_category]
        
        # Add opener
        if style["openers"]:
            opener = random.choice(style["openers"])
            response = opener + response
        
        # Add expressive action (30% chance)
        if random.random() < 0.3 and style["expressive_actions"]:
            action = random.choice(style["expressive_actions"])
            response = f"{action} {response}"
        
        # Add emoji (50% chance)
        if random.random() < 0.5 and style["emojis"]:
            emoji = random.choice(style["emojis"])
            response = response + f" {emoji}"
        
        # Add Gen Alpha flavor if detected
        if contains_gen_alpha and random.random() < 0.4:
            response = self._add_gen_alpha_flavor(response)
        
        return response

    def _add_gen_alpha_flavor(self, response: str) -> str:
        """Add Gen Alpha slang and references"""
        flavors = [
            "fr fr", "no cap", "lowkey", "highkey", "bet", "say less"
        ]
        flavor = random.choice(flavors)
        
        # Insert at random position or append
        if random.random() < 0.5:
            words = response.split()
            if len(words) > 2:
                insert_pos = random.randint(1, len(words) - 1)
                words.insert(insert_pos, flavor)
                response = " ".join(words)
        else:
            response = f"{response} {flavor}"
        
        return response

    def get_sassy_comeback(self, toxicity_level: int) -> str:
        """Generate sassy comebacks based on toxicity level"""
        if toxicity_level == 1:  # Mild sass
            comebacks = [
                "Okay, and? 🍵",
                "Anyways... ✨",
                "Cool story bro 📖",
                "I'm gonna pretend I didn't see that 🙈"
            ]
        else:  # Savage mode
            comebacks = [
                "Yikes, someone woke up and chose violence today 💀",
                "Okay, projection is strong with this one 🎬",
                "Anyways, as I was saying before the interruption... 🎤",
                "I'd roast you back but my mom said not to burn trash 🔥"
            ]
        
        return random.choice(comebacks)

# Global instance
tone_system = AdaptiveToneSystem()