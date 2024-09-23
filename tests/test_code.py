# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license. 
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import pytest
from unittest.mock import patch, mock_open, MagicMock, call
import subprocess
from rich.console import Console

# Import the functions to test
from navamai.code import process_markdown_file, open_vite_server

@pytest.fixture
def mock_console():
    return MagicMock(spec=Console)

def test_open_vite_server(mock_console):
    with patch('webbrowser.open') as mock_webbrowser_open:
        open_vite_server()
        mock_webbrowser_open.assert_called_once_with("http://localhost:5173")

@pytest.mark.parametrize("file_content,expected_app_folder", [
    (
        "# Install script\n\n```bash\nmkdir test_app\ncd test_app\n```\n# File: test.txt\n\n```\nTest content\n```",
        "test_app"
    ),
    (
        "# Install script\n\n```bash\nmkdir complex_app_name\ncd complex_app_name\n```\n# File: test.txt\n\n```\nTest content\n```",
        "complex_app_name"
    ),
])
def test_process_markdown_file(file_content, expected_app_folder, mock_console):
    with patch('builtins.open', mock_open(read_data=file_content)) as mock_file, \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.chmod') as mock_chmod, \
         patch('subprocess.run') as mock_subprocess_run, \
         patch('shutil.rmtree') as mock_rmtree, \
         patch('os.getcwd', return_value='/current/dir'):

        process_markdown_file('test.md', 'apps')

        # Check if the correct app folder was created
        mock_makedirs.assert_any_call('/current/dir/apps', exist_ok=True)
        mock_file.assert_any_call(f'/current/dir/apps/{expected_app_folder}_install_script.sh', 'w')
        
        # Check if chmod was called for the install script
        mock_chmod.assert_called_with(f'/current/dir/apps/{expected_app_folder}_install_script.sh', 0o755)
        
        # Check if subprocess.run was called to execute the install script
        mock_subprocess_run.assert_called_with(
            ['/bin/bash', f'/current/dir/apps/{expected_app_folder}_install_script.sh'],
            check=True,
            cwd='/current/dir/apps'
        )

        # Check if the test.txt file was created
        mock_file.assert_any_call(f'/current/dir/apps/{expected_app_folder}/test.txt', 'w')

def test_process_markdown_file_existing_folder(mock_console):
    file_content = "# Install script\n\n```bash\nmkdir test_app\ncd test_app\n```\n# File: test.txt\n\n```\nTest content\n```"
    
    with patch('builtins.open', mock_open(read_data=file_content)) as mock_file, \
         patch('os.path.exists', side_effect=[True, False, False]), \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.chmod') as mock_chmod, \
         patch('subprocess.run') as mock_subprocess_run, \
         patch('shutil.rmtree') as mock_rmtree, \
         patch('os.getcwd', return_value='/current/dir'):

        process_markdown_file('test.md', 'apps')

        # Check if the existing folder was removed
        mock_rmtree.assert_called_with('/current/dir/apps/test_app')


def test_process_markdown_file_cleanup_script(mock_console):
    file_content = """
# Install script

```bash
mkdir test_app
cd test_app
```

# Run script

```bash
echo "Running the app"
```
"""
    
    with patch('builtins.open', mock_open(read_data=file_content)) as mock_file, \
         patch('os.path.exists', side_effect=[False, False, True, True]), \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.chmod') as mock_chmod, \
         patch('subprocess.run') as mock_subprocess_run, \
         patch('subprocess.Popen') as mock_popen, \
         patch('os.getcwd', return_value='/current/dir'):

        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'', b'')
        mock_popen.return_value = mock_process

        process_markdown_file('test.md', 'apps')

        # Check if subprocess.run was called to execute the cleanup script
        mock_subprocess_run.assert_called_with(
            ['/bin/bash', '/current/dir/apps/cleanup_script.sh'],
            check=True
        )

def test_process_markdown_file_invalid_install_script():
    file_content = """
# Some other content

```
Not an install script
```
"""
    
    with patch('builtins.open', mock_open(read_data=file_content)):
        with pytest.raises(ValueError, match="Install script not found in the markdown file"):
            process_markdown_file('test.md', 'apps')


def test_process_markdown_file_cleanup_script_error():
    file_content = """
# Install script

```bash
mkdir test_app
cd test_app
```

# Run script

```bash
echo "Running the app"
```
"""
    
    with patch('builtins.open', mock_open(read_data=file_content)) as mock_file, \
         patch('os.path.exists', side_effect=[False, False, True, True]), \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.chmod') as mock_chmod, \
         patch('subprocess.run') as mock_subprocess_run, \
         patch('subprocess.Popen') as mock_popen, \
         patch('os.getcwd', return_value='/current/dir'):

        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b'', b'')
        mock_popen.return_value = mock_process

        mock_subprocess_run.side_effect = [None, subprocess.CalledProcessError(1, 'cmd')]

        process_markdown_file('test.md', 'apps')

        # Check if subprocess.run was called to execute the cleanup script
        assert mock_subprocess_run.call_count == 2
        mock_subprocess_run.assert_has_calls([
            call(['/bin/bash', '/current/dir/apps/test_app_install_script.sh'], check=True, cwd='/current/dir/apps'),
            call(['/bin/bash', '/current/dir/apps/cleanup_script.sh'], check=True)
        ])

def test_process_markdown_file_no_run_script():
    file_content = """
# Install script

```bash
mkdir test_app
cd test_app
```

# File: test.txt

```
Test content
```
"""
    
    with patch('builtins.open', mock_open(read_data=file_content)) as mock_file, \
         patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.chmod') as mock_chmod, \
         patch('subprocess.run') as mock_subprocess_run, \
         patch('os.getcwd', return_value='/current/dir'):

        process_markdown_file('test.md', 'apps')

        # Check that subprocess.Popen was not called
        assert mock_subprocess_run.call_count == 1  # Only for the install script