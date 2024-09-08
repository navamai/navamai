import base64
import json
from typing import Generator

import boto3

from navamai.provider import Provider


class Bedrock(Provider):
    def __init__(self):
        super().__init__()
        self.client = boto3.client("bedrock-runtime")

    def create_request_data(self, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": config["max-tokens"],
            "system": config["system"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config["temperature"],
        }
        return {
            "modelId": model,
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps(body).encode("utf-8"),
        }

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        response = self.client.invoke_model_with_response_stream(**request_data)
        for event in response.get("body", []):
            if "chunk" in event:
                chunk = json.loads(event["chunk"]["bytes"].decode("utf-8"))
                if "delta" in chunk and "text" in chunk["delta"]:
                    yield chunk["delta"]["text"]

    def create_vision_request_data(self, image_data: bytes, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": config["max-tokens"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64.b64encode(image_data).decode("utf-8"),
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            "temperature": config["temperature"],
        }
        return {
            "modelId": model,
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps(body).encode("utf-8"),
        }

    def stream_vision_response(
        self, image_data: bytes, prompt: str
    ) -> Generator[str, None, None]:
        request_data = self.create_vision_request_data(image_data, prompt)
        response = self.client.invoke_model_with_response_stream(**request_data)
        for event in response.get("body", []):
            if "chunk" in event:
                chunk = json.loads(event["chunk"]["bytes"].decode("utf-8"))
                if "delta" in chunk and "text" in chunk["delta"]:
                    yield chunk["delta"]["text"]
