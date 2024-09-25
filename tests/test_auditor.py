# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import pytest

from navamai.auditor import Auditor


@pytest.fixture
def sample_data():
    return [
        {
            "timestamp": "2023-09-22T10:00:00",
            "command": "create file example.txt",
            "prompt": "Create a text file",
            "destination_file": "example.txt",
        },
        {
            "timestamp": "2023-09-22T10:30:00",
            "command": "read file example.txt",
            "source_file": "example.txt",
        },
        {
            "timestamp": "2023-09-22T11:00:00",
            "command": "create table employees",
            "custom_prompt": "Create a table of employees",
            "destination_file": "employees.csv",
        },
    ]


@pytest.fixture
def auditor(sample_data):
    return Auditor(sample_data)


def test_init(auditor, sample_data):
    assert len(auditor.data) == len(sample_data)
    assert len(auditor.timestamps) == len(sample_data)
    assert len(auditor.commands) == len(sample_data)
    assert isinstance(auditor.stop_words, set)
    assert isinstance(auditor.excluded_words, set)


def test_command_frequency_analysis(auditor):
    freq_analysis = auditor.command_frequency_analysis()
    assert isinstance(freq_analysis, list)
    assert len(freq_analysis) > 0
    assert isinstance(freq_analysis[0], tuple)
    assert len(freq_analysis[0]) == 2


def test_file_operation_analysis(auditor):
    file_ops = auditor.file_operation_analysis()
    assert isinstance(file_ops, dict)
    assert "read_write_ratio" in file_ops
    assert "common_extensions" in file_ops
    assert "common_source_folders" in file_ops
    assert "common_destination_folders" in file_ops


def test_prompt_analysis(auditor):
    prompt_analysis = auditor.prompt_analysis()
    assert isinstance(prompt_analysis, dict)
    assert "common_keywords" in prompt_analysis
    assert "common_bigrams" in prompt_analysis
    assert "average_prompt_length" in prompt_analysis
    assert "task_types" in prompt_analysis


def test_time_based_analysis(auditor):
    time_analysis = auditor.time_based_analysis()
    assert isinstance(time_analysis, dict)
    assert "peak_hours" in time_analysis
    assert "busiest_days" in time_analysis
    assert "average_time_between_commands" in time_analysis


def test_user_behavior_analysis(auditor):
    behavior_analysis = auditor.user_behavior_analysis()
    assert isinstance(behavior_analysis, dict)
    assert "common_command_sequences" in behavior_analysis
    assert "prompt_complexity_over_time" in behavior_analysis


def test_command_prompt_distribution(auditor):
    distribution = auditor.command_prompt_distribution()
    assert isinstance(distribution, dict)
    assert "with_user_prompt" in distribution
    assert "with_custom_prompt" in distribution
    assert "with_prompt_file" in distribution
    assert "without_prompt" in distribution


def test_create_ascii_timeline(auditor):
    timeline = auditor.create_ascii_timeline()
    assert isinstance(timeline, str)
    assert len(timeline) > 0


def test_get_file_extension():
    assert Auditor._get_file_extension("example.txt") == "txt"
    assert Auditor._get_file_extension("file_without_extension") == "no_extension"


def test_get_folder():
    assert Auditor._get_folder("folder/subfolder/file.txt") == "folder"
    assert Auditor._get_folder("file.txt") == "root"


def test_categorize_task():
    assert Auditor._categorize_task("Create a table of employees") == "create table"
    assert (
        Auditor._categorize_task("Write a function to calculate sum")
        == "write function"
    )
    assert Auditor._categorize_task("Explain how to use Python") == "explanation"
    assert Auditor._categorize_task("Random task") == "other"


def test_get_bigrams():
    words = ["hello", "world", "python", "test"]
    bigrams = Auditor._get_bigrams(words)
    assert bigrams == ["hello world", "world python", "python test"]


def test_edge_cases(sample_data):
    # Test with only one data point
    single_data_auditor = Auditor([sample_data[0]])
    assert (
        single_data_auditor.time_based_analysis()["average_time_between_commands"] == 0
    )

    # Test with identical timestamps
    identical_timestamps_data = [
        {**sample_data[0], "timestamp": "2023-09-22T10:00:00"},
        {**sample_data[1], "timestamp": "2023-09-22T10:00:00"},
    ]
    identical_timestamps_auditor = Auditor(identical_timestamps_data)
    assert (
        identical_timestamps_auditor.time_based_analysis()[
            "average_time_between_commands"
        ]
        == 0
    )
