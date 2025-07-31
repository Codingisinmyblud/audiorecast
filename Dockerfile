# ---- 1. base OS + python -----------------------------------------------------
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

# ---- 2. system libs Demucs & audio deps need ---------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg git build-essential libsndfile1-dev  && \
    rm -rf /var/lib/apt/lists/*

# ---- 3. install Poetry -------------------------------------------------------
RUN pip install "poetry==$POETRY_VERSION"

# ---- 4. copy project ---------------------------------------------------------
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --only main

# copy source after deps to leverage layer caching
COPY src/ /app/src/
COPY scripts/ /app/scripts/

# ---- 5. default entry --------------------------------------------------------
ENTRYPOINT ["python", "-m", "audiorecast.pipeline"]
# Usage example:
#   docker run --rm -v "$PWD/outputs":/app/outputs \
#        audiorecast /app/data/examples/song.mp3 /app/outputs/halal.wav
