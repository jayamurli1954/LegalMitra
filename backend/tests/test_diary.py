from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta
import random

client = TestClient(app)

# Helper to generate unique data
def unique_str():
    return str(random.randint(1000, 9999))

def test_diary_flow():
    # 1. Create Client
    client_res = client.post("/api/v1/diary/clients", json={
        "full_name": "Test Client " + unique_str(),
        "mobile": "9999999999",
        "email": "test@example.com"
    })
    assert client_res.status_code == 200
    client_id = client_res.json()["id"]
    print(f"Created Client ID: {client_id}")

    # 2. Create Case
    case_res = client.post("/api/v1/diary/cases", json={
        "case_number": "WP " + unique_str() + "/2024",
        "court": "High Court",
        "client_id": client_id,
        "case_type": "Civil",
        "filing_date": str(date.today())
    })
    assert case_res.status_code == 200
    case_id = case_res.json()["id"]
    print(f"Created Case ID: {case_id}")

    # 3. Log Hearing
    next_date = str(date.today() + timedelta(days=7))
    hearing_res = client.post("/api/v1/diary/hearings", json={
        "case_id": case_id,
        "hearing_date": str(date.today()),
        "purpose": "Admission",
        "order_passed": "Notice Issued",
        "next_date": next_date
    })
    assert hearing_res.status_code == 200
    print("Logged Hearing")

    # 4. Verify Next Date Update in Case
    get_case_res = client.get(f"/api/v1/diary/cases/{case_id}")
    assert get_case_res.json()["next_hearing"] == next_date
    print("Verified Case Next Hearing Update")

    # 5. Log Fee
    fee_res = client.post("/api/v1/diary/fees", json={
        "case_id": case_id,
        "amount_billed": 10000.0,
        "amount_received": 2000.0,
        "date": str(date.today())
    })
    assert fee_res.status_code == 200
    print("Logged Fee")

    # 6. Check Dashboard
    dash_res = client.get("/api/v1/diary/dashboard")
    assert dash_res.status_code == 200
    stats = dash_res.json()
    assert stats["hearings_today"] >= 1
    assert stats["fees_outstanding"] >= 8000.0
    print("Dashboard Stats Verified")

if __name__ == "__main__":
    test_diary_flow()
