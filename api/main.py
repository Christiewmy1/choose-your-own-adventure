from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.engine import get_engine
from api.routers.profile import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_engine()  # load all data files once at startup
    yield


app = FastAPI(title="HuskyAdvisor API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://christiewmy1.github.io",  # Christy's deployed site
        "https://christiewmy1.github.io/choose-your-own-adventure/",
        "http://127.0.0.1:4173",
        "http://localhost:4173",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_origin_regex=r"(^https?://(localhost|127\.0\.0\.1)(:\d+)?$)|(^https://[a-zA-Z0-9-]+-[a-zA-Z0-9-]+\.hf\.space$)",
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(profile_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
