# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from unittest.mock import MagicMock, patch

import pytest

from navamai.groq import Groq


@pytest.fixture
def groq_instance():
    with patch("groq.Groq"):
        yield Groq()


def test_init(groq_instance):
    assert isinstance(groq_instance, Groq)
    assert hasattr(groq_instance, "client")
    assert hasattr(groq_instance, "full_config")


def test_create_request_data(groq_instance):
    groq_instance.model_config = {
        "model": "mixtral-8x7b-32768",
        "max-tokens": 1000,
        "temperature": 0.7,
        "system": "You are a helpful assistant.",
    }

    prompt = "Hello, Groq!"
    request_data = groq_instance.create_request_data(prompt)

    assert request_data["model"] == "mixtral-8x7b-32768"
    assert request_data["max_tokens"] == 1000
    assert request_data["temperature"] == 0.7
    assert request_data["messages"] == [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Groq!"},
    ]



@pytest.mark.asyncio
async def test_stream_response(groq_instance):
    groq_instance.model_config = {
        "model": "mixtral-8x7b-32768",
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
    groq_instance.client.chat.completions.create = mock_create

    response = groq_instance.stream_response("Hello, Groq!")
    result = list(response)

    assert result == ["Hello", ", human!"]
    mock_create.assert_called_once_with(
        model="mixtral-8x7b-32768",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, Groq!"},
        ],
        stream=True,
    )


def test_resolve_model(groq_instance):
    assert groq_instance.resolve_model("mixtral-8x7b-32768") == "mixtral-8x7b-32768"
    assert groq_instance.resolve_model("llama2-70b-4096") == "llama2-70b-4096"
