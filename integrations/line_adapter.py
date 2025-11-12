"""LINE adapter: 連接 Skill 4 (飲食計畫生成) 到 LINE webhook。

此模組提供將飲食計畫轉換為 LINE 友善訊息格式的功能。
"""
from typing import Dict
import json

from skills.skill_4_diet_generator.scripts import diet_generator


def handle_line_event(event_body: Dict) -> Dict:
    """處理 LINE webhook 事件，生成飲食計畫回覆。

    預期 event_body 格式:
      {
        "user_id": "U123",
        "replyToken": "...",
        "profile": {
          "calories": 2000,
          "name": "Alice",
          "preferences": ["素食"]
        }
      }

    返回: LINE 回覆格式
      {
        "replyToken": "...",
        "messages": [{"type": "text", "text": "..."}]
      }
    """
    profile = event_body.get("profile", {})
    plan = diet_generator.generate_diet(profile)

    # 格式化飲食計畫訊息
    text = _format_diet_plan_for_line(plan)

    # LINE 回覆格式
    reply = {
        "replyToken": event_body.get("replyToken"),
        "messages": [{"type": "text", "text": text}]
    }

    return reply


def _format_diet_plan_for_line(plan: Dict) -> str:
    """將飲食計畫格式化為 LINE 訊息。
    
    參數:
        plan: 由 diet_generator.generate_diet() 返回的計畫字典
    
    返回:
        格式化的訊息文本
    """
    total = plan.get("calories_total", 0)
    name = plan.get("name", "User")
    prefs = ", ".join(plan.get("preferences", [])) if plan.get("preferences") else "無特殊偏好"
    
    text = f"🍽️ {name} 的每日飲食計畫\n"
    text += "━━━━━━━━━━━━━━━\n"
    text += f"目標熱量: {total} kcal\n"
    text += f"飲食偏好: {prefs}\n\n"
    
    for meal in plan.get("meals", []):
        meal_type = meal.get("type", "未知")
        calories = meal.get("calories", 0)
        items = meal.get("items", [])
        
        text += f"【{meal_type}】 {calories} kcal\n"
        for item in items:
            text += f"  • {item}\n"
        text += "\n"
    
    text += f"📝 {plan.get('notes', '祝用餐愉快！')}"
    
    return text


if __name__ == "__main__":
    # 本地測試範例
    sample_event = {
        "user_id": "U123",
        "replyToken": "TEST_TOKEN",
        "profile": {
            "calories": 2000,
            "name": "Alice",
            "preferences": ["素食"]
        },
    }
    result = handle_line_event(sample_event)
    print(json.dumps(result, indent=2, ensure_ascii=False))
