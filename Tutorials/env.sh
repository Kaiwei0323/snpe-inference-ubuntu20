#!/bin/bash

# ---------------------------------------------------------
#  System Dependencies Setup for SNPE + Python Environment
# ---------------------------------------------------------

# SNPE SDK paths
SDK_DIR="/data/sdk"
SNPE_ROOT="$SDK_DIR/v2.26.0.240828/qairt/2.26.0.240828"

echo "Updating package list..."
apt update -y

echo "Installing core utilities..."
apt install -y software-properties-common cmake

echo "Installing MQTT broker & clients..."
apt install -y mosquitto mosquitto-clients

echo "Installing Cairo & GObject dependencies..."
apt install -y libcairo2-dev libgirepository1.0-dev

echo "Installing PortAudio..."
apt install -y portaudio19-dev

echo "Installing Python build tools..."
apt install -y python3-pip python3-dev

echo "Installing Python packages from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

cat >> ~/.bashrc << 'EOF'

export SDK_DIR="/data/sdk"
export SNPE_ROOT="$SDK_DIR/v2.26.0.240828/qairt/2.26.0.240828"
export ADSP_LIBRARY_PATH="$SNPE_ROOT/lib/hexagon-v68/unsigned"
export LD_PRELOAD=/lib/aarch64-linux-gnu/libgomp.so.1

EOF

echo "All dependencies installed successfully."

