# ==========================================================
# 🧠 melody_ai_v2/brain/personality/adaptive_tones.py
# ----------------------------------------------------------
# MelodyAI Ultimate Adaptive Response System v3.1 - CLEAN FIX
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
        # 🎨 SUBTLE Tone Enhancements
        # ----------------------------
        self.response_styles = {
            "affectionate": {
                "emojis": ["💖", "✨", "🥰", "🌟", "💫"],
                "subtle_enhancements": ["Aww ", "So sweet ", ""]
            },
            "playful": {
                "emojis": ["😂", "😎", "✨", "🙌", "💀"],
                "subtle_enhancements": ["Haha ", "Lol ", ""]
            },
            "chill": {
                "emojis": ["💫", "✨", "🎵"],
                "subtle_enhancements": ["Okay ", "I see ", ""]
            },
            "cold": {
                "emojis": ["😏", "💀", "🙄"],
                "subtle_enhancements": ["...", "Hmm ", ""]
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
    # 🎭 Build SUBTLE expressive response
    # ==========================================================
    def build_response(self, base_message: str, final_score: int, contains_gen_alpha: bool, toxicity_level: int) -> str:
        mode = self.get_personality_mode(final_score)
        style = self.response_styles[mode]

        # Start with clean base message
        final_response = base_message

        # Add subtle enhancement (20% chance, and only if it fits naturally)
        if random.random() < 0.2 and style["subtle_enhancements"]:
            enhancement = random.choice(style["subtle_enhancements"])
            # Only add if it doesn't create awkward double openings
            if enhancement and not any(opener in final_response.lower() for opener in ["haha", "lol", "aww", "okay"]):
                final_response = enhancement + final_response

        # Add emoji (40% chance) - but only if not too many already
        if random.random() < 0.4 and style["emojis"]:
            current_emojis = sum(1 for char in final_response if char in ['💖','✨','🥰','🌟','💫','😂','😎','🙌','💀','🎵','😏','🙄'])
            if current_emojis < 2:  # Don't add if already has emojis
                final_response += f" {random.choice(style['emojis'])}"

        # Add Gen Alpha flavor (30% chance if detected and not already present)
        if contains_gen_alpha and random.random() < 0.3:
            if not any(flavor in final_response.lower() for flavor in self.gen_alpha_flavors):
                # Add at end or in middle naturally
                if random.random() < 0.5:
                    final_response += f" {random.choice(self.gen_alpha_flavors)}"
                else:
                    words = final_response.split()
                    if len(words) > 3:
                        insert_pos = random.randint(1, len(words)-1)
                        words.insert(insert_pos, random.choice(self.gen_alpha_flavors))
                        final_response = " ".join(words)

        # Add sassy comebacks only for cold mode or high toxicity
        if (mode == "cold" or toxicity_level >= 8) and random.random() < 0.4:
            comebacks = [
                "Yikes, someone woke up and chose violence today 💀",
                "Okay, projection is strong with this one 🎬",
                "Anyways, as I was saying... 🎤"
            ]
            final_response += f" {random.choice(comebacks)}"

        return final_response

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