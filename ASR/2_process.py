import os
import torch
from faster_whisper import WhisperModel
from tqdm import tqdm

AUDIO_DIR = "audio"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tự phát hiện GPU
if torch.cuda.is_available():
    device_type = "cuda"
    compute_type = "float16"
    print("[INFO] Phát hiện GPU - sử dụng CUDA")
else:
    device_type = "cpu"
    compute_type = "int8"  # giảm RAM khi chạy CPU
    print("[INFO] Không có GPU - chạy bằng CPU")

print("[INFO] Đang tải model...")
model = WhisperModel("medium", device=device_type, compute_type=compute_type)

def asr_alignment_to_paragraph(audio_path):
    # segments là generator, xử lý tuần tự
    segments, _ = model.transcribe(audio_path, beam_size=5)

    parts = []
    for seg in segments:
        start_time = int(seg.start)
        minutes = start_time // 60
        seconds = start_time % 60
        time_str = f"{minutes}:{seconds:02d}"
        text = seg.text.strip()
        parts.append(f"{text} ({time_str})")

    return ", ".join(parts)

def main():
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".mp3")]

    for audio_file in tqdm(audio_files, desc="Xử lý audio", unit="file"):
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        base_name = os.path.splitext(audio_file)[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")

        if os.path.exists(output_path):
            tqdm.write(f"[SKIP] {output_path} đã tồn tại")
            continue

        try:
            paragraph = asr_alignment_to_paragraph(audio_path)

            # Lưu ngay khi xong file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(paragraph)

            tqdm.write(f"[DONE] {output_path} đã lưu")
        except Exception as e:
            tqdm.write(f"[ERROR] {audio_file} - {e}")

if __name__ == "__main__":
    main()
