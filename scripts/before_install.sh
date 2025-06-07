#!/bin/bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv pipenv

# Create directory if it doesn't exist
mkdir -p /var/www/investment-analysis
