from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from typing import List
from app.schemas.avatar import AvatarResponse
from app.services.avatar_service import create_avatar, get_user_avatars
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/avatars", tags=["avatars"])

@router.post("/", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def upload_avatar(
    name: str = Form(...),
    file: UploadFile = File(...),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await create_avatar(db, current_user, name, file)

@router.get("/", response_model=List[AvatarResponse])
async def list_avatars(db = Depends(get_db), current_user = Depends(get_current_user)):
    return await get_user_avatars(db, current_user["id"])