#!/bin/bash

# Define directories
SDK_DIR="/data/sdk"
VIDEO_DIR="/data/video"
ZIP_FILE="v2.26.0.240828.zip"

# Create the necessary directories if they do not exist
mkdir -p "$SDK_DIR"
mkdir -p "$VIDEO_DIR"

# Download the zip file
echo "Downloading SDK zip file..."
curl -L -o "$SDK_DIR/$ZIP_FILE" "https://huggingface.co/datasets/kaiwei0323/my-sdk/resolve/main/v2.26.0.240828.zip"

# Check if the zip file exists before attempting to unzip
if [ -f "$SDK_DIR/$ZIP_FILE" ]; then
  echo "Extracting zip file..."
  unzip "$SDK_DIR/$ZIP_FILE" -d "$SDK_DIR"
  echo "SDK extracted successfully."
  # Delete the zip file after extraction
  rm "$SDK_DIR/$ZIP_FILE"
  echo "ZIP file deleted."
else
  echo "Error: ZIP file not found at $SDK_DIR/$ZIP_FILE. Skipping extraction."
fi

# Download the video files into the correct directory
echo "Downloading video files..."
curl -L -o "$VIDEO_DIR/brain_tumor.mp4" "https://huggingface.co/datasets/kaiwei0323/demo-video/resolve/main/brain_tumor.mp4"
curl -L -o "$VIDEO_DIR/fall.mp4" "https://huggingface.co/datasets/kaiwei0323/demo-video/resolve/main/fall.mp4"
curl -L -o "$VIDEO_DIR/freeway.mp4" "https://huggingface.co/datasets/kaiwei0323/demo-video/resolve/main/freeway.mp4"
curl -L -o "$VIDEO_DIR/med_ppe.mp4" "https://huggingface.co/datasets/kaiwei0323/demo-video/resolve/main/med_ppe.mp4"
curl -L -o "$VIDEO_DIR/ppe.mp4" "https://huggingface.co/datasets/kaiwei0323/demo-video/resolve/main/ppe.mp4"

echo "Video files downloaded successfully to $VIDEO_DIR"

