from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime

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

escalations_log = []


@app.get("/")
def root():
    return {"status": "EMI Nudge API is live"}


@app.get("/api/loans")
def get_loan(request: Request):
    borrower_id = request.headers.get("borrower_id")
    loan = loans_db.get(borrower_id)
    if not loan:
        return {"error": "Borrower not found", "received_borrower_id": borrower_id}
    return loan


class EscalationPayload(BaseModel):
    loan_id: str
    borrower_name: str
    days_past_due: str | None = None
    reason_for_transfer: str
    transcript: str | None = None

@app.post("/api/collections/escalations")
def log_escalation(payload: EscalationPayload):
    record = payload.dict()
    record["received_at"] = datetime.utcnow().isoformat()
    escalations_log.append(record)
    return {"status": "logged", "record": record}


@app.get("/api/collections/escalations")
def get_escalations():
    return {"count": len(escalations_log), "escalations": escalations_log}