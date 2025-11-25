# Skill 4 — Diet Generator

目標：建立一個簡單的飲食（diet）產生器 skill，用於根據使用者資料或目標生成每日飲食建議。

檔案結構（初始）：

- `skills/4-diet-generator/`
  - `__init__.py` - 套件匯出
  - `SKILL.md` - 技能說明文件
  - `scripts/diet_generator.py` - 主程式
  - `README.md` - 使用說明
  - `requirements.txt` - 第三方套件列表
  - `.env.example` - 範例環境變數

基本功能：
- `generate_diet(user_profile: dict) -> dict`：回傳簡易飲食建議（JSON 形式）。

進階（未實作）：
- 與營養資料庫整合
- 支援限制性飲食（vegetarian、keto、low-carb）
