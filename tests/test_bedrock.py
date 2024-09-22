import pytest
from unittest.mock import patch, MagicMock
import json
import base64
from navamai.bedrock import Bedrock

@pytest.fixture
def bedrock_instance():
    with patch('boto3.client'):
        instance = Bedrock()
        instance.model_config = {
            "model": "test-model",
            "max-tokens": 100,
            "system": "test system",
            "temperature": 0.7
        }
        return instance

def test_init(bedrock_instance):
    assert isinstance(bedrock_instance.client, MagicMock)

def test_create_request_data(bedrock_instance):
    bedrock_instance.model_config = {
        "model": "test-model",
        "max-tokens": 100,
        "system": "test system",
        "temperature": 0.7
    }
    request_data = bedrock_instance.create_request_data("Test prompt")
    
    assert request_data["modelId"] == "test-model"
    assert request_data["contentType"] == "application/json"
    assert request_data["accept"] == "application/json"
    
    body = json.loads(request_data["body"].decode("utf-8"))
    assert body["anthropic_version"] == "bedrock-2023-05-31"
    assert body["max_tokens"] == 100
    assert body["system"] == "test system"
    assert body["messages"] == [{"role": "user", "content": "Test prompt"}]
    assert body["temperature"] == 0.7

def test_stream_response(bedrock_instance):
    mock_response = {
        "body": [
            {"chunk": {"bytes": json.dumps({"delta": {"text": "Test"}}).encode()}},
            {"chunk": {"bytes": json.dumps({"delta": {"text": " response"}}).encode()}}
        ]
    }
    bedrock_instance.client.invoke_model_with_response_stream.return_value = mock_response
    
    response = list(bedrock_instance.stream_response("Test prompt"))
    assert response == ["Test", " response"]

def test_create_vision_request_data(bedrock_instance):
    bedrock_instance.model_config = {
        "model": "test-model",
        "max-tokens": 100,
        "temperature": 0.7
    }
    image_data = b"fake_image_data"
    request_data = bedrock_instance.create_vision_request_data(image_data, "Describe this image")
    
    body = json.loads(request_data["body"].decode("utf-8"))
    assert body["anthropic_version"] == "bedrock-2023-05-31"
    assert body["max_tokens"] == 100
    assert body["temperature"] == 0.7
    assert len(body["messages"]) == 1
    assert body["messages"][0]["role"] == "user"
    assert len(body["messages"][0]["content"]) == 2
    assert body["messages"][0]["content"][0]["type"] == "image"
    assert body["messages"][0]["content"][0]["source"]["type"] == "base64"
    assert body["messages"][0]["content"][0]["source"]["media_type"] == "image/jpeg"
    assert body["messages"][0]["content"][0]["source"]["data"] == base64.b64encode(image_data).decode("utf-8")
    assert body["messages"][0]["content"][1]["type"] == "text"
    assert body["messages"][0]["content"][1]["text"] == "Describe this image"

def test_stream_vision_response(bedrock_instance):
    mock_response = {
        "body": [
            {"chunk": {"bytes": json.dumps({"delta": {"text": "This image"}}).encode()}},
            {"chunk": {"bytes": json.dumps({"delta": {"text": " shows"}}).encode()}}
        ]
    }
    bedrock_instance.client.invoke_model_with_response_stream.return_value = mock_response
    
    response = list(bedrock_instance.stream_vision_response(b"fake_image_data", "Describe this image"))
    assert response == ["This image", " shows"]