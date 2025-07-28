# src/audiorecast/data/stem_splitter.py
from pathlib import Path
import subprocess
import librosa, soundfile as sf, numpy as np

__all__ = ["split_stems"]

def _make_accompaniment(stems_dir: Path) -> Path:
    # Merges bass + drums + other → accompaniment.wav (same SR/chan as stems).
    acc_path = stems_dir / "accompaniment.wav"
    if acc_path.exists():
        return acc_path

    mix, sr = None, None
    for name in ("bass.wav", "drums.wav", "other.wav"):
        stem = stems_dir / name
        if not stem.exists():
            continue
        y, sr = librosa.load(stem, sr=None, mono=False)  # y shape: (C, N)
        mix = y if mix is None else mix + y

    if mix is None:
        raise RuntimeError(f"No stems found in {stems_dir}")

    # (C, N) to (N, C)  and clip to [-1,1]
    mix = mix.T.astype(np.float32)
    mix = np.clip(mix, -1.0, 1.0)

    sf.write(acc_path, mix, sr)
    return acc_path


# Run Demucs and return the directory containing the stems.
def split_stems(
    wav_path: Path,
    model: str = "mdx_extra_q",
    two_stem: bool = False,
    make_acc: bool = False,
) -> Path:
    
    out_root = wav_path.parent / wav_path.stem
    if out_root.exists():
        return next(out_root.glob(f"{model}/*"))

    cmd = ["demucs", "-n", model, "-o", str(out_root)]
    if two_stem:
        cmd += ["--two-stems", "vocals"]
    cmd.append(str(wav_path))
    subprocess.run(cmd, check=True)

    stems_dir = next(out_root.glob(f"{model}/*"))
    if make_acc and not two_stem:
        _make_accompaniment(stems_dir)
    return stems_dir
