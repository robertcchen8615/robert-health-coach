# 代謝分析判讀指南

## 血糖判讀標準
| 空腹血糖 | 狀態 | 建議 |
|----------|------|------|
| 70-85 | 優秀 | 繼續維持 |
| 86-95 | 良好 | 目標範圍 |
| 96-110 | 偏高 | 檢查前一晚碳水 |
| >110 | 警示 | 需調整飲食或就醫 |

## 血酮判讀標準
| 血酮 (mmol/L) | 狀態 | 說明 |
|---------------|------|------|
| <0.5 | 未入酮 | 需嚴格控碳 |
| 0.5-0.8 | 輕度入酮 | 初學者/混搭型 |
| 0.8-1.5 | 營養性酮症 | 理想範圍 |
| 1.5-3.0 | 深度酮症 | 已適應者 |
| >3.0 | 過高 | 需確認是否酮酸中毒 |

## 隱藏碳水偵測邏輯
```python
def detect_hidden_carbs(log):
    # 規則1：血糖波動 >30 但聲稱低碳
    glucose_spike = log['post_meal_glucose'] - log['fasting_glucose']
    declared_carbs = log['total_carbs']
    
    if glucose_spike > 30 and declared_carbs < 20:
        return "可能隱藏碳水：" + suggest_culprits(log['meals'])
    
    # 規則2：水果、調味料、加工食品
    suspicious_foods = ['水果', '醬料', '加工', '代糖']
    found = [f for f in log['meals'] if any(s in f for s in suspicious_foods)]
    
    if found:
        return f"可疑食物：{', '.join(found)}"
    
    return None
```

## Randle Cycle 判斷
**現象**：脂肪攝取過多 → 細胞優先燃燒脂肪 → 葡萄糖利用下降 → 血糖/血酮都偏低

**識別條件**：
- 當日油脂 >150g
- 血酮 <0.8 且前一日 ≥1.0
- 血糖正常或偏高

**建議**：
- 單餐油脂控制在 30-40g
- 避免「油炸+高脂肉+椰子油」三重奏

## 適應期評估
**週期指標**：
- Week 1-2: 血酮 0.5-1.0（酮流感期）
- Week 3-4: 血酮 0.8-1.5（轉換期）
- Week 5+: 血酮穩定 1.0-2.0（適應期）

**警訊**：
- 持續 >2 週血酮 <0.5 → 碳水未控好
- 血酮 >3.0 持續 3 天 → 需醫師評估