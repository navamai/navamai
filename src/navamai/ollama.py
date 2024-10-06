# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import base64
import json
from typing import Any, Dict, Generator

import requests
from rich.console import Console

from navamai.provider import Provider

console = Console()

class Ollama(Provider):
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:11434"

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "model": self.resolve_model(config["model"]),
            "stream": True,
            "system": config["system"],
            "options": {
                "num_predict": config["max-tokens"],
                "temperature": config["temperature"],
            },
        }

    def create_request_data(self, prompt: str, image_data: bytes = None) -> Dict[str, Any]:
        request_data = self._create_base_request_data()
        request_data["prompt"] = prompt
        if image_data:
            request_data["images"] = [base64.b64encode(image_data).decode("utf-8")]
        return request_data

    def _stream_response(self, request_data: Dict[str, Any]) -> Generator[str, None, None]:
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        
        with requests.post(url, headers=headers, data=json.dumps(request_data), stream=True) as response:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
                    if chunk.get("done", False):
                        break

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str) -> Generator[str, None, None]:
        if media_type == "image/webp":
            console.print("WebP images are not supported by Ollama Llava", style="red")
            return
        request_data = self.create_request_data(prompt, image_data)
        yield from self._stream_response(request_data)