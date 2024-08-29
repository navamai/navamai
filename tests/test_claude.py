# test_claude.py

import pytest
from unittest.mock import patch, MagicMock
from navamai.claude import Claude
import anthropic

def test_claude_initialization():
    claude = Claude()
    assert isinstance(claude.client, anthropic.Anthropic)

def test_claude_set_model_config():
    claude = Claude()
    config = {
        "model": "sonnet",
        "provider": "claude",
        "max-tokens": 1000,
        "temperature": 0.3,
        "folder": "Embeds",
        "save": True,
        "system": "Only respond to the prompt using valid markdown syntax. When responding with markdown headings start at level 2. Do not explain your response."
    }
    claude.set_model_config("intents")
    assert claude.model_config == config

def test_claude_create_request_data():
    claude = Claude()
    claude.model_config = {
        "model": "sonnet",
        "provider": "claude",
        "max-tokens": 1000,
        "temperature": 0.3,
        "folder": "Embeds",
        "save": True,
        "system": "You are a helpful assistant."
    }

    request_data = claude.create_request_data("Hello, Claude!")

    assert request_data["model"] == "claude-3-5-sonnet-20240620"  # Assuming model mapping is applied
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.3
    assert request_data["system"] == "You are a helpful assistant."

def test_claude_create_request_data_with_model_mapping():
    claude = Claude()
    claude.model_config = {
        "model": "custom-model",
        "provider": "claude",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    claude.full_config = {"model-mapping": {"custom-model": "claude-3-opus-20240229"}}

    request_data = claude.create_request_data("Hello, Claude!")

    assert request_data["model"] == "claude-3-opus-20240229"

@patch("anthropic.Anthropic")
def test_claude_stream_response_error_handling(mock_anthropic):
    claude = Claude()
    claude.model_config = {
        "model": "sonnet",
        "provider": "claude",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }

    mock_anthropic.return_value.messages.stream.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        list(claude.stream_response("Hi"))

def test_claude_get_model_info():
    claude = Claude()
    claude.model_config = {"model": "sonnet"}
    assert claude.get_model_info() == "Claude - sonnet (mapped to claude-3-5-sonnet-20240620)"

def test_claude_resolve_model():
    claude = Claude()
    claude.full_config = {"model-mapping": {"sonnet": "claude-3-sonnet-20240229"}}
    assert claude.resolve_model("sonnet") == "claude-3-sonnet-20240229"
    assert claude.resolve_model("unknown-model") == "unknown-model"