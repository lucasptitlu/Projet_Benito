from enum import Enum
from typing import Optional

from fastapi import APIRouter, Response

from app.Database.clients import Clients
from app.Database.games import Games


router = APIRouter()


class TableList(str, Enum):
    Clients = "Clients"
    Games = "Games"


# @router.get("/dbTest")
# async def get_test(self):
#     # This is a test don't push that to main
#     data = ""
#     db = Games()
#     db.add_game("PacMan", "Arcade", 2, 120)
#     data = db.get_all_table()
#     return data


@router.put("/credit")
async def credit(id: int, bonito: int):
    return (
        Clients().credit_by_id(id, bonito),
        Response(content="Youpi c'est cool ", status_code=200),
    )


@router.get("/{table}")
async def get_table(table: TableList):
    return (
        Clients().get_all_table() if table == "Clients" else Games().get_all_table(),
        Response(status_code=200),
    )


@router.put("/add/client")
async def add_to_table(
    table: TableList,
    name: str,
    email: str,
    bonito: Optional[int] = 0,
    bonitard: Optional[int] = 0,
):
    return (
        Clients().add_client(table, name, email, bonito, bonitard),
        Response(status_code=200),
    )


@router.put("/add/games")
async def add_to_table(
    name: str,
    category: str,
    min_ratio: int,
    hour_ratio: Optional[int] = 0,
):
    return (
        Games().add_game(name, category, min_ratio, hour_ratio),
        Response(status_code=200),
    )


@router.put("/game/start")
async def start_game(
    id: int,
):
    return (
        Games().start_game(id),
        Response(status_code=200),
    )


@router.put("/game/end")
async def end_game(
    id: int,
):
    return (
        Games().end_game(id),
        Response(status_code=200),
    )
