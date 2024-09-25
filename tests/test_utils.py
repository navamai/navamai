# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os
import sys
from datetime import datetime
from unittest.mock import ANY, MagicMock, mock_open, patch

import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from navamai.bedrock import Bedrock
from navamai.claude import Claude
from navamai.gemini import Gemini
from navamai.groq import Groq
from navamai.ollama import Ollama
from navamai.openai import Openai
from navamai.perplexity import Perplexity
from navamai.utils import get_provider_instance, trail


# Test the trail decorator
def test_trail_decorator():
    @trail
    def sample_function(arg1, arg2, kwarg1=None, flag=False):
        return {
            "prompt_file": "prompt.txt",
            "custom_prompt": "Custom prompt",
            "source_file": "source.txt",
            "destination_file": "dest.txt",
        }

    mock_datetime = MagicMock(wraps=datetime)
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

    with patch("navamai.utils.datetime", mock_datetime), patch(
        "navamai.utils.open", mock_open()
    ) as mock_file, patch("yaml.dump") as mock_yaml_dump:

        result = sample_function("value1", "value2", kwarg1="test", flag=True)

        # Check if the function returns the expected result
        assert result == {
            "prompt_file": "prompt.txt",
            "custom_prompt": "Custom prompt",
            "source_file": "source.txt",
            "destination_file": "dest.txt",
        }

        # Check if the log file was opened
        mock_file.assert_called_once_with("trail.yml", "a")

        # Check if yaml.dump was called with the correct log entry
        expected_log_entry = [
            {
                "timestamp": "2024-01-01T12:00:00",
                "command": "sample_function value1 value2 --kwarg1=test --flag",
                "custom_prompt": "Custom prompt",
                "prompt_file": "prompt.txt",
                "source_file": "source.txt",
                "destination_file": "dest.txt",
            }
        ]
        mock_yaml_dump.assert_called_once_with(
            expected_log_entry, mock_file(), default_flow_style=False
        )


def test_trail_decorator_with_string_result():
    @trail
    def sample_function_string():
        return "output.txt"

    with patch("navamai.utils.open", mock_open()) as mock_file, patch(
        "yaml.dump"
    ) as mock_yaml_dump, patch("os.path.exists", return_value=True):

        result = sample_function_string()

        assert result == "output.txt"

        # Check if yaml.dump was called
        mock_yaml_dump.assert_called_once()

        # Get the actual call arguments
        actual_call = mock_yaml_dump.call_args

        # Check the structure of the log entry
        assert len(actual_call[0]) == 2  # Two positional arguments
        assert isinstance(actual_call[0][0], list)  # First arg is a list
        assert len(actual_call[0][0]) == 1  # List contains one dictionary
        log_entry = actual_call[0][0][0]

        # Check each key in the log entry
        assert "timestamp" in log_entry
        assert isinstance(log_entry["timestamp"], str)  # Timestamp should be a string
        assert (
            log_entry["command"] == "sample_function_string "
        )  # Note the trailing space
        assert log_entry["custom_prompt"] is None
        assert log_entry["prompt_file"] is None
        assert log_entry["source_file"] is None
        assert log_entry["destination_file"] == "output.txt"

        # Check the second positional argument (file object)
        assert actual_call[0][1] == mock_file()

        # Check keyword arguments
        assert actual_call[1] == {"default_flow_style": False}


# Test the get_provider_instance function
@pytest.mark.parametrize(
    "provider,expected_class",
    [
        ("claude", Claude),
        ("ollama", Ollama),
        ("groq", Groq),
        ("openai", Openai),
        ("gemini", Gemini),
        ("bedrock", Bedrock),
        ("perplexity", Perplexity),
    ],
)
def test_get_provider_instance(provider, expected_class):
    instance = get_provider_instance(provider)
    assert isinstance(instance, expected_class)


def test_get_provider_instance_invalid():
    with pytest.raises(ValueError, match="Unsupported provider: invalid_provider"):
        get_provider_instance("invalid_provider")


# Run the tests
if __name__ == "__main__":
    pytest.main()
