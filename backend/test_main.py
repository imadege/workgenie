# test_main.py

from fastapi.testclient import TestClient
from main import app, events_db

client = TestClient(app)

# Helper function to reset the in-memory events database before each test
def reset_events_db():
    global events_db
    events_db = [
        {"id": 1, "title": "Event 1", "organizer": "User A", "date_time": "2024-10-14T15:00:00", "location": "Venue A", "joiners": [], "status": "active"},
        {"id": 2, "title": "Event 2", "organizer": "User B", "date_time": "2024-10-15T18:00:00", "location": "Venue B", "joiners": [], "status": "active"},
    ]


# Test to get all events
def test_get_events():
    reset_events_db()  # Reset events before test
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 2
    assert response.json()["events"][0]["title"] == "Event 1"


# Test joining an event
def test_join_event():
    reset_events_db()  # Reset events before test
    response = client.post("/api/events/1/join", json={"user": "UserX"})
    assert response.status_code == 200
    assert "UserX" in response.json()["joiners"]


# Test leaving an event
def test_leave_event():
    reset_events_db()  # Reset events before test
    # First join the event
    client.post("/api/events/1/join", json={"user": "UserX"})
    # Now leave the event
    response = client.post("/api/events/1/leave", json={"user": "UserX"})
    assert response.status_code == 200
    assert "UserX" not in response.json()["joiners"]


# Test canceling an event by the organizer
def test_cancel_event():
    reset_events_db()  # Reset events before test
    response = client.post("/api/events/1/cancel", json={"user": "User A"})
    active_events = response.json()["events"]
    active_events = [event for event in active_events if event["status"] == "active"]
    assert response.status_code == 200
    assert len(active_events) == 1  # One event should be removed


# Test that non-organizers cannot cancel the event
def test_cancel_event_not_organizer():
    reset_events_db()  # Reset events before test
    response = client.post("/api/events/1/cancel", json={"user": "UserC"})
    assert response.status_code == 403  # UserX is not the organizer


# Test updating an event
def test_update_event():
    reset_events_db()  # Reset events before test
    update_data = {
        "title": "Updated Event Title",
        "organizer": "Updated Organizer",
        "date_time": "2024-10-20T10:00:00",
        "location": "Updated Venue"
    }
    response = client.post("/api/events/1/update", json=update_data)
    assert response.status_code == 200
    assert response.json()["event"]["title"] == "Updated Event Title"
    assert response.json()["event"]["location"] == "Updated Venue" 
