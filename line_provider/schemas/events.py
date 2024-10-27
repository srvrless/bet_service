import enum
from datetime import datetime

from pydantic import BaseModel


class EventStatus(enum.Enum):
    pending = "pending"
    team1_won = "team1_won"
    team2_won = "team2_won"


class Event(BaseModel):
    id: str
    coefficient: float
    deadline: datetime
    status: EventStatus


class EventCreate(BaseModel):
    coefficient: float
    deadline: datetime


class EventStatusUpdate(BaseModel):
    status: EventStatus
