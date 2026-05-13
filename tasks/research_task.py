# tasks/research_task.py
from crewai import Task
from agents.researcher import researcher

def get_research_task(borrower):
    return Task(
        description=f"""Review this borrower and produce a financial summary:
ID:         {borrower['id']}
Name:       {borrower['name']}
Score:      {borrower['credit_score']}
Income:     ${borrower['monthly_income']}/month
Loan:       ${borrower['loan_amount']}
Bankruptcy: {borrower['has_bankruptcy']}
Employment: {borrower['employment']}
Calculate debt-to-income ratio. Note strengths and red flags.""",
        expected_output="""Structured summary with:
- Borrower overview
- Key strengths
- Red flags
- Debt-to-income ratio""",
        agent=researcher
    )