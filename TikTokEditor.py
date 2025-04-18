import subprocess
import random
import os
import logging
from datetime import datetime

class TikTokEditor:
    def __init__(self):
        self.effects = [
            "noise=alls=20:allf=t", 
            "hue=s=0",
            "curves=vintage",
            "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3",
            "zoompan=z='zoom+0.002':d=150"
        ]
        self.logger = logging.getLogger(__name__)
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Проверка доступности FFmpeg"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.logger.info("FFmpeg доступен")
        except Exception as e:
            self.logger.error("FFmpeg не установлен: %s", str(e))
            raise RuntimeError("FFmpeg не найден") from e

    def _random_filters(self) -> str:
        return ",".join(random.sample(self.effects, 2))

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            # Проверка существования исходного файла
            if not os.path.exists(input_path):
                self.logger.error("Исходный файл не найден: %s", input_path)
                return None

            # Создание выходной директории
            os.makedirs(output_dir, exist_ok=True)
            self.logger.info("Выходная директория: %s", output_dir)

            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(output_dir, f"processed_{timestamp}.mp4")
            
            # Команда FFmpeg с улучшенными параметрами
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "verbose",  # Максимально подробное логирование
                "-i", input_path,
                "-vf", f"format=yuv420p,{self._random_filters()},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "20",
                "-movflags", "+faststart",
                "-y",
                output_path
            ]
            
            # Запуск обработки
            result = subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # Таймаут 5 минут
            )
            
            # Логирование вывода
            self.logger.info("FFmpeg stdout: %s", result.stdout)
            if result.stderr:
                self.logger.error("FFmpeg stderr: %s", result.stderr)

            if not os.path.exists(output_path):
                self.logger.error("Выходной файл не создан")
                return None

            return output_path
            
        except subprocess.CalledProcessError as e:
            self.logger.error("Ошибка FFmpeg: %s", e.stderr, exc_info=True)
            return None
        except Exception as e:
            self.logger.error("Общая ошибка: %s", str(e), exc_info=True)
            return None
