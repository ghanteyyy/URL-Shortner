from fastapi import FastAPI
from db.session import engine
from db.base import Base
from routers import user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, tags=['user'])
