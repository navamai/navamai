# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license. 
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import pytest
from unittest.mock import patch, mock_open, call
from datetime import datetime
from navamai.metrics import (
    count_tokens,
    generate_yaml_data,
    save_to_yaml,
    save_test_summary,
    read_yaml_files,
    process_data,
    create_sparkline,
    display_trends,
)

def test_count_tokens():
    text = "This is a test."
    assert count_tokens(text) == 5  # Corrected assertion based on actual tokenization

def test_generate_yaml_data():
    provider = "test_provider"
    model = "test_model"
    config = "test_config"
    prompt = "test_prompt"
    status = "success"
    details = "test_details"
    response_time = 1.5
    token_count = 100

    yaml_data = generate_yaml_data(provider, model, config, prompt, status, details, response_time, token_count)
    
    assert len(yaml_data) == 1
    timestamp = list(yaml_data.keys())[0]
    assert yaml_data[timestamp][provider][model][config] == {
        "prompt": prompt,
        "status": status,
        "details": details,
        "response_time": response_time,
        "token_count": token_count,
    }

@patch('builtins.open', new_callable=mock_open)
@patch('yaml.dump')
def test_save_to_yaml(mock_yaml_dump, mock_file):
    data = {"test": "data"}
    save_to_yaml(data)
    mock_file.assert_called_once()
    mock_yaml_dump.assert_called_once()

@patch('navamai.metrics.generate_yaml_data')
@patch('navamai.metrics.save_to_yaml')
def test_save_test_summary(mock_save_to_yaml, mock_generate_yaml_data):
    mock_generate_yaml_data.return_value = {"test": "data"}
    save_test_summary("provider", "model", "config", "prompt", "status", "details", 1.5, 100)
    mock_generate_yaml_data.assert_called_once()
    mock_save_to_yaml.assert_called_once_with({"test": "data"})

@patch('os.listdir')
@patch('builtins.open', new_callable=mock_open)
@patch('yaml.safe_load')
def test_read_yaml_files(mock_yaml_load, mock_file, mock_listdir):
    mock_listdir.return_value = ["test_summary_20230101.yml", "test_summary_20230102.yml"]
    mock_yaml_load.side_effect = [{"data1": "value1"}, {"data2": "value2"}]
    
    result = read_yaml_files()
    
    assert len(result) == 2
    assert result["20230101"] == {"data1": "value1"}
    assert result["20230102"] == {"data2": "value2"}

def test_process_data():
    data = {
        "20230101": {
            "2023-01-01T12:00:00": {
                "provider1": {
                    "model1": {
                        "config1": {
                            "response_time": 1.5,
                            "token_count": 100
                        }
                    }
                }
            }
        }
    }
    
    with patch('navamai.metrics.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 7)
        mock_datetime.strptime.return_value = datetime(2023, 1, 1)
        
        result = process_data(data)
    
    assert len(result) == 1
    assert ("provider1", "model1", "config1") in result
    assert result[("provider1", "model1", "config1")]["response_times"] == [1.5]
    assert result[("provider1", "model1", "config1")]["token_counts"] == [100]

def test_create_sparkline():
    data = [1, 2, 3, 4, 5]
    sparkline = create_sparkline(data, max(data), width=5)
    assert len(sparkline) == 5
    assert all(char in "▁▂▃▄▅▆▇" for char in sparkline)

if __name__ == "__main__":
    pytest.main()