#!/usr/bin/env python3
"""
LINE Bot 主應用程式 - 連接 webhook 到各 Skill

功能：
  - 接收 LINE webhook 事件
  - 根據用戶訊息路由到對應 Skill
  - 整合 Skill 4 (Diet Generator) 和 Skill 2 (Metabolic Analysis)
  - 返回 LINE 回覆訊息
"""
import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 載入環境變數
load_dotenv()

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 建立 Flask app
app = Flask(__name__)

# LINE Bot 配置
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    logger.warning(
        "⚠️ LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設定。"
        "請在 .env 檔案中設定。"
    )

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN) if CHANNEL_ACCESS_TOKEN else None
handler = WebhookHandler(CHANNEL_SECRET) if CHANNEL_SECRET else None

# 匯入各 Skill 模組
try:
    from skills.skill_4_diet_generator.scripts import diet_generator
    logger.info("✅ 成功載入 Skill 4 (Diet Generator)")
except ImportError as e:
    logger.error(f"❌ 無法載入 Skill 4: {e}")
    diet_generator = None

try:
    from integrations.metabolic_analysis_adapter import (
        analyze_metabolic_log_for_line,
    )
    logger.info("✅ 成功載入 Skill 2 (Metabolic Analysis)")
except ImportError as e:
    logger.error(f"❌ 無法載入 Skill 2: {e}")
    analyze_metabolic_log_for_line = None


# ============================================================================
# 命令路由系統
# ============================================================================
def parse_command(text: str) -> tuple[str, list]:
    """解析用戶訊息中的命令與參數。

    支援格式：
      - "/diet" - 使用預設設置生成飲食計畫
      - "/diet 2000" - 指定熱量 2000 kcal
      - "/diet 2000 素食" - 指定熱量和飲食偏好
      - "/analyze" - 分析代謝日誌（需提供 JSON 資料）
      - "/help" - 顯示說明

    返回: (command, args)
    """
    parts = text.strip().split()
    if not parts:
        return ("", [])

    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return (command, args)


def handle_diet_command(user_id: str, args: list) -> str:
    """處理 /diet 命令 - 生成飲食計畫。

    使用 Skill 4 生成每日飲食計畫。

    參數:
      - args[0] (可選): 熱量 (預設 2000)
      - args[1] (可選): 飲食偏好 (例如 "素食", "低碳")

    返回: 格式化的飲食計畫訊息
    """
    if diet_generator is None:
        return "❌ Skill 4 (飲食計畫生成) 未載入。請檢查環境設定。"

    try:
        # 解析參數
        calories = 2000
        preferences = []

        if len(args) > 0:
            try:
                calories = int(args[0])
            except ValueError:
                return f"❌ 熱量值無效: {args[0]}。請輸入數字，例如 /diet 2000"

        if len(args) > 1:
            preferences = args[1:]

        # 生成飲食計畫
        profile = {
            "calories": calories,
            "name": f"User_{user_id[-4:]}",
            "preferences": preferences,
        }

        plan = diet_generator.generate_diet(profile)

        # 格式化回覆訊息
        response = f"🍽️ {plan['name']} 的每日飲食計畫\n"
        response += f"━━━━━━━━━━━━━━━\n"
        response += f"每日總熱量: {plan['calories_total']} kcal\n"
        pref_str = (", ".join(plan.get("preferences", ["無"]))
                    if plan.get("preferences") and plan.get("preferences") != ["none"]
                    else "無")
        response += f"飲食偏好: {pref_str}\n\n"

        for meal in plan["meals"]:
            response += f"【{meal['type']}】 {meal['calories']} kcal\n"
            for food in meal["items"]:
                response += f"  • {food}\n"
            response += "\n"

        response += f"📝 {plan.get('notes', '盡量喝水，適度運動！')}"

        return response

    except Exception as e:
        logger.error(f"diet_command 錯誤: {e}", exc_info=True)
        return f"❌ 生成飲食計畫時出錯: {str(e)}"


def handle_analyze_command(user_id: str, body_text: str) -> str:
    """處理 /analyze 命令 - 分析代謝日誌。

    預期用戶在訊息中附加 JSON 格式的日誌資料。

    格式:
      /analyze
      {
        "date": "2025-11-12",
        "fasting_glucose": 92,
        "blood_ketone": 0.6,
        "meals": [...]
      }

    返回: 代謝分析結果
    """
    if analyze_metabolic_log_for_line is None:
        return "❌ Skill 2 (代謝分析) 未載入。"

    try:
        # 從訊息中提取 JSON
        lines = body_text.split('\n', 1)
        if len(lines) < 2:
            return (
                "❌ 缺少日誌資料。\n"
                "格式: /analyze\n"
                "{JSON 格式的日誌資料}"
            )

        json_str = lines[1]
        log_data = json.loads(json_str)

        # 呼叫 Skill 2
        result = analyze_metabolic_log_for_line(log_data)

        return result

    except json.JSONDecodeError as e:
        return f"❌ JSON 格式錯誤: {str(e)}"
    except Exception as e:
        logger.error(f"analyze_command 錯誤: {e}", exc_info=True)
        return f"❌ 分析日誌時出錯: {str(e)}"


def handle_help_command() -> str:
    """顯示可用命令說明。"""
    help_text = (
        "🤖 健康教練 Bot 說明\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "📋 可用命令:\n\n"
        "🍽️ /diet [熱量] [偏好]\n"
        "生成每日飲食計畫\n"
        "例: /diet\n"
        "例: /diet 2000\n"
        "例: /diet 2000 素食\n\n"
        "📊 /analyze\n"
        "分析代謝日誌（血糖、血酮）\n"
        "需要提供 JSON 格式的日誌資料\n\n"
        "💬 /help\n"
        "顯示此說明訊息\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "💡 提示: 輸入命令後，根據提示提供相關資訊。"
    )
    return help_text


def route_user_message(user_id: str, text: str) -> str:
    """根據用戶訊息路由到對應 Skill。

    邏輯:
      1. 解析命令
      2. 檢查是否為內建命令 (/diet, /analyze, /help)
      3. 執行對應的 Skill 或顯示錯誤

    返回: 回覆訊息
    """
    command, args = parse_command(text)

    if command == "/diet":
        return handle_diet_command(user_id, args)
    elif command == "/analyze":
        return handle_analyze_command(user_id, text)
    elif command == "/help":
        return handle_help_command()
    elif command.startswith("/"):
        return (
            f"❌ 未知命令: {command}\n"
            "輸入 /help 查看可用命令"
        )
    else:
        # 普通訊息 - 提示用戶
        return (
            "👋 你好！\n"
            "我是健康教練助手，可以幫助你：\n\n"
            "🍽️ 生成個人飲食計畫\n"
            "📊 分析代謝指標\n\n"
            "輸入 /help 了解更多命令"
        )


# ============================================================================
# Webhook 事件處理
# ============================================================================
def handle_message(event):
    """處理 LINE TextMessage 事件."""
    try:
        user_id = event.source.user_id
        user_message = event.message.text

        logger.info(f"📨 收到來自 {user_id} 的訊息: {user_message}")

        # 路由訊息到對應 Skill
        reply_text = route_user_message(user_id, user_message)

        # 發送回覆
        if line_bot_api:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
            logger.info(f"✅ 已回覆 {user_id}")
        else:
            logger.warning("⚠️ LINE Bot API 未初始化")

    except LineBotApiError as e:
        logger.error(f"LINE API 錯誤: {e.status_code} {e.error.message}")
    except Exception as e:
        logger.error(f"訊息處理錯誤: {e}", exc_info=True)


# 延遲註冊 handler（避免 handler is None 錯誤）
if handler:
    handler.add(MessageEvent, message=TextMessage)(handle_message)


# ============================================================================
# HTTP 路由
# ============================================================================
@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook 回調端點.

    預期請求:
      - Content-Type: application/json
      - Body: LINE webhook 事件 JSON
      - Headers: X-Line-Signature (簽名驗證)

    返回: 200 OK
    """
    # 取得請求簽名與內容
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    logger.info(f"📥 收到 webhook: {body[:100]}...")

    if not handler:
        return jsonify({"error": "Handler 未初始化"}), 500

    try:
        handler.handle(body, signature)
        return jsonify({"status": "ok"}), 200
    except InvalidSignatureError:
        logger.error("❌ 無效簽名")
        return jsonify({"error": "Invalid signature"}), 403
    except Exception as e:
        logger.error(f"❌ Webhook 處理錯誤: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """健康檢查端點."""
    status = {
        "status": "healthy",
        "line_bot_api": "configured" if line_bot_api else "not_configured",
        "skill_4_diet": "loaded" if diet_generator else "not_loaded",
        "skill_2_metabolic": "loaded" if analyze_metabolic_log_for_line else "not_loaded",
    }
    return jsonify(status), 200


@app.route("/", methods=["GET"])
def index():
    """根路由 - 顯示歡迎訊息."""
    return jsonify({
        "service": "robert-health-coach LINE Bot",
        "version": "1.0.0",
        "webhook_url": "/callback",
        "health_check": "/health",
    }), 200


# ============================================================================
# 錯誤處理
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    """404 錯誤處理."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 錯誤處理."""
    logger.error(f"內部伺服器錯誤: {error}")
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# 應用啟動
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"

    logger.info(f"🚀 啟動 LINE Bot (Port {port}, Debug={debug})")
    logger.info(f"Webhook URL: http://localhost:{port}/callback")
    logger.info("Health check: http://localhost:{}/health".format(port))

    app.run(host="0.0.0.0", port=port, debug=debug)
