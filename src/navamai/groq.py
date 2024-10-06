# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from typing import Any, Dict, Generator, List

import groq

import navamai.configure as configure
from navamai.provider import Provider


class Groq(Provider):
    def __init__(self):
        super().__init__()
        self.client = groq.Groq()
        self.full_config = configure.load_config()

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "model": self.resolve_model(config["model"]),
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
        }

    def _create_message_content(
        self, prompt: str, image_data: bytes = None, media_type: str = None
    ) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": self.model_config["system"]},
            {"role": "user", "content": prompt},
        ]
        # Note: Groq doesn't support image input as of now, but we'll keep the
        # structure similar to other providers for consistency and future-proofing
        return messages

    def create_request_data(
        self, prompt: str, image_data: bytes = None, media_type: str = None
    ) -> Dict[str, Any]:
        request_data = self._create_base_request_data()
        request_data["messages"] = self._create_message_content(prompt, image_data, media_type)
        return request_data

    def _stream_response(
        self, request_data: Dict[str, Any]
    ) -> Generator[str, None, None]:
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(
        self, image_data: bytes, prompt: str, media_type: str
    ) -> Generator[str, None, None]:
        # As of now, Groq doesn't support image input, so we'll raise a NotImplementedError
        raise NotImplementedError("Groq does not currently support vision-based responses.")