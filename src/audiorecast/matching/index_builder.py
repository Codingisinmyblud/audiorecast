# Scans the slices folder and builds (embeddings.npy, paths.jsonl, faiss.index)

from pathlib import Path
import json, faiss, numpy as np
from tqdm import tqdm
from audiorecast.embedding.extractor import EmbeddingExtractor

SLICE_ROOT = Path("data/raw")  # parent of all YT IDs
EMB_DIR = Path("data/embeddings")
EMB_DIR.mkdir(parents=True, exist_ok=True)

def gather_slice_paths() -> list[Path]:
    return sorted(SLICE_ROOT.glob("*/**/slices/*.wav"))

def run():
    extractor = EmbeddingExtractor()
    vecs, paths = [], []

    for p in tqdm(gather_slice_paths(), desc="Embedding slices"):
        vecs.append(extractor(p).numpy())
        paths.append(str(p))

    vecs = np.stack(vecs).astype("float32")
    np.save(EMB_DIR / "embeddings.npy", vecs)

    with open(EMB_DIR / "paths.jsonl", "w") as f:
        f.writelines(json.dumps({"path": p}) + "\n" for p in paths)

    index = faiss.IndexFlatL2(vecs.shape[1])        # exact k-NN (small dataset)
    index.add(vecs)
    faiss.write_index(index, str(EMB_DIR / "slice_index.faiss"))

if __name__ == "__main__":
    run()
