# import psycopg
from psycopg.rows import dict_row
from fastapi import Body, FastAPI
from pydantic_settings import BaseSettings
from . import models
from .database import engine
from .routers import post,user,auth

app=FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Wassup:)"}