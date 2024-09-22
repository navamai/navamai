import pytest
from unittest.mock import patch
import base64
from navamai.claude import Claude

@pytest.fixture
def claude_instance():
    with patch('anthropic.Anthropic'):
        yield Claude()

def test_init(claude_instance):
    assert isinstance(claude_instance, Claude)
    assert hasattr(claude_instance, 'client')
    assert hasattr(claude_instance, 'full_config')

def test_create_request_data(claude_instance):
    claude_instance.model_config = {
        "model": "claude-3-sonnet-20240229",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    prompt = "Hello, Claude!"
    request_data = claude_instance.create_request_data(prompt)
    
    assert request_data["model"] == "claude-3-sonnet-20240229"
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert request_data["system"] == "You are a helpful assistant."
    assert request_data["messages"] == [{"role": "user", "content": [{"type": "text", "text": "Hello, Claude!"}]}]

def test_create_vision_request_data(claude_instance):
    claude_instance.model_config = {
        "model": "claude-3-sonnet-20240229",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    image_data = b"fake_image_data"
    prompt = "Describe this image"
    media_type = "image/jpeg"
    
    request_data = claude_instance.create_vision_request_data(image_data, prompt, media_type)
    
    assert request_data["model"] == "claude-3-sonnet-20240229"
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert request_data["system"] == "You are a helpful assistant."
    assert len(request_data["messages"]) == 1
    assert request_data["messages"][0]["role"] == "user"
    assert len(request_data["messages"][0]["content"]) == 2
    assert request_data["messages"][0]["content"][0]["type"] == "image"
    assert request_data["messages"][0]["content"][0]["source"]["type"] == "base64"
    assert request_data["messages"][0]["content"][0]["source"]["media_type"] == "image/jpeg"
    assert request_data["messages"][0]["content"][0]["source"]["data"] == base64.b64encode(image_data).decode("utf-8")
    assert request_data["messages"][0]["content"][1] == {"type": "text", "text": "Describe this image"}

def test_resolve_model(claude_instance):
    assert claude_instance.resolve_model("claude-3-5-sonnet-20240620") == "claude-3-5-sonnet-20240620"
    assert claude_instance.resolve_model("sonnet") == "sonnet"