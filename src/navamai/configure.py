# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os

import yaml

CONFIG_FILE = "navamai.yml"


def load_config(section=None):
    if not os.path.exists(CONFIG_FILE):
        return {} if section is None else {}

    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    if section:
        return config.get(section, {})
    return config


def has_vision_capability(model):
    config = load_config()
    vision_models = config.get("vision-models", [])
    return model in vision_models


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)


def edit_config(keys, value):
    config = load_config()
    current = config
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    # Convert value based on existing type or default to string
    if keys[-1] in current:
        existing_type = type(current[keys[-1]])
        try:
            if existing_type == bool:
                current[keys[-1]] = value.lower() in ("true", "1", "yes", "on")
            elif existing_type == int:
                current[keys[-1]] = int(value)
            elif existing_type == float:
                current[keys[-1]] = float(value)
            elif existing_type == list:
                current[keys[-1]] = (
                    value.split(",") if isinstance(value, str) else list(value)
                )
            else:
                current[keys[-1]] = str(value)
        except ValueError:
            raise ValueError(f"Cannot convert '{value}' to {existing_type}")
    else:
        # If key doesn't exist, default to string
        current[keys[-1]] = str(value)

    save_config(config)


def get_model_mapping():
    config = load_config()
    return config.get("model-mapping", {})


def resolve_model(model):
    model_mapping = get_model_mapping()
    return model_mapping.get(model, model)
