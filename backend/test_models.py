import pytest
from pydantic import ValidationError
from models import EventUpdate
from datetime import datetime, timedelta
from models import EventUpdate, create_event, read_events, update_event
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio

def test_event_update_valid_data():
    event_data = {
        "title": "Annual Meeting",
        "organizer": "John Doe",
        "date_time": "2023-10-10 10:00:00",
        "location": "Conference Room A"
    }
    event = EventUpdate(**event_data)
    assert event.title == "Annual Meeting"
    assert event.organizer == "John Doe"
    assert event.date_time == "2023-10-10 10:00:00"
    assert event.location == "Conference Room A"

def test_event_update_missing_title():
    event_data = {
        "organizer": "John Doe",
        "date_time": "2023-10-10 10:00:00",
        "location": "Conference Room A"
    }
    with pytest.raises(ValidationError):
        EventUpdate(**event_data)

def test_event_update_invalid_date_time():
    event_data = {
        "title": "Annual Meeting",
        "organizer": "John Doe",
        "date_time": "invalid-date-time",
        "location": "Conference Room A"
    }
    with pytest.raises(ValidationError):
        EventUpdate(**event_data)
        def test_event_update_valid_data():
            event_data = {
                "title": "Annual Meeting",
                "organizer": "John Doe",
                "date_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "location": "Conference Room A"
            }
            event = EventUpdate(**event_data)
            assert event.title == "Annual Meeting"
            assert event.organizer == "John Doe"
            assert event.date_time.strftime("%Y-%m-%d %H:%M:%S") == event_data["date_time"]
            assert event.location == "Conference Room A"

        def test_event_update_missing_title():
            event_data = {
                "organizer": "John Doe",
                "date_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "location": "Conference Room A"
            }
            with pytest.raises(ValidationError):
                EventUpdate(**event_data)

        def test_event_update_invalid_date_time():
            event_data = {
                "title": "Annual Meeting",
                "organizer": "John Doe",
                "date_time": "invalid-date-time",
                "location": "Conference Room A"
            }
            with pytest.raises(ValidationError):
                EventUpdate(**event_data)

        def test_event_update_date_time_in_past():
            event_data = {
                "title": "Annual Meeting",
                "organizer": "John Doe",
                "date_time": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                "location": "Conference Room A"
            }
            with pytest.raises(ValidationError):
                EventUpdate(**event_data)
                @pytest.fixture(scope="module")
                def event_data():
                    return {
                        "title": "Annual Meeting",
                        "organizer": "John Doe",
                        "date_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        "location": "Conference Room A"
                    }

                @pytest.fixture(scope="module")
                def invalid_event_data():
                    return {
                        "title": "Annual Meeting",
                        "organizer": "John Doe",
                        "date_time": "invalid-date-time",
                        "location": "Conference Room A"
                    }

                @pytest.fixture(scope="module")
                def past_event_data():
                    return {
                        "title": "Annual Meeting",
                        "organizer": "John Doe",
                        "date_time": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        "location": "Conference Room A"
                    }

                @pytest.mark.asyncio
                async def test_create_event(event_data):
                    event = EventUpdate(**event_data)
                    event_id = await create_event(event)
                    assert ObjectId.is_valid(event_id)

                @pytest.mark.asyncio
                async def test_read_events(event_data):
                    event = EventUpdate(**event_data)
                    await create_event(event)
                    events = await read_events()
                    assert len(events) > 0
                    assert isinstance(events[0], EventUpdate)

                @pytest.mark.asyncio
                async def test_update_event(event_data):
                    event = EventUpdate(**event_data)
                    event_id = await create_event(event)
                    updated_data = event_data.copy()
                    updated_data["title"] = "Updated Meeting"
                    updated_event = EventUpdate(**updated_data)
                    modified_count = await update_event(event_id, updated_event)
                    assert modified_count == 1

                def test_event_update_valid_data(event_data):
                    event = EventUpdate(**event_data)
                    assert event.title == "Annual Meeting"
                    assert event.organizer == "John Doe"
                    assert event.date_time.strftime("%Y-%m-%d %H:%M:%S") == event_data["date_time"]
                    assert event.location == "Conference Room A"

                def test_event_update_missing_title():
                    event_data = {
                        "organizer": "John Doe",
                        "date_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                        "location": "Conference Room A"
                    }
                    with pytest.raises(ValidationError):
                        EventUpdate(**event_data)

                def test_event_update_invalid_date_time(invalid_event_data):
                    with pytest.raises(ValidationError):
                        EventUpdate(**invalid_event_data)

                def test_event_update_date_time_in_past(past_event_data):
                    with pytest.raises(ValidationError):
                        EventUpdate(**past_event_data)

