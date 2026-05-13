# agents/decider.py
# Loan Decision Maker Agent

from crewai import Agent

decider = Agent(
    role="Loan Decision Maker",
    goal="Make final APPROVE, REVIEW or REJECT decision",
    backstory="""You are the Head of Underwriting at NetCredit.
You make final loan decisions compliant with OLA and ILPA regulations.""",
    verbose=True
)