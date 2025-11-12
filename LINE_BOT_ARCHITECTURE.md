# 📐 LINE Bot 系統架構

## 完整系統架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                           LINE User                              │
└──────────────────────────────────────────────────────────────────┘
                                 │
                         (訊息, /diet, /analyze)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LINE Messaging API Cloud                       │
│                  (line.me webhook infrastructure)                │
└──────────────────────────────────────────────────────────────────┘
                                 │
                    (POST webhook event body)
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Flask Web Application                          │
│                      line-bot/app.py                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ GET  /              (welcome message)                      │  │
│  │ POST /callback      (webhook endpoint - main entry)        │  │
│  │ GET  /health        (health check status)                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                                 │
                    (webhook event handler)
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Command Router & Parser                          │
│              (route_user_message function)                       │
│                                                                   │
│  Text: "/diet 2000 素食"                                        │
│         ↓                                                         │
│    parse_command()                                               │
│         ↓                                                         │
│    ("/diet", ["2000", "素食"])                                  │
└──────────────────────────────────────────────────────────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
    /diet       │    /analyze    │    /help       │
    ▼           │       ▼        │     ▼          │
                │                │                │
    ┌───────────────────┐  ┌──────────────────┐  │
    │  handle_diet_     │  │handle_analyze_   │  │
    │   command()       │  │  command()       │  │
    │                   │  │                  │  │
    │ validate args     │  │ parse JSON       │  │
    │ call Skill 4      │  │ call Skill 2     │  │
    │ format result     │  │ format result    │  │
    └───────────────────┘  └──────────────────┘  │
            │                      │              │
            ▼                      ▼              │ /help
    ┌─────────────────────────────────────────┐  │
    │  Skill Integration Layer                │  │
    │  integrations/                          │  │
    └─────────────────────────────────────────┘  │
            │                      │              │
            ▼                      ▼              ▼
    ┌─────────────────────────────────────────┐
    │  Skills  (Business Logic)               │
    │                                         │
    │  ┌──────────────────────────────────┐   │
    │  │ Skill 4: Diet Generator          │   │
    │  │ - Generate meal plans            │   │
    │  │ - Support preferences            │   │
    │  │ - Calorie allocation (30/40/30)  │   │
    │  └──────────────────────────────────┘   │
    │                                         │
    │  ┌──────────────────────────────────┐   │
    │  │ Skill 2: Metabolic Analysis      │   │
    │  │ - Glucose evaluation             │   │
    │  │ - Ketone analysis                │   │
    │  │ - Hidden carb detection          │   │
    │  │ - Randle cycle detection         │   │
    │  │ - Overall health score           │   │
    │  └──────────────────────────────────┘   │
    │                                         │
    │  (Other Skills as needed...)            │
    └─────────────────────────────────────────┘
            │                      │
            └──────────────┬───────┘
                           │
            (formatted response text)
                           │
                           ▼
    ┌─────────────────────────────────────────┐
    │  Response Formatter                     │
    │  (adapters & format functions)          │
    │                                         │
    │  ┌──────────────────────────────────┐   │
    │  │ line_adapter._format_diet_plan() │   │
    │  └──────────────────────────────────┘   │
    │                                         │
    │  ┌──────────────────────────────────┐   │
    │  │ metabolic_analysis_adapter.*     │   │
    │  └──────────────────────────────────┘   │
    └─────────────────────────────────────────┘
                           │
                  (TEXT response message)
                           │
                           ▼
    ┌─────────────────────────────────────────┐
    │  LINE Bot SDK                           │
    │  (line_bot_api.reply_message)           │
    └─────────────────────────────────────────┘
                           │
              (reply_message API call)
                           │
                           ▼
    ┌─────────────────────────────────────────┐
    │  LINE Messaging API Cloud               │
    │  (message delivery)                     │
    └─────────────────────────────────────────┘
                           │
              (訊息傳遞到用戶)
                           │
                           ▼
    ┌─────────────────────────────────────────┐
    │  LINE App - User's Phone                │
    │  (displays bot response)                │
    └─────────────────────────────────────────┘
```

---

## 資料流範例

### 情景 1️⃣：飲食計畫請求

```
1. User: "/diet 2000 素食"
   └─ TEXT message sent to LINE API

2. LINE API: webhook callback
   └─ POST to https://your-domain.com/callback
   └─ Body contains: message text "/diet 2000 素食"

3. Flask app.callback()
   └─ Validate signature (X-Line-Signature)
   └─ Extract message content
   └─ Pass to handler.handle()

4. @handler.add(MessageEvent, message=TextMessage)
   └─ Call handle_message(event)
   └─ Extract user_id, message.text
   └─ Call route_user_message(user_id, "/diet 2000 素食")

5. route_user_message()
   └─ parse_command("/diet 2000 素食")
   └─ Returns: ("/diet", ["2000", "素食"])
   └─ Match: /diet
   └─ Call handle_diet_command("U123", ["2000", "素食"])

6. handle_diet_command()
   └─ Parse arguments
   └─ Create profile: {"calories": 2000, "name": "User_xxx", "preferences": ["素食"]}
   └─ Call diet_generator.generate_diet(profile)

7. diet_generator.generate_diet()
   └─ Generate 3 meals
   └─ Allocate calories (600, 800, 600)
   └─ Match preferences
   └─ Return JSON: {"meals": [...], "calories_total": 2000, ...}

8. Back to handle_diet_command()
   └─ Format response text
   └─ Return multiline message:
      "🍽️ User_xxx 的每日飲食計畫
       ...
       【早餐】600 kcal
       ..."

9. Back to handle_message()
   └─ Call line_bot_api.reply_message(reply_token, TextSendMessage(text=...))

10. LINE Messaging API
    └─ Queue message delivery
    └─ Send to user's device

11. User receives message in LINE App
    └─ Displays formatted diet plan
```

---

### 情景 2️⃣：代謝分析請求

```
1. User sends:
   "/analyze
    {
      "date": "2025-11-12",
      "fasting_glucose": 92,
      "blood_ketone": 0.8,
      "meals": [...]
    }"

2. ... (similar to scenario 1, steps 2-5)

3. route_user_message()
   └─ parse_command()
   └─ Returns: ("/analyze", [])
   └─ Match: /analyze
   └─ Call handle_analyze_command("U123", full_message)

4. handle_analyze_command()
   └─ Extract JSON from message body
   └─ Parse: {"date": "2025-11-12", ...}
   └─ Call analyze_metabolic_log_for_line(log_data)

5. analyze_metabolic_log_for_line()
   └─ Evaluate glucose (92 → "良好")
   └─ Evaluate ketone (0.8 → "營養性酮症")
   └─ Detect hidden carbs (yes/no)
   └─ Detect Randle cycle (yes/no)
   └─ Calculate overall score
   └─ Generate detailed report text

6. Back through chain...
   └─ Format complete report
   └─ Send via reply_message()

7. User receives detailed metabolic report
   └─ 🩸 血糖分析
   └─ 🧪 血酮分析
   └─ ⚠️ 警告
   └─ 📈 整體得分
```

---

## 元件詳解

### 1. Flask Application (`line-bot/app.py`)

```python
# 核心功能:
1. initialize LineBotApi with token
2. setup WebhookHandler with secret
3. Register message event handler
4. Define HTTP routes: /, /callback, /health
5. Route commands to handlers
6. Format and send replies
```

**Key Functions:**
- `callback()` - Webhook endpoint
- `handle_message(event)` - Message event handler
- `route_user_message(user_id, text)` - Command router
- `parse_command(text)` - Parse /command format
- `handle_diet_command()` - Process /diet
- `handle_analyze_command()` - Process /analyze
- `handle_help_command()` - Process /help

### 2. Skill Integration Layer (`integrations/`)

```
line_adapter.py (Skill 4)
├─ handle_line_event()          # Convert event to LINE format
└─ _format_diet_plan_for_line() # Format response

metabolic_analysis_adapter.py (Skill 2)
├─ analyze_metabolic_log_for_line()    # Main analysis
├─ _get_glucose_status()               # Evaluate glucose
├─ _get_ketone_status()                # Evaluate ketone
├─ _detect_hidden_carbs()              # Hidden carb detection
├─ _detect_randle_cycle()              # Randle cycle detection
└─ _calculate_overall_score()          # Health score
```

### 3. Skills Layer (`skills/`)

```
skill_4_diet_generator/
└─ scripts/diet_generator.py
   └─ generate_diet(user_profile)

skill_2_metabolic_analysis/
└─ scripts/analyze_logs.py
   └─ analyze_metabolic_log(log, profile)
```

---

## 部署架構

### 本地開發

```
User's Machine
├─ Flask App (localhost:5000)
├─ ngrok tunnel (https://abc123.ngrok.io)
└─ Webhook URL: https://abc123.ngrok.io/callback
```

### 生產環境

```
Option A: Docker + Heroku
├─ Dockerfile
├─ Build image
├─ Push to Heroku
└─ Webhook URL: https://app-name.herokuapp.com/callback

Option B: Google Cloud Run
├─ Cloud Run service
├─ Auto-scaling
└─ Webhook URL: https://region-project.cloudfunctions.net/callback

Option C: AWS Lambda + API Gateway
├─ Lambda function
├─ API Gateway endpoint
└─ Webhook URL: https://api-id.execute-api.region.amazonaws.com/callback
```

---

## 環境變數流向

```
.env
├─ LINE_CHANNEL_ACCESS_TOKEN
│  └─ Used by: LineBotApi initialization
│     └─ Used for: reply_message API calls
│
├─ LINE_CHANNEL_SECRET
│  └─ Used by: WebhookHandler initialization
│     └─ Used for: X-Line-Signature validation
│
├─ FLASK_ENV
│  └─ development (debug=True, hot reload)
│  └─ production (debug=False)
│
└─ PORT
   └─ Server port (default: 5000)
```

---

## 錯誤處理流

```
User Message
    ↓
Try Parse Command
    ├─ Success: Execute handler
    ├─ Failure: Return error message
    └─ Unknown command: Suggest /help

Handler Execution
    ├─ Skill loaded: Call skill
    ├─ Skill not loaded: Return error
    ├─ Argument error: Return usage message
    └─ Skill error: Return error message

Format Response
    ├─ Success: Format nicely
    ├─ Error: Return error explanation
    └─ Missing data: Request more info

Send Reply
    ├─ API success: Message delivered
    ├─ API error: Log error
    └─ Invalid token: Log configuration error
```

---

## 擴展點

### 添加新命令

```python
# In route_user_message():
elif command == "/newcommand":
    return handle_new_command(user_id, args)

# Add handler function:
def handle_new_command(user_id, args):
    # Logic here
    return response_text
```

### 集成新的 Skill

```python
# 1. Import skill
from skills.skill_X.scripts import skill_x_module

# 2. Create adapter
# integrations/skill_x_adapter.py

# 3. Add command handler
def handle_skill_x_command(user_id, args):
    result = skill_x_module.process(args)
    return format_for_line(result)

# 4. Add to router
elif command == "/skillx":
    return handle_skill_x_command(user_id, args)
```

---

**Last Updated:** 2025-11-12
