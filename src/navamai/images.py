# Copyright 2024 and beyond, NavamAI. All Rights Reserved.
# https://www.navamai.com/
# This code is Apache-2.0 licensed. Please see the LICENSE file in our repository for the full license text.
# You may use this code under the terms of the Apache-2.0 license.
# This code is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import io
import os

import cv2
import term_image.image as TermImage
from PIL import Image
from rich.console import Console

console = Console()


def display_image(image_path):
    if "TERM_PROGRAM" in os.environ and os.environ["TERM_PROGRAM"] == "vscode":
        img = TermImage.from_file(image_path)
        img.draw()
    else:
        console.print(f"Use VS Code Terminal for displaying images.", style="yellow")
        console.print(
            f"Processed image saved to config > save-folder if save is enabled."
        )


def capture_image():
    # [TODO] Fix warning
    # WARNING: AVCaptureDeviceTypeExternal is deprecated for Continuity Cameras. Please use AVCaptureDeviceTypeContinuityCamera and add NSCameraUseContinuityCameraDeviceType to your Info.plist.

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise IOError("Cannot access the camera")

    # Wait for the camera to initialize and adjust light levels
    for i in range(30):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise IOError("Failed to capture an image")

    _, buffer = cv2.imencode(".jpg", frame)

    return buffer.tobytes()


def resize_image(image_data, max_size=5 * 1024 * 1024):
    """Resize the image to ensure it's under 5MB."""
    img = Image.open(io.BytesIO(image_data))

    # Calculate current size
    current_size = len(image_data)

    if current_size <= max_size:
        return image_data  # No need to resize

    # Calculate the scale factor
    scale_factor = (max_size / current_size) ** 0.5

    # Calculate new dimensions
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)

    # Resize the image
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Convert back to bytes
    buffer = io.BytesIO()
    img_resized.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()
