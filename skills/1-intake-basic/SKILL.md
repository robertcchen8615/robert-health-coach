---
name: intake-basic
description: 標準化患者基本資料，建立健康檔案 JSON，供其他 skills 使用
version: 1.0.0
tags: [profile, intake, medical-history]
---

# Intake Basic - 患者基本資料建檔

## 功能說明
將患者的基本資料（年齡、體重、目標、病史、用藥、檢驗值）標準化為 JSON 格式，作為所有其他 skills 的基礎數據源。

## 何時使用
- 首次建立患者檔案
- 更新患者基本資料
- 其他 skill 需要讀取患者檔案時

## 使用方式
提供以下資訊：
- 年齡、性別、體重、身高
- 健康目標（例：6個月減內臟脂肪）
- 病史（例：心導管 8 次、肝炎 B）
- 現用藥物
- 重要檢驗值（eGFR, HbA1c 等）

## 詳細表單
參見 [form.md](./form.md)

## 工具腳本
- `scripts/validate_profile.py` - 驗證資料完整性與合理性