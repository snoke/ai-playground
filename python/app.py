from fastapi import FastAPI, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from transformers import MarianMTModel, MarianTokenizer
import json
from transformers import AutoProcessor, AutoModelForImageTextToText
import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
from models.whisper import Whisper
from models.opus_en_mul import OpusEnMul
from models.opus_mul_en import OpusMulEn
from models.phi3mini import Phi3mini
app = FastAPI()
#phi3mini = Phi3mini("/root/.cache/huggingface/hub/models--microsoft--Phi-3.5-mini-instruct/snapshots/af0dfb8029e8a74545d0736d30cb6b58d2f0f3f0");
print('loading phi3mini')
phi3mini = Phi3mini()
print('loading phi3mini finished')
opusenmul = OpusEnMul()
opusmulen = OpusMulEn()
# CORS Middleware hinzufügen
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Sprachsets aus mul.json laden
with open("mul.json", "r") as f:
    mul_languages = json.load(f)


def normalize_language(lang_code: str) -> str:
    """
    Prüft, ob eine Sprache in der mul.json vorhanden ist, und gibt das normalisierte Sprachset zurück.
    Falls die Basisform (z. B. 'deu') nicht vorhanden ist, wird eine alternative Form wie 'deu_Latn' verwendet.
    """
    base_lang = lang_code.split("_")[0]  # Entfernt den Unterstrich und alles danach, falls vorhanden
    # Zuerst Basisform prüfen
    if base_lang in mul_languages:
        return base_lang
    # Alternative Formen prüfen
    for alternative in mul_languages:
        if alternative.startswith(base_lang):
            return alternative
    # Sprache nicht gefunden
    raise ValueError(f"Sprache {lang_code} wurde nicht in mul.json gefunden.")



@app.post("/chat/")
async def chat(body: dict = Body(...)):
    messages = body.get("messages")
    result = phi3mini.prompt(messages)
    print(result)
    return result

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile, language: str = Form(...)):
    with open(file.filename, "wb") as audio:
        audio.write(await file.read())
    result = Whisper.transcribe(file, language)
    return {"transcription": result["text"]}


@app.post("/translate/")
def translate_text(body: dict = Body(...)):
    text = body.get("text")
    from_lang = body.get("from_language", "deu")
    to_lang = body.get("to_language", "eng")

    try:
        # Sprache normalisieren
        from_lang_normalized = normalize_language(from_lang)
        to_lang_normalized = normalize_language(to_lang)

        # Übersetzung von Quellsprache nach Englisch
        if from_lang_normalized != "eng":
            print(f"Übersetze von {from_lang} nach Englisch")

            intermediate_text = opusmulen.translate(text, from_lang)
        else:
            intermediate_text = text
        print(intermediate_text)

        # Übersetzung von Englisch in Zielsprache
        if to_lang_normalized != "eng":
            print(f"Übersetze von Englisch nach {to_lang}")
            translated_text = opusenmul.translate(intermediate_text, to_lang)
        else:
            translated_text = intermediate_text
        print(translated_text)
        return {"translation": {"message": translated_text, "from": from_lang_normalized, "to": to_lang}}

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}

print("Laden fertig")