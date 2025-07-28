# Time-stretch / pad a donor mouth-slice so it fits an arbitrary window length.

from pathlib import Path
import numpy as np, librosa, soundfile as sf

DEFAULT_SR = 16_000

def adapt_slice(slice_path: Path, target_duration: float, sr: int = DEFAULT_SR) -> np.ndarray:
    # Returns a 1-D float32 array exactly `target_duration` seconds long.
    y, src_sr = librosa.load(slice_path, sr=sr, mono=True)
    # Time-stretch so total len roughly matches target 
    rate = len(y) / (target_duration * sr)
    y = librosa.effects.time_stretch(y, rate=rate)
    
    target_len = int(target_duration * sr)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]
    return y.astype(np.float32)


def save_wav(y: np.ndarray, path: Path, sr: int = DEFAULT_SR):
    y = np.clip(y, -1.0, 1.0)
    sf.write(path, y, sr)
