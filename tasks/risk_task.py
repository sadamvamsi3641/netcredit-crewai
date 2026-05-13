# tasks/risk_task.py
from crewai import Task
from agents.risk_analyst import risk_analyst

def get_risk_task(borrower):
    return Task(
        description=f"""Using the researcher summary, assess credit risk
for borrower {borrower['id']}.
Classify as LOW, MEDIUM or HIGH risk.
Explain top 3 risk factors.""",
        expected_output="""Risk assessment with:
- Risk tier: LOW / MEDIUM / HIGH
- Top 3 risk factors
- Recommendation to decider""",
        agent=risk_analyst
    )