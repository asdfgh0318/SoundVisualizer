# SoundVisualizer — single-image demo build.
# UI + fake-capture only; no hardware passthrough. Open http://localhost:8000.
#
# Build:    docker build -t soundvisualizer .
# Run:      docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data soundvisualizer
# (or:      docker compose up)

# --- Stage 1: build the React bundle ------------------------------------
FROM node:22-alpine AS frontend-build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --silent

COPY tsconfig*.json vite.config.ts eslint.config.js index.html ./
COPY src ./src

# Empty VITE_API_BASE -> same-origin fetch in the bundle.
ENV VITE_API_BASE=""
RUN npm run build

# --- Stage 2: server + bundled frontend ---------------------------------
FROM python:3.12-slim AS runtime
WORKDIR /app

# libportaudio2 is needed at import time by `sounddevice` (transitive dep of
# mosqito). The runtime image never actually opens an audio device — the demo
# only uses the synthetic /dev/fake_capture path.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libportaudio2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps via the project pyproject (editable so server/ stays
# importable as a package).
COPY pyproject.toml ./
COPY server ./server
RUN pip install --no-cache-dir -e . --quiet

# Bundle the built frontend
COPY --from=frontend-build /app/dist /app/static
ENV SOUNDVIS_STATIC=/app/static

# Demo mode — Tyto stays disabled. Frequent commands like /dev/seed and
# /dev/fake_capture work without any config edits.
COPY config.example.toml /app/config.toml

EXPOSE 8000
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
