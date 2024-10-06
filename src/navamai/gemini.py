# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os
from typing import Any, Dict, Generator, List

import google.generativeai as genai

import navamai.configure as configure
from navamai.provider import Provider


class Gemini(Provider):
    def __init__(self):
        super().__init__()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.full_config = configure.load_config()

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "model": self.resolve_model(config["model"]),
            "max_output_tokens": config["max-tokens"],
            "temperature": config["temperature"],
        }

    def _create_message_content(
        self, prompt: str, image_data: bytes = None, media_type: str = None
    ) -> List[Any]:
        contents = []
        if image_data:
            contents.append({"mime_type": media_type, "data": image_data})
        contents.append(self.model_config["system"] + "\n\n" + prompt)
        return contents

    def create_request_data(
        self, prompt: str, image_data: bytes = None, media_type: str = None
    ) -> Dict[str, Any]:
        request_data = self._create_base_request_data()
        request_data["contents"] = self._create_message_content(prompt, image_data, media_type)
        return request_data

    def _stream_response(
        self, request_data: Dict[str, Any]
    ) -> Generator[str, None, None]:
        model = genai.GenerativeModel(request_data["model"])
        response = model.generate_content(
            request_data["contents"],
            stream=True,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request_data["max_output_tokens"],
                temperature=request_data["temperature"],
            ),
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(
        self, image_data: bytes, prompt: str, media_type: str
    ) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt, image_data, media_type)
        yield from self._stream_response(request_data)