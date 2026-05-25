import io
import re
import tempfile
from typing import List

import torch
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS

_model = None


def _get_model() -> ChatterboxTurboTTS:
    global _model
    if _model is None:
        _model = ChatterboxTurboTTS.from_pretrained(device="cpu")
    return _model


def _chunk_text(text: str, max_chars: int) -> List[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


def generate_tts_audio(
    script: str,
    audio_prompt_bytes: bytes,
    max_chars: int = 320,
    silence_seconds: float = 0.2,
) -> bytes:
    model = _get_model()
    chunks = _chunk_text(script, max_chars=max_chars)
    silence_samples = int(model.sr * silence_seconds)
    silence = torch.zeros(silence_samples)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_file.write(audio_prompt_bytes)
        temp_path = temp_file.name

    parts = []
    try:
        for idx, chunk in enumerate(chunks, start=1):
            wav_chunk = model.generate(chunk, audio_prompt_path=temp_path)
            if wav_chunk.dim() > 1:
                wav_chunk = wav_chunk[0]
            parts.append(wav_chunk.cpu())
            if idx < len(chunks):
                parts.append(silence)

        full_wav = torch.cat(parts, dim=0)
        buffer = io.BytesIO()
        ta.save(buffer, full_wav.unsqueeze(0), model.sr, format="wav")
        return buffer.getvalue()
    finally:
        try:
            import os

            os.remove(temp_path)
        except OSError:
            pass
