# test_utils.py

import pytest
from unittest.mock import patch, mock_open
from navamai import utils

def test_load_config():
    mock_config = """
    ask:
      provider: claude
    model-mapping:
      gpt-3.5-turbo: gpt-3.5-turbo-0613
    """
    with patch("builtins.open", mock_open(read_data=mock_config)):
        config = utils.load_config()
        assert config["ask"]["provider"] == "claude"
        assert config["model-mapping"]["gpt-3.5-turbo"] == "gpt-3.5-turbo-0613"

def test_load_config_section():
    mock_config = """
    ask:
      provider: claude
    model-mapping:
      gpt-3.5-turbo: gpt-3.5-turbo-0613
    """
    with patch("builtins.open", mock_open(read_data=mock_config)):
        ask_config = utils.load_config("ask")
        assert ask_config["provider"] == "claude"

def test_edit_config():
    mock_config = {"ask": {"provider": "claude"}}
    with patch("navamai.utils.load_config", return_value=mock_config):
        with patch("navamai.utils.save_config") as mock_save:
            utils.edit_config(["ask", "provider"], "openai")
            mock_save.assert_called_once_with({"ask": {"provider": "openai"}})

def test_resolve_model():
    mock_mapping = {"gpt-3.5-turbo": "gpt-3.5-turbo-0613"}
    with patch("navamai.utils.get_model_mapping", return_value=mock_mapping):
        assert utils.resolve_model("gpt-3.5-turbo") == "gpt-3.5-turbo-0613"
        assert utils.resolve_model("claude-2") == "claude-2"