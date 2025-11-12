#!/usr/bin/env python3
"""
Skill 4: Diet Generator - 根據用戶偏好生成個人化飲食計畫

功能：
  - 根據目標熱量與飲食偏好生成每日飲食計畫
  - 支援多種飲食類型（標準、素食、無麩質等）
  - 提供營養建議與食物推薦
"""
import json
import argparse
from typing import Dict, Any, List


def generate_diet(profile: Dict[str, Any]) -> Dict[str, Any]:
    """根據個人資料生成每日飲食計畫。

    參數:
      profile (dict): 包含以下鍵值：
        - calories (int): 目標每日熱量，預設 2000
        - name (str): 用戶名稱，用於個人化
        - preferences (list): 飲食偏好（例如 ["素食", "無麩質"]）

    返回:
      dict: 飲食計畫，包括：
        - calories_total (int): 目標總熱量
        - name (str): 用戶名稱
        - meals (list): 每日餐次列表（早餐、午餐、晚餐 3 餐），每個含：
          - type (str): 餐次類型（早餐、午餐、晚餐）
          - calories (int): 該餐的熱量配置
          - items (list): 推薦食物清單
        - preferences (list): 飲食偏好
        - notes (str): 營養建議

    範例:
      >>> profile = {"calories": 2000, "name": "Alice", "preferences": ["素食"]}
      >>> plan = generate_diet(profile)
      >>> print(plan["meals"][0]["type"])
      早餐
    """
    calories = int(profile.get("calories", 2000))
    preferences = profile.get("preferences", [])
    name = profile.get("name", "Friend")

    # 驗證熱量
    if calories < 500 or calories > 5000:
        return {
            "error": f"熱量值超出範圍 (500-5000): {calories}",
            "calories_total": calories,
            "name": name,
            "meals": [],
            "preferences": preferences,
            "notes": "請輸入 500-5000 之間的熱量值。",
        }

    # 定義餐次結構與熱量分配（早餐 30%、午餐 40%、晚餐 30%）
    meal_structure = [
        {"type": "早餐", "ratio": 0.30},
        {"type": "午餐", "ratio": 0.40},
        {"type": "晚餐", "ratio": 0.30},
    ]

    # 食物資料庫（按飲食偏好分類）
    food_database = {
        "all": {
            "早餐": [
                "燕麥粥 (150g)",
                "全麥麵包 (2 片)",
                "雞蛋 (2 顆)",
                "番茄 (1 個)",
                "藍莓 (100g)",
                "優格 (150ml)",
            ],
            "午餐": [
                "糙米飯 (150g)",
                "雞胸肉 (100g)",
                "花椰菜 (150g)",
                "胡蘿蔔 (100g)",
                "橄欖油 (1 湯匙)",
                "鮭魚 (80g)",
            ],
            "晚餐": [
                "白米飯 (120g)",
                "瘦牛肉 (100g)",
                "地瓜 (150g)",
                "菠菜 (150g)",
                "洋蔥 (80g)",
                "蘑菇 (100g)",
            ],
        },
        "vegetarian": {
            "早餐": ["燕麥粥", "豆漿", "全麥麵包", "莓果", "優格"],
            "午餐": ["豆類飯", "豆腐", "蔬菜", "糙米", "堅果"],
            "晚餐": ["蕎麥麵", "毛豆", "時令蔬菜", "地瓜", "芝麻"],
        },
        "vegan": {
            "早餐": ["燕麥粥", "豆漿", "全麥麵包", "莓果"],
            "午餐": ["豆類飯", "豆腐", "蔬菜", "糙米"],
            "晚餐": ["蕎麥麵", "毛豆", "時令蔬菜", "地瓜"],
        },
        "gluten-free": {
            "早餐": ["米粥", "玉米片", "雞蛋", "藍莓", "堅果奶"],
            "午餐": ["白米飯", "雞肉", "蔬菜", "馬鈴薯", "橄欖油"],
            "晚餐": ["米麵", "魚肉", "番薯", "蔬菜", "酪梨"],
        },
    }

    # 生成每日飲食計畫
    meals: List[Dict[str, Any]] = []
    for meal_info in meal_structure:
        meal_type = meal_info["type"]
        meal_calories = round(calories * meal_info["ratio"])

        # 選擇食物（考慮偏好）
        food_options = food_database.get("all", {}).get(meal_type, [])
        for pref in preferences:
            if pref in food_database and meal_type in food_database[pref]:
                food_options = food_database[pref][meal_type]
                break

        # 構建餐次 — 必須包含 'type' 鍵
        meal: Dict[str, Any] = {
            "type": meal_type,
            "calories": meal_calories,
            "items": food_options[:3] if food_options else ["(暫無推薦)"],
        }
        meals.append(meal)

    # 組合最終計畫
    pref_str = f"preferences: {', '.join(preferences)}" if preferences else "preferences: none"
    plan: Dict[str, Any] = {
        "calories_total": calories,
        "name": name,
        "meals": meals,
        "preferences": preferences if preferences else ["none"],
        "notes": f"👤 {name}, 這是為你量身訂製的飲食計畫。{pref_str}\n請根據個人口味調整，並保持充足水分攝取！",
    }

    return plan


def main():
    """CLI 主函式 - 接受命令行參數並生成飲食計畫."""
    parser = argparse.ArgumentParser(
        description="生成個人化飲食計畫",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  python diet_generator.py '{"calories": 2000}'
  python diet_generator.py '{"calories": 1800, "preferences": ["素食"]}'
  python diet_generator.py '{"calories": 2500, "name": "Bob", "preferences": ["無麩質"]}'
        """,
    )

    parser.add_argument(
        "profile",
        nargs="?",
        default='{"calories": 2000}',
        help='JSON 格式的用戶資料 (預設: {"calories": 2000})',
    )

    args = parser.parse_args()

    try:
        # 解析 JSON 輸入
        profile = json.loads(args.profile)

        # 生成飲食計畫
        plan = generate_diet(profile)

        # 輸出結果
        print(json.dumps(plan, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")
        example = '{"calories": 2000}'
        print(f"請使用有效的 JSON 格式，例如: {example}")
        exit(1)
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        exit(1)


if __name__ == "__main__":
    main()
