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
        "http://localhost:5173",  # Vite (Christy's frontend)
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(profile_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
