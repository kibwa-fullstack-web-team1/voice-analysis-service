from fastapi import FastAPI
from app.api import analysis_router
from app.config.config import config_by_name

def create_app(config_name: str):
    app = FastAPI(
        title="Voice Analysis Service",
        description="음성 파일을 분석하여 인지 건강 점수를 제공하는 서비스",
        version="0.1.0",
    )

    config = config_by_name[config_name]
    app.config = config

    app.include_router(analysis_router.router, prefix="/api", tags=["Analysis"])

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Voice Analysis Service", "phase": app.config.PHASE}

    return app
