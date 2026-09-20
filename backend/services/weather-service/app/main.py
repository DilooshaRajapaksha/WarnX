from fastapi import FastAPI

app = FastAPI(title="WarnX Weather Service")


@app.get("/health")
def health():
    return {"service": "weather-service", "status": "ok"}
