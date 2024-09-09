import base64
from typing import Generator

import anthropic

import navamai.configure as configure
from navamai.provider import Provider


class Claude(Provider):
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic()
        self.full_config = configure.load_config()

    def create_request_data(self, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "system": config["system"],
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
        }

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        with self.client.messages.stream(**request_data) as stream:
            for text in stream.text_stream:
                yield text

    def create_vision_request_data(self, image_data: bytes, prompt: str, media_type: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "system": config["system"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64.b64encode(image_data).decode("utf-8"),
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        }

    def stream_vision_response(
        self, image_data: bytes, prompt: str, media_type: str = None
    ) -> Generator[str, None, None]:
        request_data = self.create_vision_request_data(image_data, prompt, media_type)
        with self.client.messages.stream(**request_data) as stream:
            for text in stream.text_stream:
                yield text
