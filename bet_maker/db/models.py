import enum
from datetime import datetime

from db.connection import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column


class BetStatus(enum.Enum):
    pending = "pending"
    won = "won"
    lost = "lost"


class Bet(Base):
    __tablename__ = "bets"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[str] = mapped_column(unique=True)
    amount: Mapped[int]
    team: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[Enum] = mapped_column(Enum(BetStatus), default=BetStatus.pending)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
