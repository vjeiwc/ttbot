import subprocess
import random
import os
import logging
from datetime import datetime

class TikTokEditor:
    def __init__(self):
        self.effects = [
            "hue=s=0", 
            "curves=vintage",
            "split=2[split][tmp];[tmp]boxblur=10[blur];[split][blur]overlay"
        ]
        self.logger = logging.getLogger(__name__)
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        try:
            subprocess.run(
                ["ffmpeg", "-version"], 
                check=True, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            self.logger.critical("FFmpeg недоступен: %s", e)
            raise RuntimeError("Установите FFmpeg") from e

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            # Убедимся, что файл существует
            if not os.path.exists(input_path):
                self.logger.error("Файл не найден: %s", input_path)
                return None

            # Проверка размера файла
            if os.path.getsize(input_path) > 20 * 1024 * 1024:
                self.logger.warning("Видео слишком большое (макс. 20MB)")
                return None

            # Создаем выходную директорию
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"processed_{datetime.now().timestamp()}.mp4")
            
            # Упрощенная команда FFmpeg (без фильтров)
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-i", input_path,
                "-vf", "scale=640:1136:force_original_aspect_ratio=decrease",  # Без hue
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "28",
                "-t", "55",
                "-an",
                "-y",
                output_path
            ]
            
            # Запуск с полным логированием
            result = subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=50
            )
            
            # Логируем вывод FFmpeg
            self.logger.info("FFmpeg stdout: %s", result.stdout)
            if result.stderr:
                self.logger.error("FFmpeg stderr: %s", result.stderr)

            return output_path if os.path.exists(output_path) else None
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Ошибка FFmpeg: %s", e.stderr)
            return None
        except Exception as e:
            self.logger.error("Ошибка: %s", e, exc_info=True)
            return None
