# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from typing import Generator

import groq

import navamai.configure as configure
from navamai.provider import Provider


class Groq(Provider):
    def __init__(self):
        super().__init__()
        self.client = groq.Groq()
        self.full_config = configure.load_config()

    def create_request_data(self, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "messages": [
                {"role": "system", "content": config["system"]},
                {"role": "user", "content": prompt},
            ],
        }

    def stream_vision_response(
        self, image_data: bytes, prompt: str
    ) -> Generator[str, None, None]:
        pass

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
