from fastapi import FastAPI

app = FastAPI()


loans_db = {
    "LN00234": {
        "borrower_id": "LN00234",
        "borrower_name": "Rahul Mehta",
        "emi_amount": "4500",
        "due_date": "2026-08-10",
        "days_past_due": "12",
        "preferred_language": "Hindi"
    },
    "LN00567": {
        "borrower_id": "LN00567",
        "borrower_name": "Priya Nair",
        "emi_amount": "6200",
        "due_date": "2026-08-05",
        "days_past_due": "18",
        "preferred_language": "English"
    }
}

@app.get("/")
def root():
    return {"status": "EMI Nudge API is live"}

@app.get("/api/loans/{borrower_id}")
def get_loan(borrower_id: str):
    loan = loans_db.get(borrower_id)
    if not loan:
        return {"error": "Borrower not found"}
    return loan