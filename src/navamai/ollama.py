import requests
import json
from typing import Generator
from navamai.provider import Provider
import navamai.utils as utils

class Ollama(Provider):
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:11434"
        self.full_config = utils.load_config()
    
    def create_request_data(self, prompt: str) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        return {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "system": config["system"],
            "options": {
                "num_predict": config["max-tokens"],
                "temperature": config["temperature"]
            }
        }

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = self.create_request_data(prompt)

        with requests.post(url, headers=headers, data=json.dumps(data), stream=True) as response:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield chunk['response']
                    if chunk.get('done', False):
                        break