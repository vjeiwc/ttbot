#!/usr/bin/env bash
set -e

# Установка FFmpeg
sudo apt-get update
sudo apt-get install -y ffmpeg

# Очистка кеша
sudo rm -rf /var/lib/apt/lists/*
