import os
import re
from abc import ABC, abstractmethod
from typing import Generator, Optional

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

import navamai.configure as configure

class Provider(ABC):
    def __init__(self):
        self.full_config = configure.load_config()
        self.model_config = self.full_config.get("ask-model-config", {})
        self.console = Console()

    @abstractmethod
    def create_request_data(self, prompt: str) -> dict:
        pass

    @abstractmethod
    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def stream_vision_response(self, image_data: bytes, prompt: str, media_type: Optional[str] = None) -> Generator[str, None, None]:
        pass

    def set_model_config(self, model_config: str):
        self.model_config = self.full_config.get(model_config, {})

    def ask(self, prompt: str, title: Optional[str] = None) -> Optional[str]:
        full_response = ""
        terminal_height = self.console.height

        with Live(console=self.console, refresh_per_second=16, auto_refresh=False) as live:
            for chunk in self.stream_response(prompt):
                full_response += chunk
                lines = full_response.split("\n")[-(terminal_height - 2):]
                live.update(Markdown("\n".join(lines)), refresh=True)

        self.console.print()

        return self.save_response(prompt, full_response, title) if self.model_config.get("save", False) else None

    def vision(self, image_data: bytes, prompt: str, title: Optional[str] = None):
        yield from self.stream_vision_response(image_data, prompt)

    def save_response(self, prompt: str, response: str, title: Optional[str] = None) -> str:
        responses_folder = self.model_config.get("save-folder", "responses")
        os.makedirs(responses_folder, exist_ok=True)

        if title:
            filename = re.sub(r'[<>:"/\\|?*]', "", title) + ".md"
        else:
            words = [word.lower() for word in re.findall(r"\w+", response) if len(word) >= 5]
            filename = "-".join(words[:5]) + ".md"

        filepath = os.path.join(responses_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response)

        self.console.print(f"Response saved to: {filepath}")
        return filepath

    def get_model_info(self) -> str:
        model = self.model_config.get("model", "Unknown")
        model_mapping = self.full_config.get("model-mapping", {})
        actual_model = model_mapping.get(model, model)
        return f"{self.__class__.__name__} - {model}" + (f" (mapped to {actual_model})" if model != actual_model else "")

    def resolve_model(self, model: str) -> str:
        return self.full_config.get("model-mapping", {}).get(model, model)