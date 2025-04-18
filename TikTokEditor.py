import subprocess
import os
import logging
from datetime import datetime

class TikTokEditor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def _even_size(self, width: int, height: int) -> tuple:
        """Делаем размеры четными"""
        return (width // 2 * 2, height // 2 * 2)

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            # Проверка входного файла
            if not os.path.exists(input_path):
                self.logger.error("Input file missing")
                return None

            # Создаем папку для результатов
            os.makedirs(output_dir, exist_ok=True)
            
            # Генерируем имя выходного файла
            output_path = os.path.join(
                output_dir, 
                f"processed_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            )

            # Минимальная обработка видео
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-i", input_path,
                "-vf", "scale=640:-2:force_original_aspect_ratio=decrease,eq=contrast=1.1:saturation=1.2",  # Простейшие эффекты
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "30",
                "-an",  # Без аудио
                "-y",
                output_path
            ]
            
            # Запускаем обработку
            subprocess.run(
                ffmpeg_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            return output_path if os.path.exists(output_path) else None
            
        except Exception as e:
            self.logger.error("Processing failed: %s", str(e))
            return None
