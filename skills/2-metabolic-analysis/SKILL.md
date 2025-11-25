---
name: metabolic-analysis
description: 分析每日酮體/血糖/氣酮日誌，找出隱藏碳水與 Randle cycle 現象
version: 1.0.0
tags: [ketosis, glucose, metabolic, daily-tracking]
dependencies: [intake-basic]
---

# Metabolic Analysis - 代謝日誌判讀

## 功能說明
每日分析血糖、血酮、氣酮數據，識別：
1. **隱藏碳水**：血糖異常升高但無明顯碳水攝取
2. **Randle Cycle**：油脂攝取過多導致當日酮體無法上升
3. **適應期指標**：評估生酮適應程度

## 何時使用
- 每日紀錄後進行分析
- 每週回顧趨勢
- 調整飲食計畫前

## 輸入格式
```json
{
  "date": "2025-11-03",
  "fasting_glucose": 92,
  "blood_ketone": 0.6,
  "breath_ketone": 12,
  "meals": [
    {"time": "12:00", "food": "雞胸肉、青菜、橄欖油", "estimated_carbs": 10}
  ],
  "exercise": "太極 30min",
  "notes": "午後有點餓"
}
```

## 詳細分析邏輯
參見 [analysis_guide.md](./analysis_guide.md)

## 工具腳本
- `scripts/analyze_logs.py` - 執行代謝分析與警示