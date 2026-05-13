# tasks/decision_task.py
from crewai import Task
from agents.decider import decider

def get_decision_task(borrower):
    return Task(
        description=f"""Make the final loan decision for {borrower['id']}.
Rules: HIGH → REJECT. MEDIUM → REVIEW. LOW → APPROVE.
Must comply with OLA and ILPA regulations.""",
        expected_output="""Final decision report:
- Decision: APPROVE / REVIEW / REJECT
- Reason
- Regulatory compliance note
- Next steps""",
        agent=decider
    )