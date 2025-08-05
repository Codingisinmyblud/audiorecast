# for reference: scripts/update_faiss_index.py
# to run: poetry run python scripts/update_faiss_index.py

from audiorecast.matching.index_updater import update_index

if __name__ == "__main__":
    update_index()
