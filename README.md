# python-docker-template-minimal

Python 服務容器化的**最精簡**範本：Docker + docker compose + GitHub Actions CI/CD。
相依以 [uv](https://docs.astral.sh/uv/) 管理，範例應用為 FastAPI 服務（`/`、`/health`）。

> 設計原則：先給能跑的最小骨架，真正需要時再往上加（healthcheck、多階段建置、快取、多環境設定…）。

> 上 production 前依需要再加的項目（Secrets、TLS、DB、健康檢查、可觀測性、安全掃描、多架構）見 **[docs/roadmap.md](docs/roadmap.md)**；要多環境/部署請用 `python-docker-template-multienv`。

## 結構

```
.
├── app/main.py                 # FastAPI 應用
├── tests/test_main.py          # pytest 測試
├── .github/workflows/ci-cd.yml # CI 測試 + CD 推送映像到 GHCR
├── Dockerfile                  # 單階段（uv 官方映像）、非 root
├── compose.yaml                # build + ports
├── pyproject.toml              # 專案定義（非套件模式）
└── uv.lock                     # 鎖定相依（請提交進 git）
```

## 快速開始

```bash
# 本機開發
uv sync --dev
uv run uvicorn app.main:app --reload   # http://localhost:8000/docs
uv run pytest -q

# 容器
docker compose up --build              # http://localhost:8000
```

## CI/CD

`.github/workflows/ci-cd.yml`：

- **test**（push / PR 到 `main`）：`uv sync` + `uv run pytest`
- **build-and-push**（merge 到 `main`）：登入 GHCR → build → push，標籤為 `latest` 與 commit `sha`
- **release**（打 `v*` tag）：把該 commit 的 `:sha` 映像**加上版本標籤 `:v1.2.0`**（不重 build）

用內建 `GITHUB_TOKEN`，不需額外設定 secret。映像位置：

```
ghcr.io/<your-account>/python-docker-template-minimal:latest
ghcr.io/<your-account>/python-docker-template-minimal:<git-sha>
ghcr.io/<your-account>/python-docker-template-minimal:v1.2.0    # 打 tag 發版時
```

### 怎麼發版

```bash
git tag v1.2.0 && git push origin v1.2.0   # 把已在 main 的 commit 發成版本化映像 :v1.2.0
```

**映像自動清理**：`.github/workflows/cleanup.yml` 每週跑一次——`:sha` 建置**只留最近 10 個**、**保護 `latest` 與 `v*` 正式版**、刪 untagged。避免映像無限累積。

> 註：GHCR 映像名稱須為小寫，帳號名含大寫時要另做處理。

## 疑難排解：埠衝突

`docker compose up` 綁 **8000** 埠。若看到：

```
Bind for 0.0.0.0:8000 failed: port is already allocated
```

代表 8000 已被占用。排查：

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN     # 看什麼程式占用
docker ps --filter publish=8000       # 或看是哪個容器占用
```

解法：停掉占用者（`docker stop <容器>`），或改 `compose.yaml` 的 `ports`（例如 `"8001:8000"`），改用 `http://localhost:8001`。

## 修改方式

`main` 已鎖：不能直接 push，任何修改都要走 PR 且 CI 綠燈才能 merge。

```bash
git checkout -b fix/xxx
# 改、commit、git push -u origin fix/xxx
gh pr create --fill
gh pr merge --squash    # CI 綠燈後自己就能 merge（approvals = 0）
```
