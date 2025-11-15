# ---- README.md ----
# Drum Extractor (Railway trial friendly)


This minimal service extracts drum stem using UVR5 MDX-B and returns onset timestamps (in seconds) as JSON.


## Quickstart
1. Build image locally:
```bash
docker build -t drum-extractor .
```
2. Run locally (for testing):
```bash
docker run --rm -p 8000:8000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/outputs:/app/outputs drum-extractor
```
3. Test with curl:
```bash
curl -X POST http://localhost:8000/drums/beatmap -F "file=@/path/to/song.mp3"
```


## Deploy to Railway
- Create new project in Railway and connect this repo (or push Dockerfile). Railway will detect `Dockerfile` and build.
- For trial, set plan to Hobby (use $5 credit). Ensure service has ~1GB available.
- Railway will expose `PORT` env var automatically.




# ---- NOTES & TIPS ----
- This implementation uses a lazy-loaded MDX model (MDX-B). The first request may be slower while the model downloads/initializes.
- If you need to return quantized beatmaps or MIDI, extend `beatmap.py` to quantize onsets using estimated BPM.
- Keep an eye on memory usage during first runs; if you face OOM on Railway, consider switching to a slightly smaller MDX variant (mdx-drum) or use a warm-up endpoint.


# End of canvas file
