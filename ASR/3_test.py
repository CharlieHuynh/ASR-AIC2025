import os
from pydub import AudioSegment

AUDIO_DIR = "audio"
OUTPUT_DIR = "audio_cut"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CUT_DURATION_MS = 2 * 60 * 1000  # 2 phút => ms

def cut_first_2_minutes(audio_path, output_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        # Cắt đoạn 0 -> 2 phút
        cut_audio = audio[:CUT_DURATION_MS]
        cut_audio.export(output_path, format="mp3")
        print(f"[DONE] {output_path}")
    except Exception as e:
        print(f"[ERROR] {audio_path} - {e}")

def main():
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".mp3")]
    for file_name in audio_files:
        input_path = os.path.join(AUDIO_DIR, file_name)
        output_path = os.path.join(OUTPUT_DIR, file_name)
        cut_first_2_minutes(input_path, output_path)

if __name__ == "__main__":
    main()
