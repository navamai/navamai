# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license. 
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import io
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
from navamai.images import display_image, capture_image, resize_image

@pytest.fixture
def mock_console():
    with patch('images.console') as mock:
        yield mock

@pytest.fixture
def mock_term_image():
    with patch('images.TermImage') as mock:
        yield mock

def test_capture_image_success():
    with patch('cv2.VideoCapture') as mock_cap:
        mock_cap.return_value.isOpened.return_value = True
        mock_cap.return_value.read.return_value = (True, np.zeros((100, 100, 3), dtype=np.uint8))
        mock_cap.return_value.release = MagicMock()
        
        result = capture_image()
        
        assert isinstance(result, bytes)
        mock_cap.assert_called_once_with(1)
        mock_cap.return_value.read.assert_called()
        mock_cap.return_value.release.assert_called_once()

def test_capture_image_camera_not_opened():
    with patch('cv2.VideoCapture') as mock_cap:
        mock_cap.return_value.isOpened.return_value = False
        
        with pytest.raises(IOError, match="Cannot access the camera"):
            capture_image()

def test_capture_image_capture_failed():
    with patch('cv2.VideoCapture') as mock_cap:
        mock_cap.return_value.isOpened.return_value = True
        mock_cap.return_value.read.return_value = (False, None)
        
        with pytest.raises(IOError, match="Failed to capture an image"):
            capture_image()

def test_resize_image_no_resize_needed():
    # Create a small image that doesn't need resizing
    img = Image.new('RGB', (100, 100), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    small_image_data = buffer.getvalue()
    
    result = resize_image(small_image_data)
    assert result == small_image_data

if __name__ == "__main__":
    pytest.main()