#!/bin/bash
# Script to start Home Assistant in the devcontainer

echo "Starting Home Assistant..."
python3 -m homeassistant --config /config --debug
