from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.middleware.auth_middleware import AuthenticationMiddleware


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthenticationMiddleware,
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health():
    return {
        "success": True,
        "message": "Core API is running.",
        "data": {
            "status": "healthy",
        },
        "errors": None,
    }