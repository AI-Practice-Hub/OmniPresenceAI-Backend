import re
import uuid
from datetime import datetime
from bson import ObjectId
from app.services.azure_service import download_blob_to_bytes, upload_file_to_blob, generate_sas_url
from app.services.tts_service import generate_tts_audio

async def create_run(db, user: dict, payload: dict):
	user_id = str(user["id"])
	now = datetime.utcnow()

	run_doc = {
		"user_id": ObjectId(user_id),
		"script": payload["script"],
		"audio_prompt_url": payload["audio_prompt_url"],
		"avatar_url": payload.get("avatar_url"),
		"name": payload.get("name"),
		"generated_audio_url": None,
		"status": "queued",
		"created_at": now,
		"updated_at": now,
		"error": None,
	}

	result = await db.runs.insert_one(run_doc)
	run_doc["id"] = str(result.inserted_id)
	run_doc["user_id"] = str(run_doc["user_id"])
	return run_doc

async def process_run_tts(db, user: dict, run_doc: dict):
	run_id = run_doc["id"]
	user_id = str(user["id"])
	now = datetime.utcnow()

	await db.runs.update_one(
		{"_id": ObjectId(run_id), "user_id": ObjectId(user_id)},
		{"$set": {"status": "processing", "updated_at": now}},
	)

	try:
		prompt_bytes = await download_blob_to_bytes(run_doc["audio_prompt_url"])
		wav_bytes = generate_tts_audio(run_doc["script"], prompt_bytes)

		full_name = user.get("full_name", "")
		clean_name = re.sub(r"[^a-zA-Z0-9]+", "-", full_name).strip("-").lower()
		if not clean_name:
			clean_name = "user"

		unique_filename = f"{uuid.uuid4()}_tts.wav"
		blob_path = f"{clean_name}-{user_id}/tts/{unique_filename}"

		azure_url = await upload_file_to_blob(
			file_stream=wav_bytes,
			blob_path=blob_path,
			content_type="audio/wav",
		)

		await db.runs.update_one(
			{"_id": ObjectId(run_id), "user_id": ObjectId(user_id)},
			{
				"$set": {
					"generated_audio_url": azure_url,
					"status": "completed",
					"updated_at": datetime.utcnow(),
					"error": None,
				}
			},
		)
	except Exception as exc:
		await db.runs.update_one(
			{"_id": ObjectId(run_id), "user_id": ObjectId(user_id)},
			{
				"$set": {
					"status": "failed",
					"updated_at": datetime.utcnow(),
					"error": str(exc),
				}
			},
		)

	updated = await get_run(db, user_id, run_id)
	if updated and updated.get("generated_audio_url"):
		updated["generated_audio_url"] = generate_sas_url(updated["generated_audio_url"])
	return updated

async def get_run(db, user_id: str, run_id: str):
	run = await db.runs.find_one({"_id": ObjectId(run_id), "user_id": ObjectId(user_id)})
	if not run:
		return None
	run["id"] = str(run.pop("_id"))
	run["user_id"] = str(run["user_id"])
	return run

async def list_runs(db, user_id: str):
	cursor = db.runs.find({"user_id": ObjectId(user_id)}).sort("created_at", -1)
	runs = await cursor.to_list(length=100)
	for run in runs:
		run["id"] = str(run.pop("_id"))
		run["user_id"] = str(run["user_id"])
	return runs
