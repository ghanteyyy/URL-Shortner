from fastapi import FastAPI
from db.session import engine
from db.base import Base
from auth import routes as auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_routes.router, prefix="/api/auth", tags=['auth'])
