# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import json
import os
from typing import Any, Dict, Generator

import requests

import navamai.configure as configure
from navamai.provider import Provider


class Perplexity(Provider):
    def __init__(self):
        super().__init__()
        self.url = "https://api.perplexity.ai/chat/completions"
        self.full_config = configure.load_config()
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('PERPLEXITY_KEY')}",
            "Content-Type": "application/json",
        }

    def create_request_data(self, prompt: str) -> Dict[str, Any]:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "messages": [
                {"role": "system", "content": config["system"]},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "top_p": 0.9,
            "return_citations": True,
            "search_domain_filter": ["perplexity.ai"],
            "return_images": False,
            "return_related_questions": False,
            "search_recency_filter": "month",
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1,
        }

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        request_data["stream"] = True

        response = requests.post(
            self.url, json=request_data, headers=self.headers, stream=True
        )

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        for line in response.iter_lines():
            if line:
                try:
                    json_object = json.loads(line.decode("utf-8").split("data: ")[1])
                    if "choices" in json_object and len(json_object["choices"]) > 0:
                        content = (
                            json_object["choices"][0].get("delta", {}).get("content")
                        )
                        if content:
                            yield content
                except json.JSONDecodeError:
                    continue

    def create_vision_request_data(
        self, image_data: bytes, prompt: str
    ) -> Dict[str, Any]:
        # Note: As of now, there's no information about Perplexity's vision API.
        # This method may need to be adjusted when such functionality becomes available.
        raise NotImplementedError(
            "Vision API is not currently supported by Perplexity."
        )

    def stream_vision_response(
        self, image_data: bytes, prompt: str
    ) -> Generator[str, None, None]:
        # Note: As of now, there's no information about Perplexity's vision API.
        # This method may need to be adjusted when such functionality becomes available.
        raise NotImplementedError(
            "Vision API is not currently supported by Perplexity."
        )
