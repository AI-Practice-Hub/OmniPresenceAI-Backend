from pydantic import BaseModel
from datetime import datetime

class AvatarResponse(BaseModel):
    id: str
    user_id: str
    name: str
    image_url: str
    created_at: datetime