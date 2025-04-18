#!/usr/bin/env bash
set -e

# Установка FFmpeg с проверкой
sudo apt-get update
sudo apt-get install -y ffmpeg

# Проверка версии
echo "Версия FFmpeg:"
ffmpeg -version | head -n 1

# Установка зависимостей Python
python -m pip install --upgrade pip
pip install -r requirements.txt

# Проверка свободного места
df -h
