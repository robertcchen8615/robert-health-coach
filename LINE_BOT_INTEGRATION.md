# 📱 LINE Bot 整合指南

## 目錄
1. [架構概述](#架構概述)
2. [快速開始](#快速開始)
3. [命令列表](#命令列表)
4. [Webhook 設置](#webhook-設置)
5. [Skill 整合](#skill-整合)
6. [部署指南](#部署指南)
7. [常見問題](#常見問題)

---

## 架構概述

### 系統架構圖

```
LINE User
    ↓ (訊息)
LINE Messaging API
    ↓ (webhook 回調)
Flask App (/callback)
    ↓ (解析訊息)
命令路由器
    ↓
Skill 4 (飲食計畫)      Skill 2 (代謝分析)    其他 Skills
    ↓                        ↓
生成回覆                   生成報告
    ↓
LINE Bot API (reply_message)
    ↓ (訊息)
LINE User
```

### 核心檔案結構

```
line-bot/
├── app.py                          # 主應用程式
├── config.py                       # 配置常數
└── requirements.txt               # 依賴套件

integrations/
├── line_adapter.py                # Skill 4 LINE adapter
└── metabolic_analysis_adapter.py  # Skill 2 LINE adapter

tests/
└── test_line_bot_app.py          # 單元測試
```

---

## 快速開始

### 1. 取得 LINE Messaging API 憑證

1. 前往 [LINE Developers](https://developers.line.biz/)
2. 建立新的 Provider（提供商）
3. 建立 Messaging API Channel
4. 複製以下資訊：
   - **Channel Access Token** (長期 token)
   - **Channel Secret** (用於簽名驗證)

### 2. 設定環境變數

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here
FLASK_ENV=development
PORT=5000
```

### 3. 安裝依賴

```bash
pip install -r line-bot/requirements.txt
```

### 4. 在本機執行

```bash
python line-bot/app.py
```

輸出應該類似：

```
🚀 啟動 LINE Bot (Port 5000, Debug=True)
Webhook URL: http://localhost:5000/callback
Health check: http://localhost:5000/health
```

### 5. 設定 Webhook URL

在 LINE Developers Console：

1. 進入 Channel Settings
2. 找到 **Messaging API** 標籤
3. 在 **Webhook URL** 欄位，輸入你的伺服器 URL：
   ```
   https://your-domain.com/callback
   ```
4. 點擊 **Verify** 驗證連接
5. 開啟 **Use webhook** 開關

---

## 命令列表

### 🍽️ `/diet` - 飲食計畫生成

生成個人化的每日飲食計畫。

**語法：**
```
/diet [熱量] [偏好...]
```

**參數：**
- `熱量` (可選): 目標每日熱量，預設 2000 kcal
- `偏好...` (可選): 飲食偏好，例如「素食」、「低碳」

**範例：**

```
使用者: /diet
機器人: 🍽️ User_123 的每日飲食計畫
       目標熱量: 2000 kcal
       ...

使用者: /diet 1800 素食 低脂
機器人: 🍽️ User_123 的每日飲食計畫
       目標熱量: 1800 kcal
       飲食偏好: 素食, 低脂
       ...
```

**回覆格式：**

```
🍽️ [名稱] 的每日飲食計畫
━━━━━━━━━━━━━━━
目標熱量: [總熱量] kcal
飲食偏好: [偏好列表]

【早餐】 [熱量] kcal
  • 食物 1
  • 食物 2
  • 食物 3

【午餐】 [熱量] kcal
  • 食物 1
  • 食物 2
  • 食物 3

【晚餐】 [熱量] kcal
  • 食物 1
  • 食物 2
  • 食物 3

📝 [建議訊息]
```

---

### 📊 `/analyze` - 代謝日誌分析

分析血糖、血酮和飲食資料。

**語法：**
```
/analyze
{JSON格式的日誌資料}
```

**輸入格式：**

```json
{
  "date": "2025-11-12",
  "fasting_glucose": 92,
  "blood_ketone": 0.8,
  "breath_ketone": 18,
  "meals": [
    {
      "food": "雞胸肉、青菜、橄欖油",
      "estimated_carbs": 5,
      "fat_g": 35
    }
  ],
  "exercise": "散步 30 分鐘",
  "notes": "感覺不錯"
}
```

**回覆格式：**

```
📊 代謝分析報告
━━━━━━━━━━━━━━━

📅 日期: 2025-11-12

🩸 【血糖分析】
空腹血糖: 92 mg/dL
狀態: ✅ 良好
建議: 在目標範圍內

🧪 【血酮分析】
血酮值: 0.8 mmol/L
狀態: ✅ 營養性酮症（理想範圍）
建議: 保持目前的飲食習慣

[... 其他分析項目 ...]

📈 整體得分: 🌟 9/10
狀態優異！保持目前的飲食和生活習慣。
```

---

### 💬 `/help` - 說明訊息

顯示所有可用命令的說明。

**範例：**

```
使用者: /help
機器人: 🤖 健康教練助手
       📋 可用命令:
       
       🍽️ /diet [熱量] [偏好...]
       ...
```

---

## Webhook 設置

### 本機開發（使用 ngrok）

1. **下載並執行 ngrok：**
   ```bash
   ngrok http 5000
   ```

2. **複製 ngrok URL**，格式如：
   ```
   https://abc123.ngrok.io
   ```

3. **在 LINE Developers 設定 Webhook URL：**
   ```
   https://abc123.ngrok.io/callback
   ```

4. **驗證連接**

### 生產環境

1. **部署應用**（見下方 [部署指南](#部署指南)）

2. **設定 Webhook URL** 為你的 production 域名：
   ```
   https://your-domain.com/callback
   ```

3. **啟用 SSL/TLS**（必須使用 HTTPS）

### 健康檢查

檢查 bot 是否正常運作：

```bash
curl http://localhost:5000/health
```

預期回應：

```json
{
  "status": "healthy",
  "line_bot_api": "configured",
  "skill_4_diet": "loaded",
  "skill_2_metabolic": "loaded"
}
```

---

## Skill 整合

### Skill 4: 飲食計畫生成

**位置：** `integrations/line_adapter.py`

**功能：** 將 `skills.skill_4_diet_generator` 結果轉換為 LINE 訊息格式

**整合流程：**

```
使用者: /diet 2000
    ↓
parse_command() → ("/diet", ["2000"])
    ↓
route_user_message() → 呼叫 handle_diet_command()
    ↓
diet_generator.generate_diet({"calories": 2000})
    ↓
生成飲食計畫 JSON
    ↓
_format_diet_plan_for_line() → 格式化為文本
    ↓
line_bot_api.reply_message() → 發送到 LINE
```

**測試 Skill 4：**

```bash
python integrations/line_adapter.py
```

---

### Skill 2: 代謝分析

**位置：** `integrations/metabolic_analysis_adapter.py`

**功能：** 分析代謝指標並生成健康報告

**支援的指標：**
- 🩸 血糖 (fasting_glucose)
- 🧪 血酮 (blood_ketone)
- 💨 氣酮 (breath_ketone)
- 🍽️ 膳食資訊
- 🏃 運動紀錄

**分析邏輯：**

1. **血糖評估**
   - 70-85 mg/dL: ✅ 優秀
   - 86-95 mg/dL: ✅ 良好
   - 96-110 mg/dL: ⚠️ 偏高
   - >110 mg/dL: 🚨 過高

2. **血酮評估**
   - <0.5 mmol/L: ℹ️ 未入酮
   - 0.5-0.8: ✨ 輕度入酮
   - 0.8-1.5: ✅ 理想範圍
   - 1.5-3.0: 💪 深度酮症
   - >3.0: ⚠️ 過高

3. **警告偵測**
   - 隱藏碳水 (血糖高但碳水低)
   - Randle Cycle (油脂過多導致酮體受阻)

**測試 Skill 2：**

```bash
python integrations/metabolic_analysis_adapter.py
```

---

## 部署指南

### Docker 部署

1. **建立容器：**
   ```bash
   docker build -t health-coach-bot:latest .
   ```

2. **執行容器：**
   ```bash
   docker run -p 5000:5000 \
     -e LINE_CHANNEL_ACCESS_TOKEN=your_token \
     -e LINE_CHANNEL_SECRET=your_secret \
     health-coach-bot:latest
   ```

### 雲端部署

#### Heroku

1. **建立 Heroku 應用**
   ```bash
   heroku create your-app-name
   ```

2. **設定環境變數**
   ```bash
   heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_token
   heroku config:set LINE_CHANNEL_SECRET=your_secret
   ```

3. **部署**
   ```bash
   git push heroku main
   ```

4. **取得 webhook URL**
   ```
   https://your-app-name.herokuapp.com/callback
   ```

#### AWS Lambda + API Gateway

1. 使用 AWS SAM 或 Serverless Framework
2. 配置 API Gateway 路由 POST 到 `/callback`
3. 設定環境變數
4. 部署

### Google Cloud Run

1. **建立 Dockerfile**（已有）

2. **部署**
   ```bash
   gcloud run deploy health-coach-bot \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars "LINE_CHANNEL_ACCESS_TOKEN=your_token,LINE_CHANNEL_SECRET=your_secret"
   ```

3. **取得 URL** 並在 LINE Developers 設定

---

## 常見問題

### Q: Webhook 無法驗證
**A:** 
- 確認 `LINE_CHANNEL_SECRET` 正確
- 檢查伺服器是否正常運作
- 確認 `/callback` 端點可以接收 POST 請求
- 檢查防火牆設定（必須允許 443 埠）

### Q: Bot 無法回覆訊息
**A:**
- 檢查 `LINE_CHANNEL_ACCESS_TOKEN` 是否正確
- 確認 Bot 已加入好友
- 檢查應用日誌中的錯誤訊息
- 確認 Skill 模組已正確載入

### Q: 如何偵錯
**A:**
- 設定 `FLASK_DEBUG=True`
- 檢查日誌：`tail -f logs/app.log`
- 使用 `/health` 檢查狀態
- 在本機用 ngrok 測試

### Q: 如何添加新的 Skill？
**A:**
1. 在 `skills/` 中建立新 Skill
2. 在 `line-bot/app.py` 中匯入 Skill
3. 添加新命令處理函數
4. 在 `route_user_message()` 中添加路由邏輯
5. 建立 `integrations/` 中的 adapter
6. 添加單元測試

### Q: 如何處理用戶資料隱私？
**A:**
- 不要在日誌中記錄個人資訊
- 設定 `LOG_USER_DATA=False`
- 遵守 GDPR 和當地法規
- 定期審查資料保留政策

---

## 測試

### 執行所有 LINE Bot 測試

```bash
pytest tests/test_line_bot_app.py -v
```

### 測試特定命令

```bash
pytest tests/test_line_bot_app.py::TestDietCommand -v
```

### 本機模擬 webhook

```bash
curl -X POST http://localhost:5000/callback \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test_signature" \
  -d '{
    "events": [{
      "type": "message",
      "replyToken": "nHuyWiB7yP5Zw52FIkcQT",
      "source": {"userId": "U4af4980629..."},
      "message": {"type": "text", "text": "/diet 2000"}
    }]
  }'
```

---

## 更新日誌

### v1.0.0 (2025-11-12)

✨ **新增功能**
- ✅ LINE Bot 主應用程式
- ✅ Skill 4 (飲食計畫) 整合
- ✅ Skill 2 (代謝分析) 整合
- ✅ 命令路由系統
- ✅ Webhook 處理

🐛 **修復**
- N/A (初始版本)

---

**需要協助？** 查看 [README.md](../README.md) 或提交 issue。
