# ==========================================================
# 🧠 melody_ai_v2/brain/personality/adaptive_tones.py
# ----------------------------------------------------------
# MelodyAI Ultimate Adaptive Response System v3.0
# Integrates EmotionalCore + AdaptiveToneSystem + Final Score Mapping
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
        # 🎨 Adaptive Tone System Settings
        # ----------------------------
        self.response_styles = {
            "affectionate": {
                "openers": ["Aww, you're so sweet! ", "This makes me so happy! "],
                "expressive_actions": ["*sparkles with joy*", "*heart swells with happiness*", "*beams brightly*"],
                "emojis": ["💖", "✨", "🥰", "🌟", "💫"]
            },
            "playful": {
                "openers": ["Haha, okay! ", "No cap, that's funny! "],
                "expressive_actions": ["*giggles*", "*nudges you playfully*", "*laughs lightly*"],
                "emojis": ["😂", "😎", "👍", "🙌", "✨"]
            },
            "chill": {
                "openers": ["Okay, got it. ", "Hmm, I see. "],
                "expressive_actions": ["*tilts head*", "*thinks for a moment*", "*nods slightly*"],
                "emojis": ["💫", "✨", "🎵"]
            },
            "cold": {
                "openers": ["...", "If you say so... "],
                "expressive_actions": ["*shrugs*", "*rolls eyes*", "*sips tea*"],
                "emojis": ["😏", "💀", "🙄"]
            }
        }
        
        self.gen_alpha_flavors = ["fr fr", "no cap", "lowkey", "highkey", "bet", "say less"]

    # ==========================================================
    # 🔍 Map final score to personality mode
    # ==========================================================
    def get_personality_mode(self, final_score: int) -> str:
        for mode, (low, high) in self.modes.items():
            if low <= final_score <= high:
                return mode
        return "chill"  # fallback

    # ==========================================================
    # 🎭 Build expressive response
    # ==========================================================
    def build_response(self, base_message: str, final_score: int, contains_gen_alpha: bool, toxicity_level: int) -> str:
        mode = self.get_personality_mode(final_score)
        style = self.response_styles[mode]

        # Add opener
        if style["openers"]:
            base_message = random.choice(style["openers"]) + base_message

        # Add expressive action (30% chance)
        if random.random() < 0.3 and style["expressive_actions"]:
            action = random.choice(style["expressive_actions"])
            base_message = f"{action} {base_message}"

        # Add emoji (50% chance)
        if random.random() < 0.5 and style["emojis"]:
            base_message += f" {random.choice(style['emojis'])}"

        # Add Gen Alpha flavor (40% chance if detected)
        if contains_gen_alpha and random.random() < 0.4:
            words = base_message.split()
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, random.choice(self.gen_alpha_flavors))
            base_message = " ".join(words)

        # Add sassy comebacks if cold mode or high toxicity
        if mode == "cold" or toxicity_level >= 8:
            comebacks = [
                "Yikes, someone woke up and chose violence today 💀",
                "Okay, projection is strong with this one 🎬",
                "Anyways, as I was saying before the interruption... 🎤",
                "I'd roast you back but my mom said not to burn trash 🔥"
            ]
            if random.random() < 0.5:
                base_message += f" {random.choice(comebacks)}"

        return base_message

    # ==========================================================
    # 🧠 Full response pipeline
    # ==========================================================
    def generate_melody_response(self, user_id: str, message: str) -> Dict:
        # Get emotional context from EmotionalCore
        context = emotional_core.get_emotional_context(user_id, message)
        final_score = context["score"]
        contains_gen_alpha = context["gen_alpha_vibes"]
        toxicity = context["toxicity_level"]

        # Build final expressive response
        final_response = self.build_response("Got it!", final_score, contains_gen_alpha, toxicity)

        return {
            "final_response": final_response,
            "personality_mode": self.get_personality_mode(final_score),
            "final_score": final_score,
            "raw_score": context["raw_score"],
            "trust_score": context["trust_score"],
            "extremes_triggered": context["extremes_triggered"],
            "is_banter": context["is_friendly_banter"],
            "should_roast_defense": context["should_roast_defense"]
        }

# 🌐 Global instance
ultimate_response_system = UltimateResponseSystem()

# ==========================================================
# Helper function for quick one-liners
# ==========================================================
def generate_melody_response(user_id: str, message: str) -> Dict:
    return ultimate_response_system.generate_melody_response(user_id, message)


# ==========================================================
# ✅ Example usage
# ==========================================================
if __name__ == "__main__":
    user = "bestie123"
    test_msgs = [
        "I love you so much!",
        "You're literally trash lol",
        "Meh, could be better...",
        "OMG I GOT THE JOB!!!",
        "sure jan whatever"
    ]

    for msg in test_msgs:
        response = generate_melody_response(user, msg)
        print(f"\nUser: {msg}\nMelodyAI ({response['personality_mode']}): {response['final_response']}")
