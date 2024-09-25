# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import base64
import os
from typing import Generator

from openai import OpenAI

import navamai.configure as configure
from navamai.provider import Provider


class Openai(Provider):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
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

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def create_vision_request_data(self, image_data: bytes, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "messages": [
                {"role": "system", "content": config["system"]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                },
            ],
        }

    def stream_vision_response(
        self, image_data: bytes, prompt: str, media_type: str
    ) -> Generator[str, None, None]:
        request_data = self.create_vision_request_data(image_data, prompt)
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def generate_image(self, prompt: str) -> str:
        config = self.model_config
        model = self.resolve_model(config["model"])

        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size=config.get("size", "1024x1024"),
            response_format="b64_json",
        )

        image_data = base64.b64decode(response.data[0].b64_json)
        return self.save_image_response(prompt, image_data)

    def save_image_response(self, prompt: str, image_data: bytes) -> str:
        responses_folder = self.model_config.get("save-folder", "image_responses")
        os.makedirs(responses_folder, exist_ok=True)

        words = [word.lower() for word in prompt.split()[:5]]
        filename = "-".join(words) + ".png"
        filepath = os.path.join(responses_folder, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        return filepath
