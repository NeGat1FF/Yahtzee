from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import randint
import aiosqlite

DB_PATH = "sqlite.db"

combos = {
    "Pair": 0.86,
    "Full House": 1.71,
    "Yahtzee": 2.57,
    "Three Pairs": 3.42,
    "Other": 0.0
}


def roll():
    results = [randint(1, 6) for _ in range(6)]

    count = {}
    for num in results:
        count[num] = count.get(num, 0) + 1

    values = list(count.values())

    if 6 in values:
        return "Yahtzee", results
    elif 4 in values and 2 in values:
        return "Full House", results
    elif values.count(2) == 3:
        return "Three Pairs", results
    elif values.count(2) in (1,2) or 3 in values or 4 in values or 5 in values:
        return "Pair", results
    else:
        return "Other", results


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await aiosqlite.connect(DB_PATH)
    app.state.db = db
    async with db.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='transactions'
    """) as cursor:
        table_exists = await cursor.fetchone()

    if not table_exists:
        # Create the table and insert initial data
        await db.execute("""
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value FLOAT NOT NULL,
                type VARCHAR(255) NOT NULL
            )
        """)
        await db.execute("INSERT INTO transactions (value, type) VALUES (?, ?)", (100.0, 'init'))
        await db.commit()
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


async def get_balance(db):
    async with db.execute("SELECT COALESCE(SUM(value), 0) FROM transactions") as cursor:
        row = await cursor.fetchone()
        return row[0] if row else 0.0


class Bet(BaseModel):
    amount: float


@app.get("/api/v1/balance")
async def api_get_balance():
    balance = await get_balance(app.state.db)
    return {"balance": balance}

@app.get("/api/v1/combinations")
async def get_combinations():
    return combos


@app.post("/api/v1/bet")
async def place_bet(bet: Bet = Body(...)):
    db = app.state.db
    balance = await get_balance(db)

    print(bet)

    if bet.amount > balance:
        raise HTTPException(status_code=400, detail="Not enough money to place a bet")
    elif bet.amount <= 0:
        raise HTTPException(status_code=400, detail="Bet must be greater than 0")

    await db.execute("INSERT INTO transactions (value, type) VALUES (?, 'bet')", (-bet.amount,))
    await db.commit()

    combo, dices = roll()

    if combo != "Other":
        win_amount = bet.amount * combos[combo]
        await db.execute("INSERT INTO transactions (value, type) VALUES (?, 'win')", (win_amount,))
        await db.commit()

    return {"result": combo, "dice": dices}
