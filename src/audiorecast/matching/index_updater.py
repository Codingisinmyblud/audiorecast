from pathlib import Path
import json, numpy as np, faiss
from tqdm import tqdm
from audiorecast.embedding.extractor import EmbeddingExtractor

EMB_DIR    = Path("data/embeddings")
SLICE_ROOT = Path("data/raw")

def update_index(k=1):
    # STEP 01: this loads existing stuff
    emb_path  = EMB_DIR / "embeddings.npy"
    paths_path= EMB_DIR / "paths.jsonl"
    idx_path  = EMB_DIR / "slice_index.faiss"

    existing_vecs  = np.load(emb_path)               
    existing_paths = [json.loads(l)["path"] 
                        for l in paths_path.read_text().splitlines()]

    # STEP 02: this find new slices
    all_slices = sorted(str(p) 
                      for p in SLICE_ROOT.glob("*/**/slices/*.wav"))
    new_paths  = [p for p in all_slices if p not in existing_paths]
    if not new_paths:
        print("No new slices to index.")
        return

    # STEP 03: this embeds new slices
    extractor = EmbeddingExtractor()
    new_vecs  = []
    for p in tqdm(new_paths, desc="Embedding new slices"):
        new_vecs.append(extractor(Path(p)).numpy())
    new_vecs = np.stack(new_vecs).astype("float32")

    # STEP 04: this appends to numpy + paths file
    all_vecs = np.vstack([existing_vecs, new_vecs])
    np.save(emb_path, all_vecs)
    with open(paths_path, "a") as f:
        for p in new_paths:
            f.write(json.dumps({"path": p}) + "\n")

    # STEP 05: this updates FAISS
    index = faiss.read_index(str(idx_path))
    index.add(new_vecs)
    faiss.write_index(index, str(idx_path))

    print(f"Added {len(new_paths)} slices to index.")
