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
        """Проверка наличия FFmpeg"""
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL)
        except Exception as e:
            self.logger.critical("FFmpeg не установлен: %s", e)
            raise

    def _random_filter(self) -> str:
        """Выбор случайного фильтра"""
        return random.choice(self.effects)

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        """Обработка видео"""
        try:
            # Проверка размера файла
            if os.path.getsize(input_path) > 20 * 1024 * 1024:
                self.logger.warning("Файл слишком большой: %s", input_path)
                return None

            # Генерация имени выходного файла
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(output_dir, f"processed_{timestamp}.mp4")
            
            # Команда FFmpeg (оптимизированная для Render)
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-i", input_path,
                "-vf", f"{self._random_filter()},scale=640:1136:force_original_aspect_ratio=decrease",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "28",
                "-t", "55",
                "-an",  # Без аудио
                "-y",
                output_path
            ]
            
            # Запуск обработки
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=50
            )
            return output_path if os.path.exists(output_path) else None
            
        except Exception as e:
            self.logger.error("Ошибка обработки: %s", e, exc_info=True)
            return None