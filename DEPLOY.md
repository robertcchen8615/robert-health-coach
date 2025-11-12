# 部署說明（簡易）

此文件提供最小的部署步驟建議：本地開發、容器化與在雲端或 VM 上運行。

## 前提
- 已建立 `.env` 並填寫必要環境變數（API keys, DB URL 等）
- 你有一個 Docker 環境（本地或 CI runner）

## 本地開發（快速）

```bash
# 建立 venv
python3 -m venv venv
source venv/bin/activate

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest -v
```

## 建立 Docker 映像（本地）

```bash
# 在專案根目錄執行
docker build -t robert-health-coach:latest .

# 以交互模式啟動容器
docker run --rm -it \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -p 8080:8080 \
  robert-health-coach:latest
```

> 提示：Dockerfile 為簡易開發用途，若要用於 production，請調整為更安全的多段 build、鎖定套件版本、以及移除測試依賴。

## 使用 docker-compose（範例）

若你想用 docker-compose，建立 `docker-compose.yml`：

```yaml
version: "3.8"
services:
  app:
    image: robert-health-coach:latest
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./:/app
```

然後啟動：

```bash
docker-compose up --build
```

## 部署在雲端（概念步驟）
1. 將映像推到 registry（Docker Hub / ECR / GCR 等）
2. 在目標環境（K8s、EC2、App Service等）部署映像
3. 設定 secrets 與環境變數
4. 設定 ingress / load balancer 與 TLS

## CI/CD 建議
- 在 GitHub Actions 或其他 CI 執行：
  - `pytest`（測試）
  - `black --check`（格式）
  - `flake8`（lint）
  - `docker build` + 推送至 registry
  - 部署到 staging → 執行 smoke tests → 部署到 production

## 環境變數與敏感資訊
- 請勿在 repo 中硬編 API keys
- 在 cloud provider 上使用 secret manager（AWS Secrets Manager / GCP Secret Manager / GitHub Secrets）

## 監控與日誌
- 建議導入基礎監控（CPU、Memory、響應時間）與日誌收集（ELK / Datadog / Papertrail）

---

如需我協助建立 `docker-compose.yml`、K8s manifests 或把 CI 擴充為自動 build+push，回覆我你想要的目標 Provider（Docker Hub / AWS ECR / GCR / GitHub Packages），我會接著生成對應配置與密鑰設定說明。