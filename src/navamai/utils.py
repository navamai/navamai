from navamai.claude import Claude
from navamai.ollama import Ollama
from navamai.groq import Groq
from navamai.openai import Openai
from navamai.gemini import Gemini

import functools
import yaml
from datetime import datetime
import os

def trail(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Get the command name
        command_name = f.__name__

        # Get the full command with arguments
        full_command = f"{command_name} {' '.join(str(arg) for arg in args)}"
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    full_command += f" --{key}"
            else:
                full_command += f" --{key}={value}"

        # Prepare the log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'command': full_command,
            'source_file': None,
            'destination_file': None
        }

        # Execute the wrapped function
        result = f(*args, **kwargs)

        # Handle the result
        if isinstance(result, dict):
            if 'source_file' in result:
                log_entry['source_file'] = result['source_file']
            if 'destination_file' in result:
                log_entry['destination_file'] = result['destination_file']
        elif isinstance(result, str) and os.path.exists(result):
            log_entry['destination_file'] = result

        # Append to the YAML file
        with open('trail.yml', 'a') as log_file:
            yaml.dump([log_entry], log_file, default_flow_style=False)

        return result

    return wrapper


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

