# 🔐 設定 GitHub 分支保護步驟指南

本文件提供設定分支保護規則的逐步指南，確保 `main` 分支的程式碼品質與 CI/CD 流程完整性。

## 為什麼需要分支保護？

分支保護規則提供以下好處：

✅ **強制執行程式碼審查** — 防止直接 push 到主分支
✅ **自動化測試驗證** — 確保所有 PR 通過 CI 檢查
✅ **維護代碼品質** — 要求 CI (pytest、black、flake8) 全部通過
✅ **團隊協作** — 需要審核者批准後才能合併

---

## 逐步設置指南

### Step 1: 進入 Repository Settings

1. 開啟 GitHub repository：https://github.com/robertcchen8615/robert-health-coach
2. 點擊上方的 **Settings** 標籤
3. 左側菜單會出現許多選項

### Step 2: 進入 Branches 設定

1. 在左側菜單，點擊 **Branches**（可能在 "Code and automation" 群組下）
2. 你會看到 "Branch protection rules" 區域
3. 點擊 **Add rule** 按鈕

### Step 3: 設定分支名稱模式

1. **Branch name pattern** 欄位，輸入：`main`
2. 這會將規則應用到 `main` 分支

### Step 4: 設定保護規則

#### 4.1 Pull Request 要求

- ✅ **Require a pull request before merging**
  - ✅ **Require approvals**（選擇人數，建議 1）
  - ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - ✅ **Require review from Code Owners**（可選）

#### 4.2 CI/CD 檢查

- ✅ **Require status checks to pass before merging**
  - 點擊 **Search for status checks in the last week for this repository**
  - 選擇所有 CI jobs：
    - ☑️ `ci (3.9)` — Python 3.9 測試
    - ☑️ `ci (3.10)` — Python 3.10 測試
    - ☑️ `ci (3.11)` — Python 3.11 測試
  - ✅ **Require branches to be up to date before merging**（確保 PR 是最新的）

#### 4.3 其他保護選項

- ✅ **Require code reviews before merging**（已在 4.1 設定）
- ✅ **Include administrators**（讓規則也應用於管理員）
- ⚠️ **Restrict who can push to matching branches**（可選，限制誰能推送）

### Step 5: 完成設置

1. 捲到頁面底部
2. 點擊 **Create** 按鈕
3. 規則已成功建立！✅

---

## 驗證設置是否成功

### 在 Repository 首頁檢查

1. 進入 https://github.com/robertcchen8615/robert-health-coach
2. 點擊 **Code** 標籤
3. 在 "About" 區域（右側），應該會看到一個🔒圖示，表示分支已受保護

### 測試分支保護

1. **建立一個新 PR**（即使你是 admin）
2. PR 會顯示 CI 檢查狀態：
   - 🟡 Pending — CI 正在執行
   - ✅ Pass — CI 全部通過，可以合併
   - ❌ Fail — CI 失敗，禁止合併
3. 如果沒有批准，即使 CI 通過也無法合併

---

## 視覺檢查清單

| 項目                                  | 狀態           |
| ------------------------------------- | -------------- |
| Require a pull request before merging | ✅              |
| Require approvals                     | ✅ (1 reviewer) |
| Dismiss stale pull request approvals  | ✅              |
| Require status checks to pass         | ✅              |
| - ci (3.9)                            | ☑️              |
| - ci (3.10)                           | ☑️              |
| - ci (3.11)                           | ☑️              |
| Require branches to be up to date     | ✅              |
| Include administrators                | ✅              |
| **Save changes**                      | 點擊 Create    |

---

## 設置後的工作流

### 貢獻者流程

```bash
# 1. 建立 feature 分支
git checkout -b feature/my-feature

# 2. 做出改動、測試
pytest -v

# 3. 提交並推送
git commit -m "feat: add new feature"
git push origin feature/my-feature

# 4. 在 GitHub 建立 Pull Request（自動觸發 CI）

# 5. 等待 CI 通過 ✅
# GitHub Actions 會自動執行：
# - pytest (Python 3.9, 3.10, 3.11)
# - black --check
# - flake8

# 6. 獲得審核批准

# 7. 合併到 main（GitHub UI 上點擊 "Merge"）
```

### 分支保護流程圖

```
開發者推送 PR
    ↓
GitHub Actions CI 自動觸發（3 個 Python 版本）
    ↓
✅ CI 全部通過？
    ├─ ❌ 否：修復錯誤，重新推送 → 再次執行 CI
    └─ ✅ 是：繼續
    ↓
請求代碼審查
    ↓
✅ 獲得批准？
    ├─ ❌ 否：根據意見修改 → 重新提交
    └─ ✅ 是：繼續
    ↓
✅ 合併到 main 分支
```

---

## 常見問題（FAQ）

### Q: 為什麼我看不到 CI jobs 可以選擇？

A: CI jobs 在首次 workflow 執行後才會出現。確保你已經推送了程式碼並讓 GitHub Actions 執行至少一次。

**檢查 workflow 執行狀態**：https://github.com/robertcchen8615/robert-health-coach/actions

### Q: 我是 admin，為什麼還是無法直接合併？

A: 如果你勾選了 **Include administrators**，規則會應用到所有人包括 admin。若要讓 admin 繞過規則，取消勾選此選項。

### Q: 如何修改已有的規則？

A: 在 Settings → Branches，找到規則旁的 **Edit** 按鈕，修改設定後點 **Save changes**。

### Q: 可以有多個分支保護規則嗎？

A: 可以！點擊 **Add rule** 可以新增多個規則（例如為 `develop` 分支也設置規則）。

---

## 推薦配置（進階）

### 自動刪除 head 分支

- ✅ **Automatically delete head branches**
- 功能：PR 合併後自動刪除 feature 分支

### Code owners

建立 `.github/CODEOWNERS` 檔案指定代碼所有者（負責審查特定檔案）：

```
# .github/CODEOWNERS
* @robertcchen8615
skills/skill_4_diet_generator/ @robertcchen8615
tests/ @robertcchen8615
```

### Require conversation resolution

- ✅ **Require all conversations on code to be resolved before merging**
- 功能：PR 中的所有 comments/discussions 必須解決才能合併

---

## 後續步驟

✅ **分支保護已設置**

現在：
1. ✅ 本地開發與測試
2. ✅ 推送 feature 分支
3. ✅ 建立 Pull Request
4. ✅ GitHub Actions CI 自動執行
5. ✅ 請求審查並獲得批准
6. ✅ 合併到 main

---

**設置完成！你的 repository 現在有了完整的 CI/CD 與代碼品質保護。🎉**

如有問題，查看 GitHub 文檔：https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
