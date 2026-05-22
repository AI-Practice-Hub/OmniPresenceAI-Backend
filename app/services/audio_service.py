import re
import uuid
from datetime import datetime
from fastapi import UploadFile
from bson import ObjectId
from app.services.azure_service import upload_file_to_blob, generate_sas_url

async def create_audio(db, user: dict, name: str, file: UploadFile):
    user_id = str(user["id"])
    full_name = user.get("full_name", "")
    clean_name = re.sub(r'[^a-zA-Z0-9]+', '-', full_name).strip('-').lower()
    if not clean_name:
        clean_name = "user"

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    blob_path = f"{clean_name}-{user_id}/audio/{unique_filename}"
    
    file_bytes = await file.read()
    azure_url = await upload_file_to_blob(
        file_stream=file_bytes, 
        blob_path=blob_path,
        content_type=file.content_type
    )
    
    audio_doc = {
        "user_id": ObjectId(user_id),
        "name": name,
        "audio_url": azure_url,
        "created_at": datetime.utcnow()
    }
    
    result = await db.audios.insert_one(audio_doc)
    audio_doc["id"] = str(result.inserted_id)
    audio_doc["user_id"] = str(audio_doc["user_id"])
    
    # Generate SAS URL for the response so user can immediately view/listen
    audio_doc["audio_url"] = generate_sas_url(audio_doc["audio_url"])
    
    return audio_doc

async def get_user_audios(db, user_id: str):
    cursor = db.audios.find({"user_id": ObjectId(user_id)})
    audios = await cursor.to_list(length=100)
    for au in audios:
        au["id"] = str(au.pop("_id"))
        au["user_id"] = str(au["user_id"])
        # Generate SAS URL for every fetched audio file
        au["audio_url"] = generate_sas_url(au["audio_url"])
    return audios