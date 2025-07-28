# Concatenates an ordered list of numpy slices with a tiny cross-fade to avoid pops.

import numpy as np
from pathlib import Path
from audiorecast.synthesis.synthesizer import save_wav, DEFAULT_SR

def _crossfade(a: np.ndarray, b: np.ndarray, fade_ms: int = 20) -> np.ndarray:
    fade = int(DEFAULT_SR * fade_ms / 1000)
    if fade == 0:
        return np.concatenate([a, b])
    
    window = np.linspace(0, 1, fade, dtype=np.float32)
    to_return = np.concatenate(
        [a[:-fade] , a[-fade:] * (1 - window) + b[:fade] * window , b[fade:]]
    )
    return to_return

def assemble(slices: list[np.ndarray], fade_ms: int = 20) -> np.ndarray:
    track = slices[0]
    for nxt in slices[1:]:
        track = _crossfade(track, nxt, fade_ms)
    return track

def save_track(track: np.ndarray, out_path: Path):
    save_wav(track, out_path)
