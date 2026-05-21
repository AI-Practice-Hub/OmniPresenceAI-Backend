from pydantic import BaseModel
from datetime import datetime

class AudioResponse(BaseModel):
    id: str
    user_id: str
    name: str
    audio_url: str
    created_at: datetime