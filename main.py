# main.py
# NetCredit Loan Evaluation — Complete CrewAI System
# Built by Vamsi Sadam

import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process

# ── Import agents ──
from agents.researcher import researcher
from agents.risk_analyst import risk_analyst
from agents.decider import decider

# ── Import tasks ──
from tasks.research_task import get_research_task
from tasks.risk_task import get_risk_task
from tasks.decision_task import get_decision_task

# ── Import borrower data ──
from data.borrowers import borrower

# ── Build tasks with borrower data ──
research_task  = get_research_task(borrower)
risk_task      = get_risk_task(borrower)
decision_task  = get_decision_task(borrower)

# ── Assemble the Crew ──
crew = Crew(
    agents=[researcher, risk_analyst, decider],
    tasks=[research_task, risk_task, decision_task],
    process=Process.sequential,
    verbose=True
)

# ── Run it ──
print("\n" + "="*50)
print("NetCredit Loan Evaluation Starting...")
print(f"Borrower: {borrower['name']} | ID: {borrower['id']}")
print(f"Score: {borrower['credit_score']} | Loan: ${borrower['loan_amount']}")
print("="*50 + "\n")

result = crew.kickoff()

print("\n" + "="*50)
print("FINAL DECISION REPORT")
print("="*50)
print(result)