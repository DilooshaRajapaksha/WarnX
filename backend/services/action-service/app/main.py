from fastapi import FastAPI

app = FastAPI(title="WarnX Action Service")


@app.get("/health")
def health():
    return {"service": "action-service", "status": "ok"}
