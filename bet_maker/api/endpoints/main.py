from datetime import datetime
from typing import List

import aiohttp
from db.connection import async_get_session
from db.models import Bet
from fastapi import APIRouter, Depends, HTTPException
from schemas.bets import BetCreate, BetEdit, BetResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
LINE_PROVIDER_URL = "http://127.0.0.1:7777/api/v1"


@router.get("/events")
async def get_available_events():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{LINE_PROVIDER_URL}/events/all") as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail="Could not fetch events"
                )

            events = await response.json()
            print(events)
            available_events = [
                event for event in events if event["status"] == "pending"
            ]
            return available_events


@router.post("")
async def place_bet(
    bet_data: BetCreate, session: AsyncSession = Depends(async_get_session)
):
    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(
            f"{LINE_PROVIDER_URL}/events/all?id={bet_data.event_id}"
        ) as response:
            event = (await response.json())[0]
            print(event)
            if response.status != 200 or not await response.json():
                raise HTTPException(status_code=404, detail="Event not found")

            if event["status"] != "pending" and event["deadline"] <= datetime.now:
                raise HTTPException(
                    status_code=400, detail="Betting on this event is closed"
                )

            stmt = select(Bet).filter_by(event_id=bet_data.event_id)
            res = await session.execute(stmt)
            res = res.fetchone()
            if res:
                raise HTTPException(
                    status_code=400, detail="You've already bet on this event"
                )

            new_bet = Bet(
                event_id=bet_data.event_id, amount=bet_data.amount, team=bet_data.team
            )
            session.add(new_bet)
            await session.commit()
            await session.refresh(new_bet)

            return new_bet


@router.get("", response_model=List[BetResponse])
async def get_bets(session: AsyncSession = Depends(async_get_session)):
    stmt = select(Bet)
    result = await session.execute(stmt)
    bets = result.scalars().all()
    return bets


@router.patch("/status")
async def edit_bet_status(
    bet_data: dict, session: AsyncSession = Depends(async_get_session)
):
    query = select(Bet).filter_by(event_id=bet_data["event_id"])
    stmt = await session.execute(query)
    res = stmt.scalar_one()

    if res.team in bet_data["status"]:
        bet_data["status"] = "won"
    else:
        bet_data["status"] = "lost"
    print(bet_data)
    query = update(Bet).values(bet_data).filter_by(event_id=bet_data["event_id"])
    stmt = await session.execute(query)
    await session.commit()
    return bet_data
