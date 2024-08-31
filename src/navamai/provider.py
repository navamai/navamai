from abc import ABC, abstractmethod
from typing import Generator
import navamai.utils as utils
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
import os
import re

class Provider(ABC):
    def __init__(self):
        self.full_config = utils.load_config()
        self.model_config = self.full_config.get("ask-model-config", {})
        self.console = Console()

    @abstractmethod
    def create_request_data(self, prompt: str) -> dict:
        pass

    @abstractmethod
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        pass

    def set_model_config(self, model_config: str):
        self.model_config = self.full_config.get(model_config, {})
        pass
        
    def ask(self, prompt: str, title: str = None) -> str:
        with Live(console=self.console, refresh_per_second=8) as live:
            full_response = ""
            for chunk in self.stream_response(prompt):
                full_response += chunk
                formatted_response = f"{full_response}"
                live.update(Markdown(formatted_response))
        response_file_path = None
        if self.model_config.get("save", False):
            response_file_path = self.save_response(prompt, full_response, title)

        return response_file_path

    @abstractmethod
    def stream_vision_response(self, image_data: bytes, prompt: str) -> Generator[str, None, None]:
        pass

    def vision(self, image_data: bytes, prompt: str, title: str = None):
        full_response = ""
        for chunk in self.stream_vision_response(image_data, prompt):
            full_response += chunk
            yield chunk  # This yields chunks of the AI's response, not image_data

    def save_response(self, prompt: str, response: str, title: str = None) -> str:
        responses_folder = self.model_config.get('save-folder')
        os.makedirs(responses_folder, exist_ok=True)

        if title:
            # Use the title as the filename, ensuring it's safe for file systems
            filename = re.sub(r'[<>:"/\\|?*]', '', title) + ".md"
        else:
            # Create filename based on first ten words, ignoring words less than five characters
            words = [word.lower() for word in re.findall(r'\w+', response) if len(word) >= 5]
            filename = '-'.join(words[:10]) + ".md"

        filepath = os.path.join(responses_folder, filename)

        # Write the response, overwriting any existing file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response)

        self.console.print(f"Response saved to: {filepath}")
        return filepath

    def get_model_info(self) -> str:
        config = self.model_config
        model = config.get("model", "Unknown")
        model_mapping = self.full_config.get("model-mapping", {})
        if model in model_mapping:
            actual_model = model_mapping[model]
            return f"{self.__class__.__name__} - {model} (mapped to {actual_model})"
        return f"{self.__class__.__name__} - {model}"

    def resolve_model(self, model: str) -> str:
        model_mapping = self.full_config.get("model-mapping", {})
        return model_mapping.get(model, model)