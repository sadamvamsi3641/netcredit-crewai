# agents/researcher.py
# Borrower Researcher Agent

from crewai import Agent

researcher = Agent(
    role="Borrower Researcher",
    goal="Research and summarize the borrower's financial profile",
    backstory="""You are a junior analyst at NetCredit.
Your job is to review borrower data and produce a clear
financial summary for the credit risk team.""",
    verbose=True
)