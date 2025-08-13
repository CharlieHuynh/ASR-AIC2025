import os
import json
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

JSON_DIR = "media-info"
AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)

def download_mp3_from_json(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        url = data.get("watch_url")
        if not url:
            print(f"[SKIP] Không tìm thấy watch_url trong {json_file}")
            return
        
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        output_path = os.path.join(AUDIO_DIR, base_name)  # Không thêm .mp3 ở đây

        # Nếu file đã tồn tại thì bỏ qua
        if os.path.exists(f"{output_path}.mp3"):
            print(f"[EXIST] Bỏ qua {output_path}.mp3")
            return

        print(f"[DOWNLOADING] {url} -> {output_path}.mp3")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,  # yt-dlp sẽ tự thêm .mp3
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'noprogress': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"[DONE] {output_path}.mp3")
    except Exception as e:
        print(f"[ERROR] {json_file} - {e}")

def main():
    json_files = [
        os.path.join(JSON_DIR, f) for f in os.listdir(JSON_DIR)
        if f.lower().endswith(".json")
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_mp3_from_json, json_files)

if __name__ == "__main__":
    main()
