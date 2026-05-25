from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RunCreateRequest(BaseModel):
	script: str
	audio_prompt_url: str
	avatar_url: Optional[str] = None
	name: Optional[str] = None

class RunResponse(BaseModel):
	id: str
	user_id: str
	script: str
	audio_prompt_url: str
	avatar_url: Optional[str] = None
	name: Optional[str] = None
	generated_audio_url: Optional[str] = None
	status: str
	created_at: datetime
	updated_at: datetime
	error: Optional[str] = None
