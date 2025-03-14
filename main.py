from fastapi import FastAPI

from routers.notes import notes_router
from routers.auth import auth_router
from routers.users import users_router

from database.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(notes_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Notes API!"}
