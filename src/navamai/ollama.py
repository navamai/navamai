import base64
import json
from typing import Generator

import requests

import navamai.configure as configure
from navamai.provider import Provider

from rich.console import Console

console = Console()

class Ollama(Provider):
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:11434"
        self.full_config = configure.load_config()

    def create_request_data(self, prompt: str, image_data: bytes = None) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        request_data = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "system": config["system"],
            "options": {
                "num_predict": config["max-tokens"],
                "temperature": config["temperature"],
            },
        }

        if image_data:
            request_data["images"] = [base64.b64encode(image_data).decode("utf-8")]

        return request_data

    def stream_response(
        self, prompt: str, image_data: bytes = None, media_type: str = None
    ) -> Generator[str, None, None]:
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = self.create_request_data(prompt, image_data)

        with requests.post(
            url, headers=headers, data=json.dumps(data), stream=True
        ) as response:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
                    if chunk.get("done", False):
                        break

    def stream_vision_response(
        self, image_data: bytes, prompt: str, media_type: str
    ) -> Generator[str, None, None]:
        # [TODO] Handle this error gracefully. Not sure returning an empty list is the best way to handle this.
        if media_type == "image/webp":
            console.print("WebP images are not supported by Ollama Llava", style="red")
            return []
        else:
            return self.stream_response(prompt, image_data, media_type)
