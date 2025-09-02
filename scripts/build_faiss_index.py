# for reference: audiorecast/scripts/build_faiss_index.py
# to run: poetry run python audiorecast/scripts/build_faiss_index.py

from audiorecast.matching.index_builder import run

if __name__ == "__main__":
    run()
