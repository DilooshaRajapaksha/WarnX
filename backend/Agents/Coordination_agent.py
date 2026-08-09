from langgraph.graph import StateGraph , END
from typing import TypedDict

class CoordinationState(TypedDict):
    report_id : str
    location_latitude : float
    location_longitude : float
    incident_type : str
    description : str
    rainfall_mm : float
    nearby_report_count : int
    verification_result : str
    action_taken : str

def gather_context_node(state : CoordinationState):
    print(f"LOCATION IS {state['location_latitude']}, {state['location_longitude']} and the incident is {state['incident_type']} - {state['description']}")
    return {}

def verify_report_node(state : CoordinationState):
    if state['rainfall_mm'] > 50.00 and state['nearby_report_count'] >= 2:
        return{"verification_result" : "VERIFIED"}
    elif state['rainfall_mm'] >25.00 and state['nearby_report_count'] >= 1:
        return{"verification_result": "UNVERIFIED"}
    else:
        return{"verification_result" : "FLAGGED"}

def take_action(state : CoordinationState):
    if state['verification_result'] == "VERIFIED":
        return{"action_taken": "Report published to community map with green badge"}
    elif state['verification_result'] == "UNVERIFIED":
        return{"action_taken" : "Report saved as pending need more evidence"}
    else:
        return{"action_taken": "Report hidden Flagged as suspicious"}

graph = StateGraph(CoordinationState)
graph.add_node("gather_context_node", gather_context_node)
graph.add_node("verify_report_node" , verify_report_node)
graph.add_node("take_action" , take_action)
graph.set_entry_point("gather_context_node")
graph.add_edge("gather_context_node", "verify_report_node")
graph.add_edge("verify_report_node","take_action")
graph.add_edge("take_action" , END)

app = graph.compile()
result = app.invoke({
    "report_id": "RPT001",
    "location_latitude": 6.6828,
    "location_longitude": 80.3992,
    "incident_type": "flooding",
    "description": "Water rising near the main bridge",
    "rainfall_mm": 75.0,
    "nearby_report_count": 3,
    "verification_result": "",
    "action_taken": ""
})
print(result)