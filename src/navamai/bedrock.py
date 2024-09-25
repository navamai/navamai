# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import base64
import json
from typing import Any, Dict, Generator, List, Union

import boto3

from navamai.provider import Provider


class Bedrock(Provider):
    def __init__(self):
        super().__init__()
        self.client = boto3.client("bedrock-runtime")

    def _create_base_request_data(self) -> Dict[str, Any]:
        config = self.model_config
        return {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "system": config.get("system", ""),
        }

    def _create_message_content(
        self, prompt: str, image_data: bytes = None
    ) -> Union[str, List[Dict[str, Any]]]:
        if image_data:
            return [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64.b64encode(image_data).decode("utf-8"),
                    },
                },
                {"type": "text", "text": prompt},
            ]
        return prompt

    def create_request_data(
        self, prompt: str, image_data: bytes = None
    ) -> Dict[str, Any]:
        config = self.model_config
        model = self.resolve_model(config["model"])
        body = self._create_base_request_data()
        body["messages"] = [
            {
                "role": "user",
                "content": self._create_message_content(prompt, image_data),
            }
        ]

        return {
            "modelId": model,
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps(body).encode("utf-8"),
        }

    def _stream_response(
        self, request_data: Dict[str, Any]
    ) -> Generator[str, None, None]:
        response = self.client.invoke_model_with_response_stream(**request_data)
        for event in response.get("body", []):
            if "chunk" in event:
                chunk = json.loads(event["chunk"]["bytes"].decode("utf-8"))
                if "delta" in chunk and "text" in chunk["delta"]:
                    yield chunk["delta"]["text"]

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt)
        yield from self._stream_response(request_data)

    def stream_vision_response(
        self, image_data: bytes, prompt: str
    ) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt, image_data)
        yield from self._stream_response(request_data)
