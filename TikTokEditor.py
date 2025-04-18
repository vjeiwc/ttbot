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

    def _random_filters(self) -> str:
        return ",".join(random.sample(self.effects, 2))

    def _build_ffmpeg_command(self, input_path: str, output_path: str) -> list:
        return [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-i", input_path,
            "-vf", (
                f"{self._random_filters()},"
                "scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:-1:-1:color=black"
            ),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-y",
            output_path
        ]

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            if not os.path.exists(input_path):
                self.logger.error(f"Файл не найден: {input_path}")
                return None

            # Генерация имени файла
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(
                output_dir, 
                f"processed_{timestamp}.mp4"
            )

            # Запуск FFmpeg
            result = subprocess.run(
                self._build_ffmpeg_command(input_path, output_path),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if not os.path.exists(output_path):
                self.logger.error("Выходной файл не создан")
                return None

            return output_path

        except subprocess.CalledProcessError as e:
            self.logger.error(f"FFmpeg Error: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"General Error: {str(e)}")
            return None