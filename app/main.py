from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app import models
from app.api import api_router


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(api_router)
    return app


app = create_app()
