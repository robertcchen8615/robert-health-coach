"""Minimal diet generator script

This module provides a diet generator that produces daily meal plans based on
user profiles (calories, preferences, etc.).

Functions:
    generate_diet(user_profile: Dict) -> Dict: Generate a daily meal plan.
    _cli(): Command-line interface for quick testing.
"""
from __future__ import annotations

from typing import Dict, List


def generate_diet(user_profile: Dict) -> Dict:
    """Generate a placeholder daily diet based on user_profile fields.

    This function creates a simple meal plan with a naive calorie split:
    - Breakfast: 30% of daily calories
    - Lunch: 40% of daily calories
    - Dinner: 30% of daily calories

    Args:
        user_profile (Dict): User profile with optional keys:
            - calories (int or str): Total daily calorie intake. Default: 2000.
            - name (str): User's name. Default: "User".
            - preferences (List[str]): Dietary preferences (e.g., "vegetarian").

    Returns:
        Dict: A meal plan with the following structure:
            {
                "name": str,
                "calories_total": int,
                "meals": [
                    {
                        "name": str,
                        "calories": int,
                        "items": List[str]
                    },
                    ...
                ],
                "notes": str
            }

    Examples:
        >>> plan = generate_diet({"calories": 2000})
        >>> plan["calories_total"]
        2000
        >>> len(plan["meals"])
        3

        >>> plan = generate_diet({
        ...     "calories": 1500,
        ...     "name": "Alice",
        ...     "preferences": ["vegetarian"]
        ... })
        >>> plan["name"]
        'Alice'
    """
    calories = int(user_profile.get("calories", 2000))
    name = user_profile.get("name", "User")
    preferences = user_profile.get("preferences", [])

    # Calorie distribution: 30% breakfast, 40% lunch, 30% dinner
    breakfast = int(calories * 0.3)
    lunch = int(calories * 0.4)
    dinner = calories - breakfast - lunch

    plan = {
        "name": name,
        "calories_total": calories,
        "meals": [
            {
                "name": "breakfast",
                "calories": breakfast,
                "items": ["oatmeal", "banana", "greek yogurt"]
            },
            {
                "name": "lunch",
                "calories": lunch,
                "items": ["chicken salad", "brown rice", "mixed vegetables"]
            },
            {
                "name": "dinner",
                "calories": dinner,
                "items": ["salmon", "steamed broccoli", "sweet potato"]
            },
        ],
        "notes": "preferences: {}".format(",".join(preferences) if preferences else "none")
    }
    return plan


def _cli():

    """Command-line interface for diet generator.

    Accepts a JSON string as argument or uses default profile.

    Usage:
        python diet_generator.py
        python diet_generator.py '{"calories": 1800, "name": "Bob"}'
    """
    import json
    import sys

    if len(sys.argv) > 1:
        try:
            profile = json.loads(sys.argv[1])
        except Exception as e:
            print(f"Invalid JSON input: {e}")
            sys.exit(2)
    else:
        profile = {"calories": 1800}

    plan = generate_diet(profile)
    print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
