# 患者基本資料表單

## 基本資訊
| 欄位 | 必填 | 格式 | 範例 |
|------|------|------|------|
| patient_id | ✓ | string | "robert_001" |
| age | ✓ | integer | 45 |
| gender | ✓ | "M"/"F" | "M" |
| height_cm | ✓ | float | 175.0 |
| weight_kg | ✓ | float | 86.0 |
| goal | ✓ | string | "6個月減內臟脂肪" |

## 醫療史
| 欄位 | 必填 | 格式 |
|------|------|------|
| cardiac_history | ○ | array of strings |
| chronic_conditions | ○ | array of strings |
| allergies | ○ | array of strings |

## 現用藥物
| 欄位 | 必填 | 格式 |
|------|------|------|
| medications | ○ | array of objects |
| - name | ✓ | string |
| - dosage | ✓ | string |
| - frequency | ✓ | string |

## 檢驗值
| 欄位 | 正常範圍 | 警戒值 |
|------|----------|--------|
| eGFR | ≥60 | <60 需腎臟科監測 |
| HbA1c | <5.7% | ≥6.5% 糖尿病 |
| fasting_glucose | 70-100 | >126 糖尿病 |
| triglycerides | <150 | >200 需注意 |

## 輸出格式 (patient_profile.json)
```json
{
  "patient_id": "robert_001",
  "basic": {
    "age": 45,
    "gender": "M",
    "height_cm": 175.0,
    "weight_kg": 86.0,
    "bmi": 28.1,
    "goal": "6個月減內臟脂肪"
  },
  "medical_history": {
    "cardiac": ["心導管術 x8次", "Valsartan 使用中"],
    "chronic": ["B型肝炎帶原", "第三期慢性腎病 (eGFR 65)"],
    "medications": [
      {"name": "Valsartan", "dosage": "80mg", "frequency": "QD"}
    ]
  },
  "lab_values": {
    "eGFR": 65,
    "HbA1c": 6.1,
    "date": "2025-10-15"
  },
  "restrictions": {
    "sodium": "moderate",
    "sudden_fat_increase": false,
    "intense_cardio": false
  },
  "created_at": "2025-11-03T10:00:00Z"
}
```