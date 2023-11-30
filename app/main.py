from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="Bonito Project", docs_url="/api")

# To run enter from the project home (where the Readme is) : uvicorn app.main:app --reload

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
