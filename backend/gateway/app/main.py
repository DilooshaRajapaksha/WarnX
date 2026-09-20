import os

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

SERVICES = {
    "weather": os.getenv("WEATHER_URL", "http://weather-service:8000"),
    "action": os.getenv("ACTION_URL", "http://action-service:8000"),
    "coordination": os.getenv("COORDINATION_URL", "http://coordination-service:8000"),
    "learning": os.getenv("LEARNING_URL", "http://learning-service:8000"),
}
TIMEOUT = float(os.getenv("SERVICE_TIMEOUT", "5"))
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8081").split(",") if o.strip()]

app = FastAPI(title="WarnX API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"service": "gateway", "status": "ok"}


@app.get("/api/status")
async def status():
    results = {}
    async with httpx.AsyncClient(timeout=2) as client:
        for name, url in SERVICES.items():
            try:
                reply = await client.get(f"{url}/health")
                results[name] = "up" if reply.status_code == 200 else "down"
            except httpx.HTTPError:
                results[name] = "down"
    return results


@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service: str, path: str, request: Request):
    base_url = SERVICES.get(service)
    if base_url is None:
        return JSONResponse(status_code=404, content={"error": f"unknown service '{service}'"})

    headers = {}
    if request.headers.get("content-type"):
        headers["content-type"] = request.headers["content-type"]

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            upstream = await client.request(
                request.method,
                f"{base_url}/{path}",
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )
    except httpx.HTTPError:
        return JSONResponse(
            status_code=503,
            content={
                "error": f"{service} service is unavailable",
                "detail": "Only this feature is affected. The rest of WarnX is still running.",
            },
        )

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        media_type=upstream.headers.get("content-type"),
    )
