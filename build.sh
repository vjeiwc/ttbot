#!/usr/bin/env bash
set -e # Остановить при ошибках

# Установка FFmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# Python зависимости
pip install --upgrade pip
pip install -r requirements.txt
