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

def build_verification_graph():
    graph = StateGraph(CoordinationState)
    graph.add_node("gather_context_node", gather_context_node)
    graph.add_node("verify_report_node" , verify_report_node)
    graph.add_node("take_action" , take_action)
    graph.set_entry_point("gather_context_node")
    graph.add_edge("gather_context_node", "verify_report_node")
    graph.add_edge("verify_report_node","take_action")
    graph.add_edge("take_action" , END)
    return graph.compile()


class HelpMatchingState(TypedDict):
    request_id : str
    request_type : str
    help_category : str
    request_lat : float
    request_lng : float
    available_offers : list
    match_found : bool
    match_details : str
    action_taken : str

fake_offers = [
    {"category": "boat", "distance_km": 2.3, "contact": "0771234567"},
    {"category": "boat", "distance_km": 5.1, "contact": "0779876543"}
]

def search_offers_node(state : HelpMatchingState):
    print(f"Searching for {state['help_category']} offers near {state['request_lat']}, {state['request_lng']}...")
    return{"available_offers" : fake_offers}


def match_offer_node(state : HelpMatchingState):
    if len(state['available_offers']) >= 1 and state['available_offers'][0]['category'] == state['help_category']:
        closest = state['available_offers'][0]
        return {
            "match_found": True,
            "match_details": f"Match found! {closest['category']} available {closest['distance_km']}km away. Contact: {closest['contact']}"
        }
    else :
        return {
            "match_found": False,
            "match_details": "No matching offers found nearby"            
        }

def notify_match_node(state : HelpMatchingState):
    if state['match_found'] == True:
        print("Notify the Both parties")
        return{"action_taken" : "Both parties notified about the match"}
    else:
        print("No match found...Searching....")
        return{"action_taken": "No match found,Still searching offers. "}

def build_help_matching_graph():
    graph2 = StateGraph(HelpMatchingState)
    graph2.add_node("search_offers_node" , search_offers_node)
    graph2.add_node("match_offer_node" , match_offer_node)
    graph2.add_node("notify_match_node" , notify_match_node)
    graph2.set_entry_point("search_offers_node")
    graph2.add_edge("search_offers_node" , "match_offer_node")
    graph2.add_edge("match_offer_node","notify_match_node")
    graph2.add_edge("notify_match_node" , END)
    return graph2.compile()


if __name__ == "__main__":
    app = build_verification_graph()
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

    app2 = build_help_matching_graph()
    result2 = app2.invoke({
        "request_id": "HLP001",
        "request_type": "need",
        "help_category": "boat",
        "request_lat": 6.6828,
        "request_lng": 80.3992,
        "available_offers": [],
        "match_found": False,
        "match_details": "",
        "action_taken": ""
    })
    print(result2)
