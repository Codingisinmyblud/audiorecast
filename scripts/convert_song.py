# for reference: audiorecast/scripts/convert_song.py
# to run: poetry run python scripts/convert_song.py --input path/to/song.wav --out path/to/output.wav

import argparse, sys
from pathlib import Path
from audiorecast.pipeline import convert_song

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Path to song (wav/mp3)")
parser.add_argument("--out",   required=True, help="Output wav name")
args = parser.parse_args()

convert_song(Path(args.input), Path(args.out))
