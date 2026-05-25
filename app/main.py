from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routers import auth, avatars, audios, scripts, runs

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="OmniPresenceAI API", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers
app.include_router(auth.router, prefix="/api")
app.include_router(avatars.router, prefix="/api")
app.include_router(audios.router, prefix="/api")
app.include_router(scripts.router, prefix="/api")
app.include_router(runs.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to OmniPresenceAI API"}