# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import base64
import os
from typing import Any, Dict, Generator, List

from openai import OpenAI

from navamai.provider import Provider

class Openai(Provider):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "model": self.resolve_model(config["model"]),
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
        }

    def _create_message_content(self, prompt: str, image_data: bytes = None) -> List[Dict[str, Any]]:
        content = [{"role": "system", "content": self.model_config["system"]}]
        if image_data:
            content.append({
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
                        },
                    },
                    {"type": "text", "text": prompt},
                ]
            })
        else:
            content.append({"role": "user", "content": prompt})
        return content

    def create_request_data(self, prompt: str, image_data: bytes = None) -> Dict[str, Any]:
        request_data = self._create_base_request_data()
        request_data["messages"] = self._create_message_content(prompt, image_data)
        return request_data

    def _stream_response(self, request_data: Dict[str, Any]) -> Generator[str, None, None]:
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt, image_data)
        yield from self._stream_response(request_data)

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