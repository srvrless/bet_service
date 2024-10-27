import uuid
from typing import List, Optional

import aiohttp
from fastapi import APIRouter, HTTPException
from schemas.events import (
    Event,
    EventCreate,
    EventStatus,
    EventStatusUpdate,
)

router = APIRouter()
events_db = {}
BET_MAKER_URL = "http://127.0.0.1:8888/api/v1"


@router.post("", response_model=Event)
async def create_event(event_data: EventCreate):
    event_id = str(uuid.uuid4())
    event = Event(
        id=event_id,
        coefficient=round(event_data.coefficient, 2),
        deadline=event_data.deadline,
        status=EventStatus.pending,
    )
    events_db[event_id] = event
    return event


@router.get("/all", response_model=List[Event])
async def get_events(id: Optional[str] = None):
    if id:
        if id not in events_db:
            raise HTTPException(status_code=404, detail="Event not found")
        return [events_db[id]]
    return list(events_db.values())


@router.patch("/{event_id}/status", response_model=Event)
async def update_event_status(event_id: str, status_update: EventStatusUpdate):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    event = {}
    event_response = events_db[event_id]
    event_response.status = status_update.status
    event["event_id"] = event_id
    event["status"] = str(status_update.status)
    print(event)
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{BET_MAKER_URL}/bets/status", json=event):
            return event_response


@router.delete("/{event_id}")
async def delete_event(event_id: str):
    if event_id not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")

    del events_db[event_id]
    return {"message": "Event deleted successfully"}
