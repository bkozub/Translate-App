from fastapi import HTTPException
from transformers import MarianMTModel, MarianTokenizer, MarianModel

from api.schemas.translate import SupportedLanguages


class CustomTranslator:
    def __init__(self, source_language: SupportedLanguages, target_language: SupportedLanguages):
        self.source_language = source_language
        self.target_language = target_language

    def _load_model(self) -> (MarianModel, MarianTokenizer):
        """ Load the MarianMT model dynamically based on the source and target language. """
        model_name = f"Helsinki-NLP/opus-mt-{self.source_language}-{self.target_language}"
        try:
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
            return model, tokenizer
        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Unsupported language pair: {self.source_language} -> {self.target_language}")

    def translate(self, text: str) -> str:
        model, tokenizer = self._load_model()

        # Tokenize the input text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Generate translation
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.decode(translated_tokens[0],
                                           skip_special_tokens=True)

        return str(translated_text)
