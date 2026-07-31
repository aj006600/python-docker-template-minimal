from fastapi import FastAPI

app = FastAPI(title="python-docker-template-minimal", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello from python-docker-template-minimal"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
