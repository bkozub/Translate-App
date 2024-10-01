import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client(mocker):
    """Fixture to create a TestClient and mock StaticFiles for the FastAPI app."""
    # Mock StaticFiles to avoid mounting the static directory during tests
    mocker.patch.object(app, 'mount')
    return TestClient(app)


TRANSLATION_TEXT = "Hello, world!"

@pytest.fixture
def mock_translator(mocker):
    """Fixture to mock the CustomTranslator's _load_model method."""
    mock_model = mocker.MagicMock()
    mock_tokenizer = mocker.MagicMock()

    # Mock the model's generate method to return fake translation tokens
    mock_model.generate.return_value = [[1, 2, 3]]

    # Mock the tokenizer's decode method to return the mocked translation text
    mock_tokenizer.decode.return_value = TRANSLATION_TEXT

    # Patch the _load_model method to return the mocked model and tokenizer
    mocker.patch('api.services.translator.CustomTranslator._load_model', return_value=(mock_model, mock_tokenizer))


@pytest.mark.parametrize(
    "text,source_lang,target_lang",
    [
        ("Cześć, świecie!", "pl", "en"),
        ("Bonjour tout le monde", "fr", "en"),
        ("Hola mundo", "es", "en"),
        ("Hallo Welt", "de", "en"),
        ("Buongiorno mondo", "it", "en")
    ]
)
def test_translate_success(client, mock_translator, text, source_lang, target_lang):
    """ Test successful translation using CustomTranslator with different language pairs. """
    # Send a POST request to the translation API
    response = client.post("/translate/", json={
        "text": text,
        "source_language": source_lang,
        "target_language": target_lang
    })

    # Assert that the request was successful
    assert response.status_code == 200
    assert response.json() == {
        "translated_text": TRANSLATION_TEXT
    }


# Parametrize invalid text inputs
@pytest.mark.parametrize(
    "text",
    [
        1,  # Empty input
        None,  # None input
    ]
)
def test_translate_invalid_text_input(client, text):
    """ Test invalid text inputs that should trigger a 422 Unprocessable Entity error. """
    # Send a POST request with invalid text
    response = client.post("/translate/", json={
        "text": text,
        "source_language": "pl",
        "target_language": "en"
    })

    # Assert that the request returns a 422 error (Unprocessable Entity)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_translate_unsupported_language_pair(client):
    """ Test an unsupported language pair that should trigger a 400 error. """

    # Send a POST request with unsupported language pair
    response = client.post("/translate/", json={
        "text": "Cześć, świecie!",
        "source_language": "pl",
        "target_language": "pt"  # Unsupported pair
    })

    # Assert that the request returns a 400 error with the correct detail
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unsupported language pair: pl -> pt"
    }

