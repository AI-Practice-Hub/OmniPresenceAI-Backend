from fastapi import APIRouter, Depends
from app.schemas.script import ScriptGenerateRequest, ScriptGenerateResponse
from app.services.script_service import generate_script_async
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/scripts", tags=["Scripts"])

@router.post("/generate", response_model=ScriptGenerateResponse)
async def generate_script(
    request: ScriptGenerateRequest, 
    current_user=Depends(get_current_user)
):
    """
    Generate a professional spoken-word script based on a rough user idea.
    """
    generated_script = await generate_script_async(request.idea)
    return ScriptGenerateResponse(script=generated_script)
