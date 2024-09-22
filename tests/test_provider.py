import pytest
from unittest.mock import patch, MagicMock
import os
import tempfile
from navamai.provider import Provider

class MockProvider(Provider):
    def create_request_data(self, prompt: str) -> dict:
        return {"prompt": prompt}

    def stream_response(self, prompt: str):
        yield "Test response"

    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str = None):
        yield "Test vision response"

@pytest.fixture
def mock_provider():
    return MockProvider()

def test_init(mock_provider):
    assert mock_provider.full_config == mock_provider.full_config
    assert mock_provider.model_config == mock_provider.full_config.get("ask-model-config", {})

def test_set_model_config(mock_provider):
    mock_provider.set_model_config("test-config")
    assert mock_provider.model_config == mock_provider.full_config.get("test-config", {})

@patch('navamai.provider.Live')
@patch('navamai.provider.Markdown')
def test_ask(mock_markdown, mock_live, mock_provider):
    mock_live_instance = MagicMock()
    mock_live.return_value.__enter__.return_value = mock_live_instance

    result = mock_provider.ask("Test prompt")

    mock_live.assert_called_once()
    mock_live_instance.update.assert_called()
    mock_markdown.assert_called()
    assert result is None  # Since save is not set to True in the default config

def test_vision(mock_provider):
    image_data = b"fake_image_data"
    prompt = "Describe this image"
    response = list(mock_provider.vision(image_data, prompt))
    assert response == ["Test vision response"]

def test_save_response(mock_provider):
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_provider.model_config["save-folder"] = temp_dir
        mock_provider.model_config["save"] = True

        filepath = mock_provider.save_response("Test prompt", "Test response", "Test Title")

        assert os.path.exists(filepath)
        with open(filepath, 'r') as f:
            content = f.read()
            assert content == "Test response"

def test_get_model_info(mock_provider):
    mock_provider.model_config["model"] = "test-model"
    assert mock_provider.get_model_info() == "MockProvider - test-model"

def test_resolve_model(mock_provider):
    mock_provider.full_config["model-mapping"] = {"alias": "real-model"}
    assert mock_provider.resolve_model("alias") == "real-model"
    assert mock_provider.resolve_model("unknown") == "unknown"