from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import whisper
import tempfile
import os
from typing import Dict, Any, Optional

class WhisperConfig(BaseModel):
    model_name: str = "large"   # Other available: base, tiny (and more)
    host: str = "0.0.0.0"
    port: int = 8000

class WhisperTranscriptionService:
    def __init__(self, config: Optional[WhisperConfig] = None):
        self.config = config or WhisperConfig()
        self.app = FastAPI(title="Whisper Transcription API")
        self.model = None

        # Register route
        self.app.add_api_route("/transcribe/", self.transcribe_audio, methods=["POST"])

    async def load_model(self):
        try:
            self.model = whisper.load_model(self.config.model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model: {str(e)}")

    async def transcribe_audio(self, file: UploadFile = File(...)) -> Dict[str, Any]:
        if not self.model:
            await self.load_model()

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file.flush()

                result = self.model.transcribe(temp_file.name)
                os.unlink(temp_file.name)

                return {
                    "text": result["text"],
                    "language": result["language"],
                    "segments": result["segments"]
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def start(self):
        import uvicorn
        uvicorn.run(self.app, host=self.config.host, port=self.config.port)

if __name__ == "__main__":
    service = WhisperTranscriptionService()
    service.start()

