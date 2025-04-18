#!/usr/bin/env bash
set -e

# Установка FFmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# Оптимизация памяти
sudo rm -rf /var/lib/apt/lists/*

# Python зависимости
pip install --no-cache-dir -r requirements.txt
