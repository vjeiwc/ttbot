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
        selected = random.sample(self.effects, 2)
        return ",".join(selected)
    
    def process_video(self, input_path, output_dir):
        try:
            base_name = os.path.basename(input_path)
            output_path = os.path.join(output_dir, f"processed_{datetime.now().strftime('%Y%m%d%H%M%S')}_{base_name}")
            
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vf", f"{self.random_filter_chain()},scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:color=black",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "22",
                "-movflags", "+faststart",
                "-metadata", f"creation_time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "-y", output_path
            ]
            
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"✅ Видео готово: {output_path}")
            return output_path
                
        except Exception as e:
            print(f"❌ Ошибка: {str(e)}")
            return None