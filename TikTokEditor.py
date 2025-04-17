import subprocess
import random
import os
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
    
    def random_filter_chain(self):
        return ",".join(random.sample(self.effects, 2))
    
    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            # Создаем папку, если её нет
            os.makedirs(output_dir, exist_ok=True)
            
            # Генерируем уникальное имя файла
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(output_dir, f"processed_{timestamp}_{os.path.basename(input_path)}")
            
            # FFmpeg команда
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vf", f"{self.random_filter_chain()},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "22",
                "-movflags", "+faststart",
                "-y",  # Перезапись без подтверждения
                output_path
            ]
            
            # Запуск обработки
            subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE)
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Error: {e.stderr.decode()}")
            return None
        except Exception as e:
            print(f"General Error: {str(e)}")
            return None
