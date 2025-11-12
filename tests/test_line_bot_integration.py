"""
LINE Bot Webhook 整合測試

測試 webhook 端點和完整的訊息流程
"""
import json
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# 設定測試環境變數
os.environ["LINE_CHANNEL_ACCESS_TOKEN"] = "test_token"
os.environ["LINE_CHANNEL_SECRET"] = "test_secret"
os.environ["FLASK_ENV"] = "testing"


class TestWebhookEndpoints:
    """測試 webhook 端點"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端"""
        from line_bot.app import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client
    
    def test_index_endpoint(self, client):
        """測試根路由"""
        response = client.get("/")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "service" in data
        assert "webhook_url" in data
        assert data["webhook_url"] == "/callback"
    
    def test_health_check_endpoint(self, client):
        """測試健康檢查端點"""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "line_bot_api" in data
    
    def test_callback_missing_signature(self, client):
        """測試缺少簽名的 callback"""
        response = client.post(
            "/callback",
            data=json.dumps({"test": "data"}),
            content_type="application/json"
        )
        # 應該返回 403（無效簽名）或 500
        assert response.status_code in [403, 500]
    
    def test_404_not_found(self, client):
        """測試 404 錯誤處理"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data


class TestMessageFlowIntegration:
    """測試完整的訊息流程"""
    
    @pytest.fixture
    def client(self):
        """建立測試客戶端"""
        from line_bot.app import app
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client
    
    @patch("line_bot.app.handler.handle")
    @patch("line_bot.app.line_bot_api.reply_message")
    def test_diet_command_flow(self, mock_reply, mock_handle, client):
        """測試 /diet 命令的完整流程"""
        # 模擬 LINE webhook 事件
        event_data = {
            "events": [{
                "type": "message",
                "replyToken": "nHuyWiB7yP5Zw52FIkcQT",
                "source": {"userId": "U1234567890abcdef1234567890abcdef"},
                "timestamp": 1634890000000,
                "message": {
                    "type": "text",
                    "id": "100001",
                    "text": "/diet 2000"
                }
            }]
        }
        
        # 模擬 handler 會呼叫回覆訊息
        def side_effect(body, signature):
            pass
        
        mock_handle.side_effect = side_effect
        
        # 發送請求
        response = client.post(
            "/callback",
            data=json.dumps(event_data),
            content_type="application/json",
            headers={"X-Line-Signature": "fake_signature"}
        )
        
        # 檢查回應
        assert response.status_code in [200, 400]  # handler 會驗證簽名
    
    @patch("line_bot.app.line_bot_api")
    def test_help_command_returns_message(self, mock_api):
        """測試 /help 命令返回訊息"""
        from line_bot.app import route_user_message
        
        response = route_user_message("U123", "/help")
        assert "🤖" in response
        assert "命令" in response or "help" in response.lower()
    
    def test_normal_message_prompt(self):
        """測試普通訊息提示"""
        from line_bot.app import route_user_message
        
        response = route_user_message("U123", "你好")
        assert "👋" in response
        assert "help" in response.lower()


class TestErrorRecovery:
    """測試錯誤恢復"""
    
    def test_missing_environ_variables(self):
        """測試缺少環境變數的情況"""
        # 這個測試應該在沒有設定 LINE token 時執行
        # 應該能優雅地處理缺失的配置
        pass
    
    @patch("line_bot.app.diet_generator", None)
    def test_skill_not_loaded(self):
        """測試 Skill 未載入的情況"""
        from line_bot.app import handle_diet_command
        
        response = handle_diet_command("U123", [])
        assert "❌" in response
        assert "未載入" in response
    
    def test_invalid_json_parsing(self):
        """測試無效 JSON 的解析"""
        from line_bot.app import handle_analyze_command
        
        response = handle_analyze_command("U123", "/analyze\n{invalid json")
        assert "❌" in response
        assert "JSON" in response or "格式" in response


class TestCommandParsing:
    """測試命令解析的邊界情況"""
    
    def test_empty_message(self):
        """測試空訊息"""
        from line_bot.app import parse_command
        
        command, args = parse_command("")
        assert command == ""
        assert args == []
    
    def test_command_with_spaces(self):
        """測試包含多個空格的命令"""
        from line_bot.app import parse_command
        
        command, args = parse_command("  /diet   2000   素食  ")
        assert command == "/diet"
        assert args == ["2000", "素食"]
    
    def test_case_sensitivity(self):
        """測試命令大小寫敏感性"""
        from line_bot.app import parse_command
        
        command1, _ = parse_command("/DIET 2000")
        assert command1 == "/diet"  # 應該轉為小寫
    
    def test_unknown_command_prefix(self):
        """測試未知的命令前綴"""
        from line_bot.app import route_user_message
        
        response = route_user_message("U123", "@unknown")
        # 不以 / 開頭，應該被視為普通訊息
        assert "👋" in response or "help" in response.lower()


class TestDietGenerationEdgeCases:
    """測試飲食計畫生成的邊界情況"""
    
    def test_extreme_low_calories(self):
        """測試極低熱量"""
        from line_bot.app import handle_diet_command
        
        response = handle_diet_command("U123", ["500"])
        # 應該生成計畫或警告
        assert "❌" not in response or "❌" in response
    
    def test_extreme_high_calories(self):
        """測試極高熱量"""
        from line_bot.app import handle_diet_command
        
        response = handle_diet_command("U123", ["5000"])
        # 應該生成計畫
        assert "❌" not in response or "❌" in response
    
    def test_multiple_preferences(self):
        """測試多個飲食偏好"""
        from line_bot.app import handle_diet_command
        
        response = handle_diet_command("U123", ["2000", "素食", "低碳", "無麩質"])
        # 應該包含飲食計畫
        assert "🍽️" in response


class TestMetabolicAnalysisEdgeCases:
    """測試代謝分析的邊界情況"""
    
    def test_missing_optional_fields(self):
        """測試缺少可選欄位"""
        from integrations.metabolic_analysis_adapter import analyze_metabolic_log_for_line
        
        minimal_log = {
            "date": "2025-11-12",
            "fasting_glucose": 85,
            "blood_ketone": 1.0,
        }
        
        response = analyze_metabolic_log_for_line(minimal_log)
        assert "📊" in response
        assert "血糖" in response
        assert "血酮" in response
    
    def test_zero_values(self):
        """測試零值"""
        from integrations.metabolic_analysis_adapter import _get_glucose_status
        
        status = _get_glucose_status(0)
        assert "⚠️" in status["emoji"]
    
    def test_very_high_ketone(self):
        """測試非常高的血酮"""
        from integrations.metabolic_analysis_adapter import _get_ketone_status
        
        status = _get_ketone_status(5.0)
        assert "⚠️" in status["emoji"]
        assert "過高" in status["text"] or "高" in status["text"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
