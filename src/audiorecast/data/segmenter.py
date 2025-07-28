# src/audiorecast/data/segmenter.py
import librosa, numpy as np, soundfile as sf
from pathlib import Path

def slice_stem(stem_path: Path, win_sec=3, hop_sec=1):
    y, sr = librosa.load(stem_path, sr=16000, mono=True)
    win, hop = int(win_sec*sr), int(hop_sec*sr)
    slices_dir = stem_path.parent / "slices"
    slices_dir.mkdir(exist_ok=True)
    for i in range(0, len(y)-win, hop):
        slice_path = slices_dir / f"{stem_path.stem}_{i//hop:05}.wav"
        sf.write(slice_path, y[i:i+win], sr)
