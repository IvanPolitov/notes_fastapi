from fastapi import FastAPI
from notes_app.routers.notes import notes_router
from notes_app.database import engine
from notes_app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(notes_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API!"}
