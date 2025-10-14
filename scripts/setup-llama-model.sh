#!/bin/bash

# Setup script to download GGUF model for llama.cpp
# This script downloads a quantized model optimized for CPU inference on Mac

set -e

MODEL_DIR="./models"
MODEL_NAME="llama-3.2-3b-instruct-q4_k_m.gguf"
MODEL_URL="https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf"

echo "========================================="
echo "llama.cpp Model Setup"
echo "========================================="
echo ""
echo "Model: Llama 3.2 3B Instruct (Q4_K_M)"
echo "Size: ~2GB"
echo "Optimized for: Mac CPU inference"
echo ""

# Create models directory
mkdir -p "$MODEL_DIR"

# Check if model already exists
if [ -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "✓ Model already exists at $MODEL_DIR/$MODEL_NAME"
    echo ""
    MODEL_SIZE=$(du -h "$MODEL_DIR/$MODEL_NAME" | cut -f1)
    echo "File size: $MODEL_SIZE"
    exit 0
fi

echo "Downloading model..."
echo "This may take a few minutes depending on your connection"
echo ""

# Download model
if command -v wget &> /dev/null; then
    wget -O "$MODEL_DIR/$MODEL_NAME" "$MODEL_URL" --progress=bar:force
elif command -v curl &> /dev/null; then
    curl -L "$MODEL_URL" -o "$MODEL_DIR/$MODEL_NAME" --progress-bar
else
    echo "Error: Neither wget nor curl is installed"
    exit 1
fi

echo ""
echo "✓ Model downloaded successfully!"
echo ""
MODEL_SIZE=$(du -h "$MODEL_DIR/$MODEL_NAME" | cut -f1)
echo "Location: $MODEL_DIR/$MODEL_NAME"
echo "Size: $MODEL_SIZE"
echo ""
echo "Next steps:"
echo "  docker-compose -f docker-compose-local.yml up"

