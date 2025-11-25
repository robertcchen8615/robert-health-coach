# 開發環境與執行範例（Skill 4: Diet Generator）

步驟：

1. 建立虛擬環境並啟用：

   python3 -m venv venv
   source venv/bin/activate

2. 安裝依賴：

   pip install -r requirements.txt

3. 設定環境變數：

   cp .env.example .env
   # 編輯 .env 填入必要的 API key

4. 執行測試：

   python skills/4-diet-generator/scripts/diet_generator.py

備註：若你的專案使用 namespace package（例如 `skills` 為 package），確保根目錄在 PYTHONPATH 或安裝為可匯入的套件。
