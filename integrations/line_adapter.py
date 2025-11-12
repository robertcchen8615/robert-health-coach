"""LINE adapter example: show how to call skill_4_diet_generator from a webhook handler.

This is a minimal example; integrate into your actual LINE webhook handling code.
"""
from typing import Dict
import json

from skills.skill_4_diet_generator.scripts import diet_generator


def handle_line_event(event_body: Dict) -> Dict:
    """Given a parsed LINE webhook event body, generate a diet plan response.

    Expected event_body format (simplified):
      {"user_id": "U123", "message": "generate diet", "profile": {...}}

    Returns a dict that can be converted to a LINE reply payload.
    """
    profile = event_body.get("profile", {})
    plan = diet_generator.generate_diet(profile)

    # Minimal reply text summarizing the plan
    total = plan.get("calories_total")
    breakfast = plan["meals"][0]["calories"]
    lunch = plan["meals"][1]["calories"]
    dinner = plan["meals"][2]["calories"]

    text = (
        f"{plan.get('name', 'User')}, 你的每日總熱量: {total} kcal.\n"
        f"早餐: {breakfast} kcal, 午餐: {lunch} kcal, 晚餐: {dinner} kcal."
    )

    # Example LINE reply (text message)
    reply = {
        "replyToken": event_body.get("replyToken"),
        "messages": [{"type": "text", "text": text}]
    }

    return reply


if __name__ == "__main__":
    # simple local test
    sample_event = {
        "user_id": "U123",
        "message": "generate diet",
        "replyToken": "TEST_TOKEN",
        "profile": {"calories": 2000, "name": "TestUser", "preferences": ["vegetarian"]},
    }
    print(json.dumps(handle_line_event(sample_event), indent=2, ensure_ascii=False))
