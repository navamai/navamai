from navamai.claude import Claude
from navamai.ollama import Ollama
from navamai.groq import Groq
from navamai.openai import Openai
from navamai.gemini import Gemini

def get_provider_instance(provider):
    if provider == "claude":
        return Claude()
    elif provider == "ollama":
        return Ollama()
    elif provider == "groq":
        return Groq()
    elif provider == "openai":
        return Openai()
    elif provider == "gemini":
        return Gemini()
    else:
        raise ValueError(f"Unsupported provider: {provider}")

