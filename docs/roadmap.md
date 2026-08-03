# Roadmap：需要時再加（依專案需要）

這是**最精簡的單環境**範本——給你正確的骨架（容器化 + CI + 版本化發佈）。
以下項目是**刻意留白**的（不是缺陷）；需要**多環境 / 部署管線**請改用 `python-docker-template-multienv`。
上 production 前依需要再補：

## 生產環境常見需求

- **Secrets 管理**：真正的密鑰怎麼注入（GitHub Secrets、或 Vault / 雲端 secrets manager）。
- **TLS / HTTPS**：目前純 HTTP，也沒帶 reverse proxy；對外時自行加（Caddy/Traefik/nginx + 憑證）。
- **資料庫 / stateful 服務**：目前無狀態。加 compose 的 db 服務 + migration + 備份策略。
- **健康檢查**：app 有 `/health`，但 Dockerfile / compose 尚未接 `HEALTHCHECK` 去用它。
- **可觀測性**：結構化 log、metrics、tracing。
- **安全掃描**：映像漏洞掃描（Trivy）、Dependabot、SBOM、映像簽章（cosign）。
- **多架構映像**：目前只 build amd64。要跑 arm64（Apple Silicon / AWS Graviton）需 buildx 多平台建置。
