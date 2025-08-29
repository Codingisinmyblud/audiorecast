# src/audiorecast/data/segmenter.py
from pathlib import Path
import librosa, soundfile as sf, numpy as np

DEFAULT_SR = 16_000

def slice_stem(stem_path: Path, win_sec: float = 3.0, hop_sec: float = 1.0) -> list[Path]:
    # Returns a list of Path objects for every slice written. 
    # If slices already exist, they are reused (no double-write).

    y, sr = librosa.load(stem_path, sr=DEFAULT_SR, mono=True)
    win, hop = int(win_sec * sr), int(hop_sec * sr)

    slices_dir = stem_path.parent / "slices"
    slices_dir.mkdir(exist_ok=True)

    paths: list[Path] = []
    if len(y) <= win:                              
        p = slices_dir / f"{stem_path.stem}_00000.wav"
        if not p.exists():
            sf.write(p, y, sr)
        paths.append(p)
        return paths

    for i in range(0, len(y) - win, hop):
        p = slices_dir / f"{stem_path.stem}_{i//hop:05}.wav"
        if not p.exists():                         # this avoids re-writing on reruns
            sf.write(p, y[i : i + win], sr)
        paths.append(p)

    return paths
