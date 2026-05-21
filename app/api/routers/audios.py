from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from typing import List
from app.schemas.audio import AudioResponse
from app.services.audio_service import create_audio, get_user_audios
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/audios", tags=["audios"])

@router.post("/", response_model=AudioResponse, status_code=status.HTTP_201_CREATED)
async def upload_audio(
    name: str = Form(...),
    file: UploadFile = File(...),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await create_audio(db, current_user, name, file)

@router.get("/", response_model=List[AudioResponse])
async def list_audios(db = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_user_audios(db, current_user["id"])