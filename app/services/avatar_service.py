import re
import uuid
from datetime import datetime
from fastapi import UploadFile
from bson import ObjectId
from app.services.azure_service import upload_file_to_blob

async def create_avatar(db, user: dict, name: str, file: UploadFile):
    user_id = str(user["id"])
    full_name = user.get("full_name", "")
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', full_name).strip('-').lower()
    if not clean_name:
        clean_name = "user"

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    blob_path = f"{clean_name}-{user_id}/avatar/{unique_filename}"
    
    file_bytes = await file.read()
    azure_url = await upload_file_to_blob(
        file_stream=file_bytes, 
        blob_path=blob_path,
        content_type=file.content_type
    )
    
    avatar_doc = {
        "user_id": ObjectId(user_id),
        "name": name,
        "image_url": azure_url,
        "created_at": datetime.utcnow()
    }
    
    result = await db.avatars.insert_one(avatar_doc)
    avatar_doc["id"] = str(result.inserted_id)
    avatar_doc["user_id"] = str(avatar_doc["user_id"])
    return avatar_doc

async def get_user_avatars(db, user_id: str):
    cursor = db.avatars.find({"user_id": ObjectId(user_id)})
    avatars = await cursor.to_list(length=100)
    for av in avatars:
        av["id"] = str(av.pop("_id"))
        av["user_id"] = str(av["user_id"])
    return avatars