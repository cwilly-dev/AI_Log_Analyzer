import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import auth, logs, users
from app.database.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.API_PREFIX

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(logs.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)

if __name__ == "__main__":
    uvicorn.run( "app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
