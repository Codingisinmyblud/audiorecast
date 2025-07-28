# End-to-end: input song → acapella song.

from pathlib import Path
import numpy as np, librosa
from tqdm import tqdm

from audiorecast.data import stem_splitter, segmenter
from audiorecast.embedding.extractor import EmbeddingExtractor
from audiorecast.matching.matcher import Matcher
from audiorecast.synthesis.synthesizer import adapt_slice, DEFAULT_SR
from audiorecast.synthesis.assembler import assemble, save_track

WIN_SEC, HOP_SEC = 3.0, 3.0 

def convert_song(inp: Path, out: Path, k: int = 1):
    # Step 01 = Split stems of target song 
    stems = stem_splitter.split_stems(
        inp, model="mdx_extra_q", two_stem=True, make_acc=False
    )
    vocals_path      = stems / "vocals.wav"
    accompaniment_in = stems / "no_vocals.wav"

    # Step 02 = Segment original instrumental into windows
    seg_paths = segmenter.slice_stem(accompaniment_in, WIN_SEC, HOP_SEC)  
    extractor = EmbeddingExtractor()
    matcher   = Matcher(k=k)

    donor_segments = []
    for seg in tqdm(seg_paths, desc="Re-scoring target windows"):
        vec   = extractor(seg).numpy()
        best  = matcher.query(vec)[0]      # top-1 donor slice
        donor = adapt_slice(best, WIN_SEC)
        donor_segments.append(donor)

    # Step 03 = Stitch donors + save
    recast_acc = assemble(donor_segments)
    out_acc   = out.with_suffix(".acc.wav")
    save_track(recast_acc, out_acc)

    # Step 04 =  Re-attach target vocals
    v, sr = librosa.load(vocals_path, sr=DEFAULT_SR, mono=True)
    v = np.pad(v, (0, max(0, len(recast_acc) - len(v))))
    mix = v[: len(recast_acc)] + recast_acc
    save_track(mix, out)

    print(f"Saved {out.name}")
