# robert-health-coach 🏥

> 一個模組化的健康教練系統，配備多個專業 Skill（技能）提供個性化的健康建議。

![CI Status](https://github.com/robertcchen8615/robert-health-coach/workflows/CI/badge.svg)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 功能概覽

本專案提供一個可擴展的健康教練框架，包含以下 Skill：

| Skill                            | 描述                   | 狀態       |
| -------------------------------- | ---------------------- | ---------- |
| **Skill 1** — Basic Info         | 基本身體資訊收集與分析 | 📋          |
| **Skill 2** — Metabolic Analysis | 代謝與營養分析         | 📊          |
| **Skill 4** — Diet Generator     | 個性化飲食計畫生成     | ✅ **完成** |

### Skill 4：Diet Generator 🍽️

根據使用者的卡路里需求、飲食偏好與健康目標，自動生成每日飲食計畫。

**特性**：
- 🎯 自訂卡路里分配（早、午、晚三餐）
- 🥗 支援飲食偏好（素食、無麩質等）
- 📱 JSON 格式輸出（易於整合）
- 🧪 完整的單元測試覆蓋（8 個測試案例）

**範例**：
```bash
python skills/skill_4_diet_generator/scripts/diet_generator.py '{"calories": 2000, "name": "Alice", "preferences": ["vegetarian"]}'
```

輸出：
```json
{
  "name": "Alice",
  "calories_total": 2000,
  "meals": [
    {
      "name": "breakfast",
      "calories": 600,
      "items": ["oatmeal", "banana", "greek yogurt"]
    },
    {
      "name": "lunch",
      "calories": 800,
      "items": ["chicken salad", "brown rice", "mixed vegetables"]
    },
    {
      "name": "dinner",
      "calories": 600,
      "items": ["salmon", "steamed broccoli", "sweet potato"]
    }
  ],
  "notes": "preferences: vegetarian"
}
```

---

## 🚀 快速開始

### 前置要求
- Python 3.9+
- pip / 虛擬環境（建議）

### 安裝與執行

#### 1. Clone 專案
```bash
git clone https://github.com/robertcchen8615/robert-health-coach.git
cd robert-health-coach
```

#### 2. 建立虛擬環境（建議）
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
```

#### 3. 安裝依賴
```bash
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"  # 安裝專案 + 開發依賴（pytest、black、flake8）
```

#### 4. 執行測試
```bash
pytest -v
```

預期結果：所有 9 個測試通過
```
tests/test_diet_generator.py::test_generate_default PASSED
tests/test_diet_generator.py::test_generate_custom_calories PASSED
...
===================== 9 passed in 0.30s =====================
```

#### 5. 使用 Skill 4
```bash
# 基本執行（預設 1800 卡路里）
python skills/skill_4_diet_generator/scripts/diet_generator.py

# 自訂配置
python skills/skill_4_diet_generator/scripts/diet_generator.py '{"calories": 2500, "name": "Bob"}'
```

---

## 📚 開發指南

### 專案結構

```
robert-health-coach/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD
├── skills/                           # 所有 Skill 模組
│   ├── __init__.py
│   └── skill_4_diet_generator/       # Skill 4 完整實現
│       ├── __init__.py
│       ├── scripts/
│       │   └── diet_generator.py     # 核心邏輯（121 行）
│       ├── SKILL.md                  # Skill 說明
│       ├── README.md                 # 使用指南
│       ├── requirements.txt          # 依賴
│       └── .env.example              # 環境變數範本
├── integrations/                     # 與外部系統的整合
│   └── line_adapter.py               # LINE Bot webhook 適配器
├── tests/                            # 單元與整合測試
│   ├── test_diet_generator.py        # Skill 4 測試（8 個案例）
│   └── test_line_adapter.py          # LINE adapter 測試
├── pyproject.toml                    # 專案配置、依賴、pytest 設定
├── Dockerfile                        # 容器化
├── CONTRIBUTING.md                   # 貢獻規範
├── DEVELOPMENT.md                    # 詳細開發指南
├── DEPLOY.md                         # 部署說明
├── PROGRESS.md                       # 進度報告
└── README.md                         # 本檔案
```

### 常見工作流

#### 執行單元測試
```bash
pytest -v                             # 詳細輸出
pytest --cov=skills                   # 含覆蓋率
pytest tests/test_diet_generator.py   # 特定檔案
```

#### 程式碼檢查與格式化
```bash
# 檢查格式
black --check skills/ tests/

# 自動格式化
black skills/ tests/

# Linting
flake8 skills/ tests/
```

#### 提交新功能
```bash
git checkout -b feature/my-feature
# 做出改動並測試
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
# 在 GitHub 上建立 Pull Request
```

### 建立新 Skill

遵循 Skill 4 的結構：

```bash
mkdir -p skills/skill_X_name/scripts
touch skills/skill_X_name/__init__.py
touch skills/skill_X_name/scripts/main.py
touch skills/skill_X_name/README.md
touch skills/skill_X_name/SKILL.md
touch skills/skill_X_name/requirements.txt
touch skills/skill_X_name/.env.example
```

詳見 `DEVELOPMENT.md`。

---

## 🔧 整合與部署

### LINE Bot 整合

`integrations/line_adapter.py` 提供了一個輕量級適配器，用於在 LINE webhook 中呼叫 Skill。

範例使用：
```python
from integrations.line_adapter import handle_line_event

event = {
    "user_id": "U123",
    "replyToken": "TOKEN",
    "profile": {"calories": 2000, "name": "User"}
}
reply = handle_line_event(event)
# 回傳 LINE reply payload
```

### Docker 部署

建置 Docker 映像：
```bash
docker build -t robert-health-coach:latest .
```

執行容器：
```bash
docker run --rm -it \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -p 8080:8080 \
  robert-health-coach:latest
```

詳見 `DEPLOY.md`。

---

## 📊 測試覆蓋

本專案包含全面的單元測試：

| 模組           | 測試案例 | 通過率   |
| -------------- | -------- | -------- |
| Diet Generator | 8        | 100% ✅   |
| LINE Adapter   | 1        | 100% ✅   |
| **總計**       | **9**    | **100%** |

執行覆蓋率報告：
```bash
pytest --cov=skills --cov-report=html
open htmlcov/index.html
```

---

## 🔐 分支保護與 CI/CD

### 分支保護規則

我們強烈建議配置分支保護以確保程式碼品質。

**設置步驟**：
1. 進入 GitHub repository → **Settings**
2. 左側菜單 → **Branches**
3. 點擊 **Add rule**
4. **Branch name pattern**：`main`
5. ✅ **勾選**：
   - ✅ Require a pull request before merging
   - ✅ Require approvals (建議 1 人)
   - ✅ **Dismiss stale pull request approvals when new commits are pushed**
   - ✅ **Require status checks to pass before merging**
     - Select CI workflow 中的所有 checks：
       - `ci (3.9)`, `ci (3.10)`, `ci (3.11)`
   - ✅ **Require branches to be up to date before merging**
   - ✅ Include administrators
6. 點擊 **Create**

### CI/CD 流程

每次 push 或 PR 時，GitHub Actions 自動執行：

```yaml
✅ pytest（Python 3.9、3.10、3.11）
✅ black --check（程式碼格式）
✅ flake8（程式碼品質）
```

檢查執行狀態：https://github.com/robertcchen8615/robert-health-coach/actions

---

## 📖 文檔

| 文件                   | 用途                                 |
| ---------------------- | ------------------------------------ |
| `CONTRIBUTING.md`      | 如何貢獻、開發流程、commit 規範      |
| `DEVELOPMENT.md`       | 詳細開發指南、測試策略、建立新 Skill |
| `DEPLOY.md`            | 部署步驟、Docker、雲端部署建議       |
| `PROGRESS.md`          | 進度報告、統計數據、下一步計畫       |
| `SKILL.md`（各 Skill） | 各 Skill 的功能說明                  |

---

## 🤝 貢獻

歡迎貢獻！請遵循以下步驟：

1. **Fork 這個 repository**
2. **建立 feature 分支**：`git checkout -b feature/your-feature`
3. **提交更改**：`git commit -m "feat: description"`
4. **推送分支**：`git push origin feature/your-feature`
5. **建立 Pull Request**

詳見 `CONTRIBUTING.md`。

---

## 📝 Commit 規範

遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hant/)：

- `feat:` — 新功能
- `fix:` — 修復 bug
- `refactor:` — 代碼重構
- `test:` — 新增/修改測試
- `docs:` — 文檔更新
- `chore:` — 構建、依賴更新

範例：
```
feat: add calorie tracking to diet generator
fix: correct breakfast calorie calculation
test: add edge case tests for zero calories
```

---

## 📞 支援

- **Issues**：https://github.com/robertcchen8615/robert-health-coach/issues
- **Discussions**：https://github.com/robertcchen8615/robert-health-coach/discussions

---

## 📄 授權

MIT License — 詳見 `LICENSE` 檔案

---

## 🙏 致謝

感謝所有貢獻者與支持者！

---

**版本**：0.1.0
**最後更新**：2025 年 11 月 12 日
**製作者**：Health Coach Development Team
