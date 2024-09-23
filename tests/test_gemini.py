# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license. 
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import pytest
from unittest.mock import patch, MagicMock
from navamai.gemini import Gemini

@pytest.fixture
def gemini_instance():
    with patch('google.generativeai.configure'), \
         patch('os.environ.get', return_value='fake_api_key'):
        yield Gemini()

def test_init(gemini_instance):
    assert isinstance(gemini_instance, Gemini)
    assert hasattr(gemini_instance, 'full_config')

def test_init_no_api_key():
    with patch('os.environ.get', return_value=None), \
         pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
        Gemini()

def test_create_request_data(gemini_instance):
    gemini_instance.model_config = {
        "model": "gemini-pro",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    prompt = "Hello, Gemini!"
    request_data = gemini_instance.create_request_data(prompt)
    
    assert request_data["model"] == "gemini-pro"
    assert request_data["max_output_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert request_data["contents"] == ["You are a helpful assistant.\n\nHello, Gemini!"]

def test_create_request_data_with_image(gemini_instance):
    gemini_instance.model_config = {
        "model": "gemini-pro-vision",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    image_data = b"fake_image_data"
    prompt = "Describe this image"
    media_type = "image/jpeg"
    
    request_data = gemini_instance.create_request_data(prompt, image_data, media_type)
    
    assert request_data["model"] == "gemini-pro-vision"
    assert request_data["max_output_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert len(request_data["contents"]) == 2
    assert request_data["contents"][0] == {"mime_type": "image/jpeg", "data": b"fake_image_data"}
    assert request_data["contents"][1] == "You are a helpful assistant.\n\nDescribe this image"

@pytest.mark.asyncio
async def test_stream_response(gemini_instance):
    gemini_instance.model_config = {
        "model": "gemini-pro",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Hello, human!"
    mock_model.generate_content.return_value = [mock_response]
    
    with patch('google.generativeai.GenerativeModel', return_value=mock_model):
        response = gemini_instance.stream_response("Hello, Gemini!")
        result = list(response)
        
        assert result == ["Hello, human!"]
        mock_model.generate_content.assert_called_once()

@pytest.mark.asyncio
async def test_stream_vision_response(gemini_instance):
    gemini_instance.model_config = {
        "model": "gemini-pro-vision",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant."
    }
    
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "I see an image."
    mock_model.generate_content.return_value = [mock_response]
    
    with patch('google.generativeai.GenerativeModel', return_value=mock_model):
        response = gemini_instance.stream_vision_response(b"fake_image_data", "Describe this image", "image/jpeg")
        result = list(response)
        
        assert result == ["I see an image."]
        mock_model.generate_content.assert_called_once()

def test_resolve_model(gemini_instance):
    assert gemini_instance.resolve_model("gemini-pro") == "gemini-pro"
    assert gemini_instance.resolve_model("gemini-pro-vision") == "gemini-pro-vision"