from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="OmniPresenceAI API", lifespan=lifespan)

# Add Routers
app.include_router(auth.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to OmniPresenceAI API"}