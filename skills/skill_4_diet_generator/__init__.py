"""Skill 4: diet-generator package init
Expose a minimal API for the diet generator skill.
"""

from .scripts.diet_generator import generate_diet

__all__ = ["generate_diet"]
