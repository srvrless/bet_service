import enum
from typing import Optional
from db.models import BetStatus
from pydantic import BaseModel, condecimal


class EventStatus(enum.Enum):
    pending = "pending"
    team1_won = "team1_won"
    team2_won = "team2_won"


class BetCreate(BaseModel):
    event_id: str
    team: str
    amount: condecimal(gt=0, decimal_places=2)  # type: ignore


class BetEdit(BaseModel):
    event_id: str
    status: EventStatus


class BetResponse(BaseModel):
    id: int
    event_id: str
    amount: float
    status: BetStatus
