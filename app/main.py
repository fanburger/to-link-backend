from fastapi import FastAPI

from app.internal import admin
from app.routers import items, users
from app.sql.database import create_db_and_tables

app = FastAPI()


@app.on_event('startup')
def create_tables():
    create_db_and_tables()


app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)
