import subprocess
import random
import os
import logging
from datetime import datetime

class TikTokEditor:
    def __init__(self):
        self.effects = [
            "hue=s=0",               # Простой фильтр
            "curves=vintage",         # Оптимизированный эффект
            "split=2[split][tmp];[tmp]boxblur=10[blur];[split][blur]overlay"  # Лёгкий эффект размытия
        ]
        self.logger = logging.getLogger(__name__)
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL)
        except Exception as e:
            self.logger.critical("FFmpeg недоступен: %s", e)
            raise

    def _random_filters(self) -> str:
        return random.choice(self.effects)  # Только 1 эффект для экономии CPU

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            # Ограничение размера видео
            if os.path.getsize(input_path) > 20 * 1024 * 1024:  # 20MB
                self.logger.warning("Видео слишком большое")
                return None

            # Создание выходной директории
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"processed_{datetime.now().timestamp()}.mp4")
            
            # Оптимизированные параметры FFmpeg
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-i", input_path,
                "-vf", f"{self._random_filters()},scale=640:1136:force_original_aspect_ratio=decrease",  # Низкое разрешение
                "-c:v", "libx264",
                "-preset", "ultrafast",  # Минимальная нагрузка на CPU
                "-crf", "30",            # Среднее качество
                "-t", "55",               # Максимум 55 секунд
                "-an",                    # Отключение аудио
                "-y",
                output_path
            ]
            
            result = subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=50               # Таймаут меньше Render-лимита
            )
            
            return output_path if os.path.exists(output_path) else None
            
        except subprocess.CalledProcessError as e:
            self.logger.error("FFmpeg error: %s", e.stderr.decode())
        except Exception as e:
            self.logger.error("Ошибка: %s", e, exc_info=True)
        return None
