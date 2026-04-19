from fastapi import FastAPI
from db.session import engine
from db.base import Base
from auth import routes as auth_routes
from shortner import routes as shortner_routes
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortner API Docs", description="FastAPI URL shortener with JWT auth and PostgreSQL", docs_url=None)
app.mount('/static', StaticFiles(directory="static"), name="static")

app.include_router(auth_routes.router, prefix="/api/auth", tags=['auth'])
app.include_router(shortner_routes.router, tags=['shortner'])

@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="URL Shortner Docs",
        swagger_favicon_url="/static/icon.png",
    )
