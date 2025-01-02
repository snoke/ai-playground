from fastapi import FastAPI, UploadFile, Form, Body
import whisper
class Whisper:
    def __init__(self):
        self.model = whisper.load_model("base")
    async def transcribe_audio(self,file: UploadFile, language: str = Form(...)):
        with open(file.filename, "wb") as audio:
            audio.write(await file.read())
        return self.model.transcribe(file.filename, language=language)