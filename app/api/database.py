from enum import Enum

from fastapi import APIRouter, Response

from app.Database.clients import Clients
from app.Database.games import Games


router = APIRouter()


class TableList(str, Enum):
    Clients = "Clients"
    Games = "Games"


@router.get("/dbTest")
async def get_test(self):
    # This is a test don't push that to main
    data = ""
    db = Games()
    db.add_game("PacMan", "Arcade", 2, 120)
    data = db.get_all_table()
    return data


@router.get("/{table}")
async def get_table(table: TableList):
    return (
        Clients().get_all_table() if table == "Clients" else Games().get_all_table(),
        Response(status_code=200),
    )
