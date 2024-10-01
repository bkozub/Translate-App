from enum import StrEnum

from pydantic import BaseModel

SUPPORTED_LANGUAGES = ["de", "en", "el", "es", "fr", "it", "pl", "pt", "ro", "nl"]

SupportedLanguages = StrEnum('SupportedLanguages', {lang: lang for lang in SUPPORTED_LANGUAGES})


class TranslationRequest(BaseModel):
    text: str
    source_language: SupportedLanguages = "en"
    target_language: SupportedLanguages = "de"

    class Config:
        extra = "forbid"


class TranslationResponse(BaseModel):
    translated_text: str
