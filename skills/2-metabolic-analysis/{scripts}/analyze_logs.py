#!/usr/bin/env python3
"""代謝日誌分析腳本"""
import json
import sys
from datetime import datetime, timedelta

def analyze_metabolic_log(log, profile):
    results = {
        "date": log["date"],
        "scores": {},
        "alerts": [],
        "insights": []
    }
    
    # 血糖評分
    fg = log.get("fasting_glucose", 0)
    if fg < 70:
        results["alerts"].append("⚠️ 低血糖風險")
        results["scores"]["glucose"] = "low"
    elif 70 <= fg <= 85:
        results["scores"]["glucose"] = "excellent"
    elif 86 <= fg <= 95:
        results["scores"]["glucose"] = "good"
    elif 96 <= fg <= 110:
        results["scores"]["glucose"] = "moderate"
        results["alerts"].append("血糖偏高，檢查前一晚碳水")
    else:
        results["scores"]["glucose"] = "high"
        results["alerts"].append("⚠️ 血糖過高，需就醫評估")
    
    # 血酮評分
    bk = log.get("blood_ketone", 0)
    if bk < 0.5:
        results["scores"]["ketone"] = "not_in_ketosis"
        results["insights"].append("未入酮，建議碳水 <20g/天")
    elif 0.5 <= bk < 0.8:
        results["scores"]["ketone"] = "mild"
    elif 0.8 <= bk <= 1.5:
        results["scores"]["ketone"] = "optimal"
        results["insights"].append("✅ 理想酮體範圍")
    elif 1.5 < bk <= 3.0:
        results["scores"]["ketone"] = "deep"
    else:
        results["scores"]["ketone"] = "too_high"
        results["alerts"].append("⚠️ 酮體過高，排除酮酸中毒")
    
    # Randle Cycle 偵測
    total_fat = sum(m.get("fat_g", 0) for m in log.get("meals", []))
    if total_fat > 150 and bk < 0.8:
        results["alerts"].append("🔍 疑似 Randle Cycle：油脂過多導致酮體受阻")
        results["insights"].append("建議：單餐油脂控制在 30-40g")
    
    # 隱藏碳水偵測
    declared_carbs = sum(m.get("estimated_carbs", 0) for m in log.get("meals", []))
    if fg > 95 and declared_carbs < 20:
        results["alerts"].append("🔍 可能有隱藏碳水（調味料、加工食品、水果）")
    
    # 心血管安全檢查（for Robert's case）
    if profile.get("medical_history", {}).get("cardiac"):
        if log.get("chest_discomfort") or log.get("abnormal_hr"):
            results["alerts"].append("🚨 心血管症狀，立即停止運動並就醫")
    
    return results

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    log = input_data["log"]
    profile = input_data.get("profile", {})
    
    result = analyze_metabolic_log(log, profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))