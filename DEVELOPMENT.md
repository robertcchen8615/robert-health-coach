# 開發指南（DEVELOPMENT.md）

本文件詳細說明專案架構、本地開發流程、測試策略，以及如何擴展功能。

## 專案架構

```
robert-health-coach/
├── skills/                      # 所有 Skill 模組
│   ├── __init__.py
│   ├── 1-basic-info/            # Skill 1
│   ├── 2-metabolic-analysis/    # Skill 2
│   └── skill_4_diet_generator/  # Skill 4
│       ├── __init__.py
│       ├── scripts/
│       │   └── diet_generator.py
│       ├── SKILL.md
│       ├── README.md
│       └── requirements.txt
├── tests/                        # 單元與整合測試
│   ├── test_diet_generator.py
│   └── ...
├── shared/                       # 共享工具、常數
├── agent/                        # 主要 Agent 邏輯
├── line-bot/                     # LINE Bot 實作
├── pyproject.toml               # 專案配置與依賴
├── .github/workflows/ci.yml     # CI/CD 設定
└── README.md                     # 專案總覽
```

## 本地開發流程

### Step 1: 準備環境

```bash
cd /path/to/robert-health-coach
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Step 2: 執行測試

```bash
# 所有測試
pytest

# 特定檔案
pytest tests/test_diet_generator.py -v

# 含覆蓋率
pytest --cov=skills
```

### Step 3: 程式碼檢查與格式

```bash
# Black 格式檢查
black --check skills/ tests/

# Black 自動格式化
black skills/ tests/

# Flake8 lint
flake8 skills/ tests/
```

### Step 4: 推送與 CI

```bash
git add .
git commit -m "feat: description"
git push origin feature/branch
```

GitHub Actions 將自動執行：
- pytest（多 Python 版本）
- Black format check
- Flake8 lint

## 建立新 Skill

### 模板步驟

1. **建立目錄**

   ```bash
   mkdir -p skills/skill_X_name/scripts
   ```

2. **核心檔案**

   - `__init__.py` — 匯出主函數
   - `scripts/main.py` — 實現邏輯
   - `SKILL.md` — Skill 說明
   - `README.md` — 使用指南
   - `requirements.txt` — 依賴
   - `.env.example` — 環境變數範例

3. **新增測試**

   建立 `tests/test_skill_X.py`，並確保 100% 通過。

4. **更新 pyproject.toml**

   若有特殊依賴，在 `[project.optional-dependencies]` 中新增對應項。

## 測試策略

### 單元測試

每個 Skill 應包含以下測試場景：

- **Happy Path** — 正常輸入、預期輸出
- **Edge Cases** — 邊界值、空值、大值
- **Error Handling** — 無效輸入、型別錯誤

### 範例（Skill 4）

```python
def test_generate_default():
    """Happy path: default parameters"""
    plan = generate_diet({})
    assert plan["calories_total"] == 2000

def test_generate_high_calories():
    """Edge case: high calorie intake"""
    plan = generate_diet({"calories": 4000})
    assert plan["calories_total"] == 4000

def test_generate_string_calories_conversion():
    """Error handling: string to int conversion"""
    plan = generate_diet({"calories": "2500"})
    assert plan["calories_total"] == 2500
```

### 覆蓋率目標

- 核心邏輯：≥ 90%
- 整體項目：≥ 80%

```bash
pytest --cov=skills --cov-report=term-missing
```

## Git 工作流

1. **本地開發分支**

   ```bash
   git checkout -b feature/new-feature
   ```

2. **定期提交**

   ```bash
   git commit -m "feat: add new feature"
   ```

3. **推送至遠端**

   ```bash
   git push origin feature/new-feature
   ```

4. **建立 Pull Request**

   - 標題格式：`feat: description` 或 `fix: description`
   - 描述變更內容與原因
   - 確保 CI 全部通過

5. **合併**

   Reviewer 核准後，於 GitHub 上點擊 "Squash and merge"。

## 常見問題

### Q: 如何新增第三方套件依賴？

A: 編輯 `pyproject.toml`，在 `[project.dependencies]` 或 `[project.optional-dependencies]` 中新增，然後執行 `pip install -e ".[dev]"`。

### Q: 如何在本地執行 LINE Bot？

A: 參考 `line-bot/README.md`。

### Q: 如何檢查程式碼是否符合風格指南？

A:
```bash
black --check skills/
flake8 skills/
```

若不符合，執行 `black skills/` 自動修復。

## 進階話題

### 環境變數

項目支援 `.env` 檔案。複製 `.env.example` 為 `.env` 並填入必要的值（如 API key）。

### Docker

若項目有 Docker 支援，見 `Dockerfile` 與 `docker-compose.yml`。

### 部署

部署步驟（若有 CI/CD）見 `.github/workflows/` 或專案 wiki。

---

有問題？提 Issue 或聯絡維護者。感謝貢獻！🎉
