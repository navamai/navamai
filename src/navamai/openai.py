from openai import OpenAI
from typing import Generator
from navamai.provider import Provider
import navamai.utils as utils
import base64

class Openai(Provider):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.full_config = utils.load_config()
    
    def create_request_data(self, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "messages": [
                {
                    "role": "system",
                    "content": config["system"]
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
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
                {
                    "role": "system",
                    "content": config["system"]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
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
        for chunk in self.client.chat.completions.create(**request_data, stream=True):
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content