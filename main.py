#!/usr/bin/python3

import cv2
import numpy as np
import imageio
from pathlib import Path

def cartoonize_image(image_path):
    # Read the input image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise and smooth the image while preserving edges
    cartoon = cv2.bilateralFilter(gray, d=9, sigmaColor=300, sigmaSpace=300)

    # Create an edge mask using adaptive thresholding
    edges = cv2.adaptiveThreshold(cartoon, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

    # Combine the cartoon image and edge mask
    cartoon = cv2.bitwise_and(cartoon, cartoon, mask=edges)

    return cartoon

def create_cartoon_video(image_path, output_path, duration_minutes=1, fps=24):
    # Calculate the total number of frames required
    duration_seconds = duration_minutes * 60
    total_frames = int(fps * duration_seconds)

    # Cartoonize the input image
    cartoon_image = cartoonize_image(image_path)

    # Create a temporary directory to store individual frames
    temp_dir = Path("temp_frames")
    temp_dir.mkdir(exist_ok=True)

    # Write cartoon image to temp frames
    for i in range(total_frames):
        frame_name = temp_dir / f"frame_{i:03d}.png"
        cv2.imwrite(str(frame_name), cartoon_image)

    # Create the cartoon video using imageio
    video_writer = imageio.get_writer(output_path, fps=fps)

    # Add frames to the video
    for i in range(total_frames):
        frame_name = temp_dir / f"frame_{i:03d}.png"
        video_writer.append_data(imageio.imread(frame_name))

    # Close the video writer
    video_writer.close()

    # Remove temporary frames
    for frame in temp_dir.glob("*.png"):
        frame.unlink()

    # Remove temporary directory
    temp_dir.rmdir()

if __name__ == "__main__":
    # Get input image path from user
    image_path = input("Enter the path of the input image: ")

    # Get desired video duration from user
    duration_minutes = float(input("Enter the desired length of the video in minutes: "))

    # Output video path
    output_path = "cartoon_video.mp4"

    create_cartoon_video(image_path, output_path, duration_minutes)
    print(f"Cartoon video created: {output_path}")
