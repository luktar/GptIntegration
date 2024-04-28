#!/usr/bin/env bash

# Update Homebrew recipes
echo "Updating brew recipes..."
brew update

# Install ffmpeg
echo "Installing ffmpeg..."
brew install ffmpeg

# Install portaudio
echo "Installing portaudio..."
brew install portaudio

echo "Installation completed."