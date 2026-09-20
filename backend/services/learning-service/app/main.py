from fastapi import FastAPI

app = FastAPI(title="WarnX Learning Service")


@app.get("/health")
def health():
    return {"service": "learning-service", "status": "ok"}
