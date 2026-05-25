# OmniPresenceAI - Project Context for Agents

## Project Vision & Goal
**OmniPresenceAI** is an AI-driven video generation platform. The system allows users to create personalized videos where a digital avatar speaks a script using their customized cloned voice.

The core generation pipeline works as follows:
1. **Assets (Onboarding):** A user uploads a picture of themselves (Avatar) and a sample of their voice (Audio).
2. **Script Generation:** The user prompts the system with a rough idea. An LLM refines this into a professional, well-paced script (with pauses, emphasis, etc.).
3. **Voice Synthesis (TTS):** The system uses a TTS engine (e.g., ElevenLabs, Chatterbox) to generate audio of the script matching the user's cloned voice.
4. **Lip-Sync Video Generation:** A lip-sync model processes the user's Avatar and the generated TTS audio to produce the final speaking video.

## Technical Architecture (Backend)
- **Language & Framework:** Python 3.10+, FastAPI (Asynchronous)
- **Database:** MongoDB (using `motor` for async I/O)
- **Cloud Storage:** Azure Blob Storage (Blobs are kept private; we securely serve them to the frontend using dynamically generated SAS tokens)
- **Package Management:** Poetry
- **Authentication:** JWT (JSON Web Tokens), `passlib` with `bcrypt`.

## Current Implementation Status
The foundational backend Proof of Concept (POC) is established:
- **Authentication:** Users can sign up, securely hash passwords, and log in to receive a JWT access token.
- **Asset Management (`/api/avatars` & `/api/audios`):**
  - Users can securely upload their avatar images and audio voice samples via `multipart/form-data`.
  - Files are uploaded to Azure Blob Storage under strict, user-isolated logical paths: `sanitizedname-userid/avatar/uuid_filename`.
  - MongoDB documents map these assets securely to the respective `user_id`.
  - File retrieval endpoints automatically generate 1-hour read-only SAS (Shared Access Signature) tokens so the frontend can securely render private assets.
- **CORS:** Configured to allow all origins during development.

## Next Phases (Roadmap)
- **Agentic / LLM Pipeline:** Create a service or agent framework to take user thoughts and output formatted scripts for the TTS engine.
- **TTS Integration:** Connect to third-party voice generators to synthesize the audio.
- **Video Generation API:** Implement or connect to the lip-sync AI models.
- **Background Job Queue:** Because video generation is a heavy, slow process, we will need to integrate a task worker queue (e.g., Celery + Redis or FastAPI BackgroundTasks) to process videos asynchronously without timing out HTTP requests.

## Working Guidelines for AI Agents
- **Separation of Concerns:** Keep HTTP routing (`app/api/routers/`) and business logic (`app/services/`) strictly separated.
- **Async First:** Always leverage asynchronous boundaries (`async`/`await`), especially for Database and Cloud Storage I/O.
- **Security:** Do not expose secrets or passwords in responses. Serve private cloud assets via SAS tokens ONLY.
