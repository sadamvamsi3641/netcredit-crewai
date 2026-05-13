# tools/crm_update.py
# Mock CRM Update Tool — updates loan decision in CRM

from crewai.tools import tool

@tool("Update CRM")
def update_crm(borrower_id: str, decision: str) -> str:
    """Updates the loan decision in the NetCredit CRM system
    after the final decision is made."""
    
    # Mock — in real life this calls NetCredit CRM API
    print(f"\n[CRM] Updated: {borrower_id} → {decision}")
    return f"CRM successfully updated: {borrower_id} = {decision}"