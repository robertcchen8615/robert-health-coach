"""
LINE Bot 相關設定檔

此模組定義 LINE Bot 的常量和設定。
"""

# LINE Bot 命令
COMMANDS = {
    "DIET": "/diet",           # 飲食計畫生成
    "ANALYZE": "/analyze",     # 代謝日誌分析
    "HELP": "/help",          # 說明訊息
}

# 飲食計畫預設設定
DIET_DEFAULTS = {
    "calories": 2000,
    "preferences": [],
}

# 代謝分析的血糖參考範圍
GLUCOSE_RANGES = {
    "excellent": (70, 85),     # ✅ 優秀
    "good": (86, 95),          # ✅ 良好
    "moderate": (96, 110),     # ⚠️ 中等
    "high": (110, float('inf')),  # 🚨 過高
}

# 代謝分析的血酮參考範圍 (mmol/L)
KETONE_RANGES = {
    "not_in_ketosis": (0, 0.5),
    "mild": (0.5, 0.8),
    "optimal": (0.8, 1.5),
    "deep": (1.5, 3.0),
    "too_high": (3.0, float('inf')),
}

# 氣酮參考範圍 (ppm)
BREATH_KETONE_NORMAL = (20, 50)

# 日誌 levels
LOG_LEVELS = {
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
}

# 使用提示訊息
HELP_MESSAGE = """🤖 健康教練助手
━━━━━━━━━━━━━━━

📋 可用命令:

🍽️ /diet [熱量] [偏好...]
生成每日飲食計畫
例: /diet
例: /diet 2000
例: /diet 2000 素食

📊 /analyze
分析代謝日誌（血糖、血酮）
需要提供 JSON 日誌資料

💬 /help
顯示此訊息

━━━━━━━━━━━━━━━

💡 提示:
• 輸入任何命令開始
• 根據提示提供相關資訊
"""

# 錯誤訊息樣板
ERROR_MESSAGES = {
    "invalid_command": "❌ 未知命令。輸入 /help 查看可用命令",
    "invalid_calories": "❌ 熱量值無效。請輸入數字，例如 /diet 2000",
    "missing_data": "❌ 缺少必要資料",
    "json_error": "❌ JSON 格式錯誤",
    "skill_not_loaded": "❌ Skill 未載入",
}

# 成功訊息樣板
SUCCESS_MESSAGES = {
    "diet_generated": "✅ 飲食計畫已生成",
    "analysis_complete": "✅ 分析完成",
}
