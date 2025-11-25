"""Minimal diet generator script

This file provides a tiny, self-contained generate_diet function and a
simple CLI for quick testing.
"""
from __future__ import annotations

from typing import Dict, List


def generate_diet(user_profile: Dict) -> Dict:
    """Generate a placeholder daily diet based on minimal user_profile fields.

    Expected keys in user_profile (optional):
    - name: str
    - calories: int
    - preferences: List[str]

    Returns a dict with a simple meal plan.
    """
    calories = int(user_profile.get("calories", 2000))
    name = user_profile.get("name", "User")
    preferences = user_profile.get("preferences", [])

    # Very naive split: 30% breakfast, 40% lunch, 30% dinner
    breakfast = int(calories * 0.3)
    lunch = int(calories * 0.4)
    dinner = calories - breakfast - lunch

    plan = {
        "name": name,
        "calories_total": calories,
        "meals": [
            {"name": "breakfast", "calories": breakfast, "items": ["oatmeal", "banana"]},
            {"name": "lunch", "calories": lunch, "items": ["chicken salad", "brown rice"]},
            {"name": "dinner", "calories": dinner, "items": ["salmon", "steamed veg"]},
        ],
        "notes": "preferences: {}".format(",".join(preferences))
    }
    return plan


def _cli():
    import json
    import sys

    if len(sys.argv) > 1:
        try:
            profile = json.loads(sys.argv[1])
        except Exception:
            print("Invalid JSON input")
            sys.exit(2)
    else:
        profile = {"calories": 1800}

    plan = generate_diet(profile)
    print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
