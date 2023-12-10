#!/bin/bash

# Check if script is running as root user
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Please use 'sudo' or run as root."
    exit 1
fi

# Install Python3-pip
apt install python3-pip -y

# Install Git
apt install git -y

# Install other requirements to run the script
pip install opencv-python imageio

# Additional requirements for Imageo for error handling
pip install imageio[ffmpeg]
pip install imageio[pyav]
