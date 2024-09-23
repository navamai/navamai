import base64
from typing import Generator, Dict, Any, List

import anthropic

import navamai.configure as configure
from navamai.provider import Provider


class Claude(Provider):
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic()
        self.full_config = configure.load_config()

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "model": self.resolve_model(config["model"]),
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "system": config["system"],
        }

    def _create_message_content(self, prompt: str, image_data: bytes = None, media_type: str = None) -> List[Dict[str, Any]]:
        content = []
        if image_data:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64.b64encode(image_data).decode("utf-8"),
                },
            })
        content.append({"type": "text", "text": prompt})
        return content

    def create_request_data(self, prompt: str, image_data: bytes = None, media_type: str = None) -> Dict[str, Any]:
        request_data = self._create_base_request_data()
        request_data["messages"] = [{"role": "user", "content": self._create_message_content(prompt, image_data, media_type)}]
        return request_data

    def _stream_response(self, request_data: Dict[str, Any]) -> Generator[str, None, None]:
        with self.client.messages.stream(**request_data) as stream:
            yield from stream.text_stream

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: str = None) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt, image_data, media_type)
        yield from self._stream_response(request_data)