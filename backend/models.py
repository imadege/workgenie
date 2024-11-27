from pydantic import BaseModel, field_validator
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import asyncio
import os

# MongoDB connection setup
connection_string = os.getenv("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017/")    
client = AsyncIOMotorClient(connection_string)
db = client["event_database"]
collection = db["events"]

class EventUpdate(BaseModel):
    """
    EventUpdate model represents the structure of an event update with the following attributes:
    - title: The title of the event.
    - organizer: The organizer of the event.
    - date_time: The date and time of the event in datetime format.
    - location: The location where the event will take place.
    """
    title: str
    organizer: str
    date_time: datetime
    location: str

    @field_validator('date_time')
    def date_time_not_in_past(cls, value):
        """
        Validator to ensure the date_time is not in the past.
        """
        if value < datetime.now():
            raise ValueError('date_time must not be in the past')
        return value

async def create_event(event: EventUpdate) -> str:
    """
    Asynchronously create an event in the database.

    Args:
        event (EventUpdate): The event data to be inserted.

    Returns:
        str: The ID of the created event.
    """
    event_dict = event.model_dump()
    result = await collection.insert_one(event_dict)
    return str(result.inserted_id)

async def read_events() -> List[EventUpdate]:
    """
    Asynchronously read all events from the database.

    Returns:
        List[EventUpdate]: A list of EventUpdate objects.
    """
    events_cursor = collection.find()
    events = await events_cursor.to_list(length=None)
    return [EventUpdate(**event) for event in events]

async def update_event(event_id: str, event: EventUpdate) -> int:
    """
    Asynchronously update an event in the database.

    Args:
        event_id (str): The ID of the event to be updated.
        event (EventUpdate): The new event data.

    Returns:
        int: The number of documents updated.
    """
    event_dict = event.dict()
    result = await collection.update_one({"_id": ObjectId(event_id)}, {"$set": event_dict})
    return result.modified_count
