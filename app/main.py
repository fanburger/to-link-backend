from fastapi import FastAPI
from .internal import admin
from .routers import items, users

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)
