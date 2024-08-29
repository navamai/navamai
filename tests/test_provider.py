# test_provider.py

import pytest
from unittest.mock import patch, mock_open, MagicMock
from navamai.provider import Provider

@pytest.fixture
def mock_provider():
    class MockProvider(Provider):
        def create_request_data(self, prompt: str) -> dict:
            return {"prompt": prompt}

        def stream_response(self, prompt: str):
            yield "Test response"

    return MockProvider()

def test_provider_set_model_config(mock_provider):
    mock_config = {"ask": {"model": "test-model"}}
    with patch.object(mock_provider, "full_config", mock_config):
        mock_provider.set_model_config("ask")
        assert mock_provider.model_config == {"model": "test-model"}

@pytest.mark.parametrize("title, expected", [
    ("Test Title", "Test Title.md"),
    ("Test: Title", "Test Title.md"),
    ("Test/Title", "TestTitle.md"),
])
def test_provider_save_response(mock_provider, title, expected):
    mock_provider.model_config = {"folder": "responses", "save": True}
    
    with patch("os.makedirs"), patch("builtins.open", mock_open()), patch("os.path.join", return_value=f"responses/{expected}"):
        result = mock_provider.save_response("Test prompt", "Test response", title)
        assert result == f"responses/{expected}"

def test_get_model_info(mock_provider):
    mock_provider.model_config = {"model": "test-model"}
    assert mock_provider.get_model_info() == "MockProvider - test-model"

def test_resolve_model(mock_provider):
    mock_provider.full_config = {"model-mapping": {"model-a": "model-b"}}
    assert mock_provider.resolve_model("model-a") == "model-b"
    assert mock_provider.resolve_model("model-c") == "model-c"