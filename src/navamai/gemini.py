import google.generativeai as genai
from typing import Generator
from navamai.provider import Provider
import navamai.utils as utils
import os
import io
from PIL import Image

class Gemini(Provider):
    def __init__(self):
        super().__init__()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.full_config = utils.load_config()
    
    def create_request_data(self, prompt: str, image_data: bytes = None) -> dict:
        config = self.model_config
        model = self.resolve_model(config["model"])
        
        contents = []
        
        if image_data:
            image = Image.open(io.BytesIO(image_data))
            contents.append({
                "mime_type": "image/jpeg",
                "data": image_data
            })
        
        contents.append(config["system"] + "\n\n" + prompt)
        
        return {
            "model": model,
            "max_output_tokens": config["max-tokens"],
            "temperature": config["temperature"],
            "contents": contents
        }

    def stream_response(self, prompt: str, image_data: bytes = None) -> Generator[str, None, None]:
        request_data = self.create_request_data(prompt, image_data)
        model = genai.GenerativeModel(request_data["model"])
        response = model.generate_content(
            request_data["contents"],
            stream=True,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=request_data["max_output_tokens"],
                temperature=request_data["temperature"]
            )
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    def stream_vision_response(self, image_data: bytes, prompt: str) -> Generator[str, None, None]:
        return self.stream_response(prompt, image_data)