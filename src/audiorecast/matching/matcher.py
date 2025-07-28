# Loads the FAISS index and paths and returns the top-k slice filenames.

from pathlib import Path
import json, faiss, numpy as np

EMB_DIR = Path("data/embeddings")

class Matcher:
    def __init__(self, k: int = 5):
        self.k = k
        self.index = faiss.read_index(str(EMB_DIR / "slice_index.faiss"))
        self.paths = [json.loads(l)["path"] for l in (EMB_DIR / "paths.jsonl").read_text().splitlines()]

    def query(self, vec: np.ndarray) -> list[str]:
        vec = vec.astype("float32")[None, :]  # shape (1, D)
        _, idx = self.index.search(vec, self.k)
        return [self.paths[i] for i in idx[0]]
