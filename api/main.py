from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from api import utils
from api.schemas.translate import TranslationRequest, TranslationResponse
from api.services.translator import CustomTranslator


app = FastAPI()

app.mount("/static", StaticFiles(directory=utils.get_project_root() / "static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.post("/translate")
async def translate_text(request: TranslationRequest) -> TranslationResponse:
    translator = CustomTranslator(request.source_language, request.target_language)
    translation = translator.translate(request.text)

    return TranslationResponse(translated_text=translation)

