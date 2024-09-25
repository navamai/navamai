# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

from unittest.mock import call, mock_open, patch

import yaml

# Mock data for testing
mock_config_data = {
    "vision-models": ["model_a", "model_b"],
    "model-mapping": {"model_x": "model_y"},
}

# Convert mock_config_data to YAML format for file read simulation
mock_config_yaml = yaml.dump(mock_config_data)


# Test load_config
def test_load_config_no_file():
    with patch("os.path.exists", return_value=False):
        from navamai.configure import load_config

        assert load_config() == {}
        assert load_config("vision-models") == {}


def test_load_config_with_file():
    with patch("os.path.exists", return_value=True), patch(
        "builtins.open", mock_open(read_data=mock_config_yaml)
    ):
        from navamai.configure import load_config

        assert load_config() == mock_config_data
        assert load_config("vision-models") == mock_config_data["vision-models"]


# Test has_vision_capability
def test_has_vision_capability():
    with patch("navamai.configure.load_config", return_value=mock_config_data):
        from navamai.configure import has_vision_capability

        assert has_vision_capability("model_a") is True
        assert has_vision_capability("model_unknown") is False


# Test save_config
def test_save_config():
    with patch("builtins.open", mock_open()) as mocked_file:
        from navamai.configure import save_config

        save_config(mock_config_data)
        mocked_file.assert_called_once_with("navamai.yml", "w")

        # Ensure the file was written with the correct YAML content
        handle = mocked_file()
        written_data = "".join(
            call_arg[0][0] for call_arg in handle.write.call_args_list
        )
        assert written_data == yaml.dump(mock_config_data)


# Test edit_config
def test_edit_config_existing_key():
    updated_config_data = mock_config_data.copy()
    updated_config_data["vision-models"] = ["model_c", "model_d"]

    with patch("navamai.configure.load_config", return_value=mock_config_data), patch(
        "navamai.configure.save_config"
    ) as mock_save_config:
        from navamai.configure import edit_config

        edit_config(["vision-models"], "model_c,model_d")
        mock_save_config.assert_called_once_with(updated_config_data)


def test_edit_config_new_key():
    updated_config_data = mock_config_data.copy()
    updated_config_data["new-section"] = {"new-key": "new-value"}

    with patch("navamai.configure.load_config", return_value=mock_config_data), patch(
        "navamai.configure.save_config"
    ) as mock_save_config:
        from navamai.configure import edit_config

        edit_config(["new-section", "new-key"], "new-value")
        mock_save_config.assert_called_once_with(updated_config_data)


def test_edit_config_type_conversion():
    initial_config = {"test": {"number": "42"}}
    updated_config = {
        "test": {"number": "43"}
    }  # Expecting the value to remain as a string

    with patch("navamai.configure.load_config", return_value=initial_config), patch(
        "navamai.configure.save_config"
    ) as mock_save_config:
        from navamai.configure import edit_config

        edit_config(["test", "number"], "43")

        # Ensure that the value is stored as a string
        mock_save_config.assert_called_once_with(updated_config)


# Test get_model_mapping
def test_get_model_mapping():
    with patch("navamai.configure.load_config", return_value=mock_config_data):
        from navamai.configure import get_model_mapping

        assert get_model_mapping() == mock_config_data["model-mapping"]


# Test resolve_model
def test_resolve_model():
    with patch(
        "navamai.configure.get_model_mapping",
        return_value=mock_config_data["model-mapping"],
    ):
        from navamai.configure import resolve_model

        assert resolve_model("model_x") == "model_y"
        assert resolve_model("model_unknown") == "model_unknown"
