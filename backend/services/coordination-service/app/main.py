from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.coordination_agent import build_verification_graph, build_help_matching_graph

app = FastAPI(title="WarnX Coordination Service")

verification_graph = build_verification_graph()
help_matching_graph = build_help_matching_graph()


class ReportIn(BaseModel):
    report_id: str
    location_latitude: float
    location_longitude: float
    incident_type: str
    description: str
    rainfall_mm: float
    nearby_report_count: int


class HelpRequestIn(BaseModel):
    request_id: str
    request_type: str
    help_category: str
    request_lat: float
    request_lng: float


@app.get("/health")
def health():
    return {"service": "coordination-service", "status": "ok"}


@app.post("/reports/verify")
def verify_report(report: ReportIn):
    return verification_graph.invoke({
        **report.model_dump(),
        "verification_result": "",
        "action_taken": "",
    })


@app.post("/help/match")
def match_help(request: HelpRequestIn):
    return help_matching_graph.invoke({
        **request.model_dump(),
        "available_offers": [],
        "match_found": False,
        "match_details": "",
        "action_taken": "",
    })
