from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from datetime import datetime

async def register_user(db, user_in: UserCreate):
    existing_user = await db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_dict = user_in.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()

    result = await db.users.insert_one(user_dict)
    
    return {
        "id": str(result.inserted_id),
        "email": user_dict["email"],
        "full_name": user_dict["full_name"],
        "created_at": user_dict["created_at"]
    }

async def authenticate_user(db, email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user