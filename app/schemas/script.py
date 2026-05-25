from pydantic import BaseModel

class ScriptGenerateRequest(BaseModel):
    idea: str

class ScriptGenerateResponse(BaseModel):
    script: str
