from fastapi import FastAPI

app = FastAPI(title="ytc-python-docker-template-minimal", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello from ytc-python-docker-template-minimal"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
