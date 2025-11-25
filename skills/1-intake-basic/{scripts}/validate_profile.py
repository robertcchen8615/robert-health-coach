#!/usr/bin/env python3
"""驗證患者檔案的完整性與合理性"""
import json
import sys
from datetime import datetime

def validate_profile(data):
    errors = []
    warnings = []
    
    # 必填欄位檢查
    required_fields = ['patient_id', 'basic', 'medical_history']
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必填欄位: {field}")
    
    # BMI 計算與警示
    if 'basic' in data:
        height_m = data['basic'].get('height_cm', 0) / 100
        weight = data['basic'].get('weight_kg', 0)
        if height_m > 0:
            bmi = weight / (height_m ** 2)
            data['basic']['bmi'] = round(bmi, 1)
            
            if bmi >= 30:
                warnings.append(f"BMI {bmi:.1f} 達肥胖等級")
            elif bmi >= 27:
                warnings.append(f"BMI {bmi:.1f} 為過重")
    
    # 腎功能警示
    if 'lab_values' in data:
        egfr = data['lab_values'].get('eGFR')
        if egfr and egfr < 60:
            warnings.append(f"eGFR {egfr} < 60，需腎臟科監測，飲食需低蛋白")
        
        hba1c = data['lab_values'].get('HbA1c')
        if hba1c and hba1c >= 6.5:
            warnings.append(f"HbA1c {hba1c}% 達糖尿病標準")
    
    # 心血管風險評估
    if 'cardiac' in data.get('medical_history', {}):
        if any('心導管' in item for item in data['medical_history']['cardiac']):
            warnings.append("⚠️ 心血管病史：飲食調整需審慎，禁止過度限鈉")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "data": data
    }

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    result = validate_profile(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))