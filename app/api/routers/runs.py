from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.run import RunCreateRequest, RunResponse
from app.services.run_service import create_run, get_run, list_runs, process_run_tts
from app.api.dependencies import get_db, get_current_user

router = APIRouter(prefix="/runs", tags=["runs"])

@router.post("/", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def create_run_endpoint(
	request: RunCreateRequest,
	db = Depends(get_db),
	current_user = Depends(get_current_user)
):
	run_doc = await create_run(db, current_user, request.model_dump())
	return await process_run_tts(db, current_user, run_doc)

@router.get("/", response_model=List[RunResponse])
async def list_runs_endpoint(
	db = Depends(get_db),
	current_user = Depends(get_current_user)
):
	return await list_runs(db, current_user["id"])

@router.get("/{run_id}", response_model=RunResponse)
async def get_run_endpoint(
	run_id: str,
	db = Depends(get_db),
	current_user = Depends(get_current_user)
):
	run = await get_run(db, current_user["id"], run_id)
	if not run:
		raise HTTPException(status_code=404, detail="Run not found")
	return run
