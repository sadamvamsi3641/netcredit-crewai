# workflow.py
# NetCredit Loan Approval — LangGraph 6-Stage Stateful Workflow
# Built by Vamsi Sadam

import os
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# ── Step 1: Define the STATE ──────────────────────
# State = the data that flows through every stage
# Every node reads from state and writes back to state
class LoanState(TypedDict):
    borrower_id:     str
    name:            str
    credit_score:    int
    monthly_income:  int
    loan_amount:     int
    has_bankruptcy:  bool
    employment:      str
    identity_verified: bool
    risk_tier:       str
    dti_ratio:       float
    human_approved:  bool
    decision:        str
    reason:          str
    current_stage:   str

# ── Step 2: Define the 6 NODES ────────────────────
# Each node = one stage in the loan process

# Stage 1: Application Intake
def intake(state: LoanState):
    print(f"\n📋 Stage 1: Application Intake")
    print(f"   Borrower: {state['name']} | ID: {state['borrower_id']}")
    print(f"   Loan Amount: ${state['loan_amount']} | Income: ${state['monthly_income']}/mo")
    return {"current_stage": "intake_complete"}

# Stage 2: Identity Verification
def verify_identity(state: LoanState):
    print(f"\n🪪  Stage 2: Identity Verification")
    # Mock verification — in real life calls identity API
    verified = not state["has_bankruptcy"] or state["credit_score"] > 500
    print(f"   Identity verified: {verified}")
    return {
        "identity_verified": verified,
        "current_stage": "identity_complete"
    }

# Stage 3: Credit Scoring
def credit_score(state: LoanState):
    print(f"\n📊 Stage 3: Credit Scoring")
    dti = round((state["loan_amount"] / 12) / state["monthly_income"] * 100, 1)
    print(f"   Credit Score: {state['credit_score']}")
    print(f"   DTI Ratio: {dti}%")
    return {
        "dti_ratio": dti,
        "current_stage": "scoring_complete"
    }

# Stage 4: Risk Assessment
def risk_assessment(state: LoanState):
    print(f"\n⚠️  Stage 4: Risk Assessment")
    score = state["credit_score"]
    dti   = state["dti_ratio"]
    bankruptcy = state["has_bankruptcy"]

    if bankruptcy or score < 500:
        tier = "HIGH"
    elif score >= 700 and dti < 40:
        tier = "LOW"
    else:
        tier = "MEDIUM"

    print(f"   Risk Tier: {tier}")
    return {
        "risk_tier": tier,
        "current_stage": "risk_complete"
    }

# Stage 5: Human Review (HITL checkpoint)
def human_review(state: LoanState):
    print(f"\n👨‍💼 Stage 5: Human Review")
    print(f"   ⚠️  MEDIUM risk — routing to analyst")
    print(f"   Analyst must approve or reject manually")
    return {"current_stage": "human_review"}

# Stage 6: Final Decision
def final_decision(state: LoanState):
    print(f"\n✅ Stage 6: Final Decision")
    tier = state["risk_tier"]
    human = state.get("human_approved", False)

    if tier == "HIGH":
        decision = "REJECT"
        reason = "High risk — bankruptcy or low credit score"
    elif tier == "LOW":
        decision = "APPROVE"
        reason = "Low risk — strong credit profile"
    elif tier == "MEDIUM" and human:
        decision = "APPROVE"
        reason = "Medium risk — approved after analyst review"
    else:
        decision = "REVIEW"
        reason = "Medium risk — pending analyst review"

    print(f"   Decision: {decision}")
    print(f"   Reason: {reason}")
    return {
        "decision": decision,
        "reason": reason,
        "current_stage": "complete"
    }

# ── Step 3: Routing logic ─────────────────────────
def route_after_risk(state: LoanState):
    tier = state["risk_tier"]
    if tier == "HIGH":
        return "final_decision"    # skip human review → straight to reject
    elif tier == "LOW":
        return "final_decision"    # skip human review → straight to approve
    else:
        return "human_review"      # MEDIUM → pause for human

# ── Step 4: Build the GRAPH ───────────────────────
graph = StateGraph(LoanState)

# Add all 6 nodes
graph.add_node("intake",         intake)
graph.add_node("verify_identity",verify_identity)
graph.add_node("credit_score",   credit_score)
graph.add_node("risk_assessment",risk_assessment)
graph.add_node("human_review",   human_review)
graph.add_node("final_decision", final_decision)

# Connect the nodes (edges)
graph.set_entry_point("intake")
graph.add_edge("intake",          "verify_identity")
graph.add_edge("verify_identity", "credit_score")
graph.add_edge("credit_score",    "risk_assessment")
graph.add_edge("human_review",    "final_decision")
graph.add_edge("final_decision",  END)

# Conditional edge — after risk assessment
graph.add_conditional_edges(
    "risk_assessment",
    route_after_risk,
    {
        "human_review":   "human_review",
        "final_decision": "final_decision"
    }
)

# ── Step 5: Add CHECKPOINTER (saves state) ────────
checkpointer = MemorySaver()
app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_review"]  # pause here for HITL
)

# ── Step 6: RUN IT ────────────────────────────────
borrower = {
    "borrower_id":    "B-1042",
    "name":           "Ben Jacks",
    "credit_score":   790,
    "monthly_income": 1000,
    "loan_amount":    10000,
    "has_bankruptcy": False,
    "employment":     "Full-time, 3 years",
    "identity_verified": False,
    "risk_tier":      "",
    "dti_ratio":      0.0,
    "human_approved": False,
    "decision":       "",
    "reason":         "",
    "current_stage":  ""
}

config = {"configurable": {"thread_id": "loan-B1042"}}

print("\n" + "="*50)
print("NetCredit LangGraph Workflow Starting...")
print("="*50)

# Run until interrupt (pauses at human_review for MEDIUM risk)
app.invoke(borrower, config)

# Check if paused
state = app.get_state(config)
if state.next:
    print(f"\n⏸️  PAUSED at: {state.next}")
    print("   Simulating analyst approval...")

    # Simulate human approving
    app.update_state(config, {"human_approved": True})

    # Resume from pause
    app.invoke(None, config)

print("\n" + "="*50)
print("Workflow Complete!")
print("="*50)