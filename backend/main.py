# backend/main.py

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import EventUpdate, UserAction
from typing import List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# In-memory database to store events
events_db = [
    {"id": 1, "title": "Event 1", "organizer": "User A", "date_time": "2024-10-14T15:00:00", "duration": 2, "location": "Venue A", "joiners": [], "status": "active"},
    {"id": 2, "title": "Event 2", "organizer": "User B", "date_time": "2024-10-15T18:00:00", "duration": 3, "location": "Venue B", "joiners": [], "status": "active"},
]

# List of connected clients for WebSocket communication
clients = []

@app.get("/api/events")
async def get_events():
    """Fetch all events"""
    return {"events": events_db}


@app.post("/api/events/{event_id}/update")
async def update_event(event_id: int, event_update: EventUpdate):
    # Find the event by ID
    for event in events_db:
        if event["id"] == event_id:
            # Update the event details
            event["title"] = event_update.title
            event["organizer"] = event_update.organizer
            event["date_time"] = event_update.date_time
            event["location"] = event_update.location
            await notify_clients(event)  # Notify clients via WebSocket
            return {"message": "Event updated successfully", "event": event}
    
    raise HTTPException(status_code=404, detail="Event not found")


@app.post("/api/events/{event_id}/join")
async def join_event(event_id: int, action: UserAction):
    """Join an event"""
    for event in events_db:
        if event["id"] == event_id:
            if action.user not in event["joiners"]:
                event["joiners"].append(action.user)
                await notify_clients(event)  # Notify all clients about the update
                return event
            return {"message": "User already joined"}
    return JSONResponse(content={"message": "Event not found"}, status_code=404)


@app.post("/api/events/{event_id}/leave")
async def leave_event(event_id: int, action: UserAction):
    """Leave an event"""
    for event in events_db:
        if event["id"] == event_id:
            if action.user in event["joiners"]:
                event["joiners"].remove(action.user)
                await notify_clients(event)  # Notify all clients about the update
                return event
    return JSONResponse(content={"message": "Event not found"}, status_code=404)


@app.post("/api/events/{event_id}/cancel")
async def cancel_event(event_id: int, user: UserAction):
    """Cancel an event (only the organizer can cancel)"""
    global events_db
    for event in events_db:
        if event["id"] == event_id:
            if  event["organizer"] == user.user:
                event["status"] = "cancelled"
                await notify_clients(event)  # Notify all clients
                return {"events": events_db}
            else:
                raise HTTPException(status_code=403, detail="Only the organizer can cancel the event")
    return JSONResponse(content={"message": "Event not found"}, status_code=404)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection handler"""
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except:
        clients.remove(websocket)


async def notify_clients(event):
    """Notify all connected WebSocket clients about the updated event"""
    for client in clients:
        await client.send_json(event)
