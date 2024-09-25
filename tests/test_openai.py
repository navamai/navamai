# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from unittest.mock import MagicMock, patch

import pytest

from navamai.openai import Openai


@pytest.fixture
def openai_instance():
    with patch("openai.OpenAI"):
        yield Openai()


def test_init(openai_instance):
    assert isinstance(openai_instance, Openai)
    assert hasattr(openai_instance, "client")
    assert hasattr(openai_instance, "full_config")


def test_create_request_data(openai_instance):
    openai_instance.model_config = {
        "model": "gpt-4",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
    }

    prompt = "Hello, OpenAI!"
    request_data = openai_instance.create_request_data(prompt)

    assert request_data["model"] == "gpt-4"
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert request_data["messages"] == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, OpenAI!"},
    ]


@pytest.mark.asyncio
async def test_stream_response(openai_instance):
    openai_instance.model_config = {
        "model": "gpt-4",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
    }

    mock_chunk1 = MagicMock()
    mock_chunk1.choices = [MagicMock(delta=MagicMock(content="Hello"))]
    mock_chunk2 = MagicMock()
    mock_chunk2.choices = [MagicMock(delta=MagicMock(content=", human!"))]
    mock_chunk3 = MagicMock()
    mock_chunk3.choices = [MagicMock(delta=MagicMock(content=None))]

    mock_create = MagicMock(return_value=[mock_chunk1, mock_chunk2, mock_chunk3])
    openai_instance.client.chat.completions.create = mock_create

    response = openai_instance.stream_response("Hello, OpenAI!")
    result = list(response)

    assert result == ["Hello", ", human!"]
    mock_create.assert_called_once_with(
        model="gpt-4",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, OpenAI!"},
        ],
        stream=True,
    )


def test_create_vision_request_data(openai_instance):
    openai_instance.model_config = {
        "model": "gpt-4-vision-preview",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
    }

    prompt = "Describe this image"
    image_data = b"fake_image_data"
    request_data = openai_instance.create_vision_request_data(image_data, prompt)

    assert request_data["model"] == "gpt-4-vision-preview"
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert len(request_data["messages"]) == 2
    assert request_data["messages"][1]["content"][0]["type"] == "image_url"
    assert request_data["messages"][1]["content"][1]["type"] == "text"
    assert request_data["messages"][1]["content"][1]["text"] == "Describe this image"


@pytest.mark.asyncio
async def test_stream_vision_response(openai_instance):
    openai_instance.model_config = {
        "model": "gpt-4-vision-preview",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
    }

    mock_chunk1 = MagicMock()
    mock_chunk1.choices = [MagicMock(delta=MagicMock(content="The image shows"))]
    mock_chunk2 = MagicMock()
    mock_chunk2.choices = [MagicMock(delta=MagicMock(content=" a cat."))]
    mock_chunk3 = MagicMock()
    mock_chunk3.choices = [MagicMock(delta=MagicMock(content=None))]

    mock_create = MagicMock(return_value=[mock_chunk1, mock_chunk2, mock_chunk3])
    openai_instance.client.chat.completions.create = mock_create

    response = openai_instance.stream_vision_response(
        b"fake_image_data", "Describe this image", "image/jpeg"
    )
    result = list(response)

    assert result == ["The image shows", " a cat."]


def test_resolve_model(openai_instance):
    assert openai_instance.resolve_model("gpt-4") == "gpt-4"
    assert (
        openai_instance.resolve_model("gpt-4-vision-preview") == "gpt-4-vision-preview"
    )
