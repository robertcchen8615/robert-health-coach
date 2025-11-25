# 🚀 LINE Bot 快速開始指南

## 5 分鐘快速開始

### 1️⃣ 準備 LINE Messaging API 憑證

- 前往 https://developers.line.biz/
- 建立 Messaging API Channel
- 複製 **Channel Access Token** 和 **Channel Secret**

### 2️⃣ 設定環境變數

```bash
cp .env.example .env
```

編輯 `.env`：
```env
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here
```

### 3️⃣ 安裝依賴

```bash
pip install -r line-bot/requirements.txt
```

### 4️⃣ 啟動應用

```bash
python line-bot/app.py
```

輸出：
```
🚀 啟動 LINE Bot (Port 5000, Debug=True)
Webhook URL: http://localhost:5000/callback
Health check: http://localhost:5000/health
```

### 5️⃣ 設定 Webhook URL

#### 本地測試（使用 ngrok）

```bash
ngrok http 5000
```

複製 ngrok URL（例如 `https://abc123.ngrok.io`）

在 LINE Developers Console：
1. Messaging API 設定
2. **Webhook URL**: `https://abc123.ngrok.io/callback`
3. **Verify** → 驗證成功 ✅
4. 啟用 **Use webhook**

#### 生產環境

在 LINE Developers Console：
1. **Webhook URL**: `https://your-domain.com/callback`
2. **Verify** → 驗證成功 ✅
3. 啟用 **Use webhook**

---

## 📱 使用 LINE Bot

### 新增 Bot 為好友

在 LINE Developers Console，找到 Bot 的 **QR Code**，用 LINE App 掃描

### 試試命令

#### 命令 1️⃣：生成飲食計畫
```
使用者: /diet 2000 素食
機器人: 🍽️ User_xxx 的每日飲食計畫
       目標熱量: 2000 kcal
       飲食偏好: 素食
       ...
```

#### 命令 2️⃣：分析代謝
```
使用者: /analyze
       {
         "date": "2025-11-12",
         "fasting_glucose": 85,
         "blood_ketone": 0.8,
         "meals": [...]
       }
機器人: 📊 代謝分析報告
       ...
```

#### 命令 3️⃣：顯示說明
```
使用者: /help
機器人: 🤖 健康教練助手
       📋 可用命令:
       ...
```

---

## 🧪 測試

### 執行所有 LINE Bot 測試

```bash
pytest tests/test_line_bot_app.py tests/test_line_bot_integration.py -v
```

### 檢查 Health Check

```bash
curl http://localhost:5000/health
```

回應：
```json
{
  "status": "healthy",
  "line_bot_api": "configured",
  "skill_4_diet": "loaded",
  "skill_2_metabolic": "loaded"
}
```

---

## 🐳 Docker 部署

### 建立並執行容器

```bash
docker build -t health-coach-bot:latest .
docker run -p 5000:5000 \
  -e LINE_CHANNEL_ACCESS_TOKEN=your_token \
  -e LINE_CHANNEL_SECRET=your_secret \
  health-coach-bot:latest
```

---

## 🌐 雲端部署

### Heroku（最簡單）

```bash
# 登入 Heroku
heroku login

# 建立應用
heroku create your-app-name

# 設定環境變數
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
heroku config:set LINE_CHANNEL_SECRET=your_secret

# 部署
git push heroku main

# 取得 URL
heroku apps:info
# Webhook URL: https://your-app-name.herokuapp.com/callback
```

### AWS Lambda + API Gateway

1. 使用 AWS Serverless Application Model (SAM)
2. 配置 API Gateway 路由 POST `/callback`
3. 設定環境變數
4. 部署

### Google Cloud Run

```bash
gcloud run deploy health-coach-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "LINE_CHANNEL_ACCESS_TOKEN=your_token,LINE_CHANNEL_SECRET=your_secret"
```

取得 URL 並設定 Webhook

---

## 📋 檔案清單

| 檔案                                         | 說明                 |
| -------------------------------------------- | -------------------- |
| `line-bot/app.py`                            | 主應用程式 (550+ 行) |
| `line-bot/config.py`                         | 配置常數             |
| `line-bot/requirements.txt`                  | 依賴套件             |
| `integrations/line_adapter.py`               | Skill 4 adapter      |
| `integrations/metabolic_analysis_adapter.py` | Skill 2 adapter      |
| `tests/test_line_bot_app.py`                 | 單元測試             |
| `tests/test_line_bot_integration.py`         | 整合測試             |
| `LINE_BOT_INTEGRATION.md`                    | 完整文檔 (300+ 行)   |
| `.env.example`                               | 環境變數範本         |

---

## 🆘 常見問題

### Q: Webhook 無法驗證？
**A:**
- 確認 `LINE_CHANNEL_SECRET` 正確
- 確認伺服器正常運作
- 檢查防火牆設定（允許 443 埠）
- 使用 ngrok 本地測試

### Q: Bot 無法回覆？
**A:**
- 檢查 `LINE_CHANNEL_ACCESS_TOKEN` 是否正確
- 確認 Bot 已加入好友
- 檢查 `/health` 端點
- 查看應用日誌

### Q: 如何偵錯？
**A:**
- 設定 `FLASK_DEBUG=True`
- 查看應用日誌
- 使用 ngrok 本地測試
- 執行 `/health` 檢查狀態

---

## 📚 進階功能

### 新增自訂命令

編輯 `line-bot/app.py` 的 `route_user_message()` 函數：

```python
elif command == "/mycommand":
    return my_command_handler(user_id, args)
```

### 新增新的 Skill

1. 建立 `skills/skill_X/`
2. 在 `line-bot/app.py` 中匯入
3. 建立 `integrations/skill_X_adapter.py`
4. 在路由系統中添加處理

### 修改飲食計畫格式

編輯 `integrations/line_adapter.py` 的 `_format_diet_plan_for_line()` 函數

---

## 🔗 相關資源

- [LINE Messaging API 文檔](https://developers.line.biz/en/docs/messaging-api/)
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- [Flask 文檔](https://flask.palletsprojects.com/)
- [完整 LINE Bot 整合指南](./LINE_BOT_INTEGRATION.md)

---

**需要幫助？** 查看 [README.md](./README.md) 或 [LINE_BOT_INTEGRATION.md](./LINE_BOT_INTEGRATION.md)
