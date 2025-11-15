# ---- Dockerfile ----
# Lightweight Dockerfile tuned for Railway trial (1 GB)
FROM python:3.10-slim


WORKDIR /app


# system deps: ffmpeg and libsndfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --upgrade pip \
&& pip install -r requirements.txt


COPY . ./


ENV PORT=8000
EXPOSE ${PORT}


# Use simple entrypoint for Railway (it injects PORT env)
CMD ["python", "app.py"]
