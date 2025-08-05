# scripts/ingest_acapellas.py
# to run: poetry run python scripts/ingest_acapellas.py 

from pathlib import Path
from audiorecast.data import downloader, stem_splitter, segmenter

PLAYLIST_FILE = Path("data/ingest/misc.txt")
RAW_DIR = Path("data/raw")

for url in PLAYLIST_FILE.read_text().splitlines():
    wav = downloader.download_audio(url, RAW_DIR)

    #  Use 4-stem model but we are going to build our own accompaniment track
    stems_dir = stem_splitter.split_stems(
        wav_path=wav,
        model="mdx_extra_q", 
        two_stem=False,
        make_acc=True,
    )

    acc = stems_dir / "accompaniment.wav"
    if not acc.exists():
        print(f"[WARN] no accompaniment for {wav.name}, skipping")
        continue

    segmenter.slice_stem(acc)
