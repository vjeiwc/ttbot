import subprocess
import random
import os
from datetime import datetime
import logging

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

    def random_filter_chain(self):
        return ",".join(random.sample(self.effects, 2))

    def process_video(self, input_path: str, output_dir: str) -> str | None:
        try:
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            output_path = os.path.join(output_dir, f"processed_{timestamp}.mp4")
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-i", input_path,
                "-vf", f"{self.random_filter_chain()},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "22",
                "-y",
                output_path
            ]
            
            subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE)
            return output_path
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"FFmpeg Error: {e.stderr.decode()}")
            return None
        except Exception as e:
            self.logger.error(f"General Error: {str(e)}")
            return None
