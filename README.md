# ytc-python-docker-template-minimal

Python 服務容器化的**最精簡**範本：Docker + docker compose + GitHub Actions CI/CD。
相依以 [uv](https://docs.astral.sh/uv/) 管理，範例應用為 FastAPI 服務（`/`、`/health`）。

> 設計原則：先給能跑的最小骨架，真正需要時再往上加（healthcheck、多階段建置、快取、多環境設定…）。

## 結構

```
.
├── app/main.py                 # FastAPI 應用
├── tests/test_main.py          # pytest 測試
├── .github/workflows/ci-cd.yml # CI 測試 + CD 推送映像到 GHCR
├── Dockerfile                  # 單階段（uv 官方映像）、非 root
├── docker-compose.yml          # build + ports
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
- **build-and-push**（push 到 `main`）：登入 GHCR → build → push，標籤為 `latest` 與 commit sha

用內建 `GITHUB_TOKEN`，不需額外設定 secret。映像位置：

```
ghcr.io/<your-account>/ytc-python-docker-template-minimal:latest
ghcr.io/<your-account>/ytc-python-docker-template-minimal:<git-sha>
```

> 註：GHCR 映像名稱須為小寫，帳號名含大寫時要另做處理。

## 修改方式

`main` 已鎖：不能直接 push，任何修改都要走 PR 且 CI 綠燈才能 merge。

```bash
git checkout -b fix/xxx
# 改、commit、git push -u origin fix/xxx
gh pr create --fill
gh pr merge --squash    # CI 綠燈後自己就能 merge（approvals = 0）
```
