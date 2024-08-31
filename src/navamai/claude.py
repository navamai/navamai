import anthropic
from typing import Generator
from navamai.provider import Provider
import navamai.utils as utils
import base64

class Claude(Provider):
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic()
        self.full_config = utils.load_config()
    
    def create_request_data(self, prompt: str) -> dict:
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
                    "content": [{"type": "text", "text": prompt}]
                }
            ]
        }

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        with self.client.messages.stream(**request_data) as stream:
            for text in stream.text_stream:
                yield text


    def create_vision_request_data(self, image_data: bytes, prompt: str) -> dict:
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
                                "media_type": "image/jpeg",
                                "data": base64.b64encode(image_data).decode('utf-8')
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }

    def stream_vision_response(self, image_data: bytes, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_vision_request_data(image_data, prompt)
        with self.client.messages.stream(**request_data) as stream:
            for text in stream.text_stream:
                yield text