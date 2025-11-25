#!/usr/bin/env python3
"""
Skill 2 (代謝分析) 的 LINE adapter

將代謝分析結果格式化為 LINE Bot 可發送的訊息格式。
"""
from typing import Dict, Any
import json


def analyze_metabolic_log_for_line(log_data: Dict) -> str:
    """分析代謝日誌並返回 LINE 友善的文本格式。

    參數:
        log_data: 包含代謝指標的日誌字典
        結構:
          {
            "date": "2025-11-12",
            "fasting_glucose": 92,
            "blood_ketone": 0.6,
            "breath_ketone": 12,
            "meals": [{"food": "...", "estimated_carbs": 10}],
            "exercise": "太極 30min",
            "notes": "..."
          }

    返回:
        格式化的分析報告字符串
    """
    response = "📊 代謝分析報告\n"
    response += "━━━━━━━━━━━━━━━\n\n"

    # 日期
    date = log_data.get("date", "未知")
    response += f"📅 日期: {date}\n\n"

    # 血糖分析
    glucose = log_data.get("fasting_glucose", 0)
    response += "🩸 【血糖分析】\n"
    response += f"空腹血糖: {glucose} mg/dL\n"

    glucose_status = _get_glucose_status(glucose)
    response += f"狀態: {glucose_status['emoji']} {glucose_status['text']}\n"
    if glucose_status.get("advice"):
        response += f"建議: {glucose_status['advice']}\n"
    response += "\n"

    # 血酮分析
    ketone = log_data.get("blood_ketone", 0)
    response += "🧪 【血酮分析】\n"
    response += f"血酮值: {ketone} mmol/L\n"

    ketone_status = _get_ketone_status(ketone)
    response += f"狀態: {ketone_status['emoji']} {ketone_status['text']}\n"
    if ketone_status.get("advice"):
        response += f"建議: {ketone_status['advice']}\n"
    response += "\n"

    # 氣酮分析（如果有）
    breath_ketone = log_data.get("breath_ketone")
    if breath_ketone is not None:
        response += "💨 【氣酮值】\n"
        response += f"氣酮: {breath_ketone} ppm\n"
        response += "💡 參考: 20-50 ppm 為正常入酮範圍\n\n"

    # 隱藏碳水偵測
    carb_alert = _detect_hidden_carbs(log_data, glucose)
    if carb_alert:
        response += "⚠️ 【警告】\n"
        response += f"{carb_alert}\n\n"

    # Randle Cycle 偵測
    randle_alert = _detect_randle_cycle(log_data, ketone)
    if randle_alert:
        response += "🔍 【Randle Cycle 警告】\n"
        response += f"{randle_alert}\n"
        response += "建議: 單餐油脂控制在 30-40g\n\n"

    # 膳食摘要
    meals = log_data.get("meals", [])
    if meals:
        total_carbs = sum(m.get("estimated_carbs", 0) for m in meals)
        response += f"🍽️ 【膳食摘要】\n"
        response += f"總碳水攝取: {total_carbs}g\n"
        for meal in meals:
            response += f"  • {meal.get('food', '未記錄')} - {meal.get('estimated_carbs', 0)}g 碳水\n"
        response += "\n"

    # 運動記錄
    exercise = log_data.get("exercise")
    if exercise:
        response += f"🏃 運動: {exercise}\n\n"

    # 總體評分
    overall_score = _calculate_overall_score(glucose, ketone)
    response += f"📈 整體得分: {overall_score['emoji']} {overall_score['score']}/10\n"
    response += f"{overall_score['message']}\n"

    # 附註
    notes = log_data.get("notes")
    if notes:
        response += f"\n📝 用戶備註: {notes}\n"

    return response


def _get_glucose_status(glucose: float) -> Dict[str, Any]:
    """評估血糖狀態."""
    if glucose < 70:
        return {
            "emoji": "⚠️",
            "text": "低血糖",
            "advice": "有低血糖風險，注意休息和補充營養"
        }
    elif 70 <= glucose <= 85:
        return {
            "emoji": "✅",
            "text": "優秀",
            "advice": "血糖控制得很好，繼續維持"
        }
    elif 86 <= glucose <= 95:
        return {
            "emoji": "✅",
            "text": "良好",
            "advice": "在目標範圍內"
        }
    elif 96 <= glucose <= 110:
        return {
            "emoji": "⚠️",
            "text": "偏高",
            "advice": "檢查前一晚的碳水攝取"
        }
    else:
        return {
            "emoji": "🚨",
            "text": "過高",
            "advice": "需要調整飲食或就醫評估"
        }


def _get_ketone_status(ketone: float) -> Dict[str, Any]:
    """評估血酮狀態."""
    if ketone < 0.5:
        return {
            "emoji": "ℹ️",
            "text": "未入酮",
            "advice": "建議碳水攝取控制在 <20g/天"
        }
    elif 0.5 <= ketone < 0.8:
        return {
            "emoji": "✨",
            "text": "輕度入酮",
            "advice": "初學者或混搭型飲食"
        }
    elif 0.8 <= ketone <= 1.5:
        return {
            "emoji": "✅",
            "text": "營養性酮症（理想範圍）",
            "advice": "保持目前的飲食習慣"
        }
    elif 1.5 < ketone <= 3.0:
        return {
            "emoji": "💪",
            "text": "深度酮症",
            "advice": "已適應生酮飲食"
        }
    else:
        return {
            "emoji": "⚠️",
            "text": "酮體過高",
            "advice": "排除酮酸中毒風險，必要時就醫"
        }


def _detect_hidden_carbs(log_data: Dict, glucose: float) -> str:
    """偵測隱藏碳水."""
    meals = log_data.get("meals", [])
    declared_carbs = sum(m.get("estimated_carbs", 0) for m in meals)

    # 邏輯: 血糖高但聲稱碳水低
    if glucose > 95 and declared_carbs < 20:
        suspicious = []
        for meal in meals:
            food = meal.get("food", "").lower()
            if any(x in food for x in ["醬", "調味", "水果", "飲料", "加工", "代糖"]):
                suspicious.append(meal.get("food", "未知食物"))

        if suspicious:
            return f"可疑食物: {', '.join(suspicious)}"
        else:
            return "血糖升高但碳水記錄較低，檢查是否有隱藏碳水（如醬料、調味料）"

    return ""


def _detect_randle_cycle(log_data: Dict, ketone: float) -> str:
    """偵測 Randle Cycle（脂肪抗性）."""
    meals = log_data.get("meals", [])
    total_fat = sum(m.get("fat_g", 0) for m in meals)

    # Randle Cycle: 油脂過多導致酮體無法上升
    if total_fat > 150 and ketone < 0.8:
        return f"油脂攝取過多 ({total_fat}g)，可能導致酮體受阻。"

    return ""


def _calculate_overall_score(glucose: float, ketone: float) -> Dict[str, Any]:
    """計算整體健康得分."""
    score = 0

    # 血糖評分 (0-5 分)
    if 70 <= glucose <= 95:
        score += 5
    elif 86 <= glucose <= 110:
        score += 3
    elif glucose >= 110:
        score += 1
    else:
        score += 2

    # 血酮評分 (0-5 分)
    if 0.8 <= ketone <= 1.5:
        score += 5
    elif 0.5 <= ketone < 0.8 or 1.5 < ketone <= 3.0:
        score += 4
    elif ketone >= 3.0:
        score += 2
    else:
        score += 1

    if score >= 8:
        return {
            "score": score,
            "emoji": "🌟",
            "message": "狀態優異！保持目前的飲食和生活習慣。"
        }
    elif score >= 6:
        return {
            "score": score,
            "emoji": "😊",
            "message": "狀態良好，可以稍做調整以進一步優化。"
        }
    elif score >= 4:
        return {
            "score": score,
            "emoji": "😐",
            "message": "需要調整飲食或生活習慣。"
        }
    else:
        return {
            "score": score,
            "emoji": "⚠️",
            "message": "需要立即檢視飲食計畫，考慮尋求專業指導。"
        }


if __name__ == "__main__":
    # 本地測試範例
    sample_log = {
        "date": "2025-11-12",
        "fasting_glucose": 92,
        "blood_ketone": 0.8,
        "breath_ketone": 18,
        "meals": [
            {"food": "蛋、起司、橄欖油", "estimated_carbs": 2, "fat_g": 35},
            {"food": "雞胸肉、堅果、沙拉", "estimated_carbs": 8, "fat_g": 25},
            {"food": "牛肉、青菜、黑巧克力", "estimated_carbs": 5, "fat_g": 40},
        ],
        "exercise": "走路 30 分鐘",
        "notes": "狀態不錯",
    }

    result = analyze_metabolic_log_for_line(sample_log)
    print(result)
