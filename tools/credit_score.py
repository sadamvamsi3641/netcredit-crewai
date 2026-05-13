# tools/credit_score.py
# Mock Colossus API Tool — fetches ML risk score

from crewai.tools import tool

@tool("Get Credit Score")
def get_credit_score(borrower_id: str) -> str:
    """Fetches the ML risk score from Colossus API
    for a given borrower ID."""
    
    # Mock data — in real life this calls Colossus API
    scores = {
        "B-1042": (680, "MEDIUM"),
        "B-1043": (725, "LOW"),
        "B-1044": (490, "HIGH"),
    }
    
    score, tier = scores.get(borrower_id, (600, "MEDIUM"))
    return f"Borrower {borrower_id}: Score={score}, Risk Tier={tier}"