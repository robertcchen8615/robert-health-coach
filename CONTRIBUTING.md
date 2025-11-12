# Contributing to robert-health-coach

感謝你有興趣貢獻到這個專案！本文件說明如何設置本地開發環境、執行測試，以及提交貢獻。

## 開發環境設置

### 1. Clone 專案

```bash
git clone https://github.com/YOUR_ACCOUNT/robert-health-coach.git
cd robert-health-coach
```

### 2. 建立虛擬環境（建議）

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows
```

### 3. 安裝依賴

```bash
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

這將安裝專案本身及所有開發依賴（pytest、black、flake8）。

## 執行測試

```bash
# 執行所有測試
pytest

# 執行特定測試檔案
pytest tests/test_diet_generator.py

# 詳細輸出
pytest -v

# 含覆蓋率報告
pytest --cov=skills --cov-report=html
```

## 程式碼風格

我們使用 **Black** 進行自動格式化，與 **Flake8** 進行 linting。

### 格式化程式碼

```bash
black skills/ tests/
```

### 檢查 Lint

```bash
flake8 skills/ tests/
```

## 提交貢獻

1. **建立 Feature Branch**

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **提交更改**

   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

3. **推送到你的 Fork**

   ```bash
   git push origin feature/my-new-feature
   ```

4. **建立 Pull Request**

   - 清楚描述你的改動與為什麼做這個改動
   - 確保所有測試通過
   - 遵循程式碼風格（Black & Flake8）

## Commit Message 規範

我們遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hant/) 規範：

- `feat:` — 新功能
- `fix:` — 修復 bug
- `refactor:` — 代碼重構（無功能變更）
- `test:` — 新增或修改測試
- `docs:` — 文檔更新
- `chore:` — 構建工具、依賴更新等

範例：

```
feat: add preferences filtering in diet generator
fix: correct calorie calculation for breakfast
test: add edge case tests for zero calories
```

## 建立新 Skill

若要新增新的 Skill（例如 Skill 5），參考 `skills/skill_4_diet_generator/` 結構：

```
skills/skill_5_new_skill/
├── __init__.py
├── SKILL.md
├── scripts/
│   └── main.py
├── README.md
├── requirements.txt
└── .env.example
```

並在 `tests/` 新增對應的測試檔案 `test_skill_5.py`。

## 問題回報

如發現 bug 或有建議，請在 GitHub Issues 中建立 issue。

感謝貢獻！🚀
