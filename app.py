# ---- app.py ----
f.save(in_path)


# convert to WAV if needed using ffmpeg into a temp file (librosa can read mp3 but using ffmpeg ensures compatibility)
wav_path = os.path.join(UPLOAD_DIR, uid + '_conv.wav')
# Use ffmpeg -y -i input -ar 44100 -ac 2 wav_path
# Keep it simple and use soundfile/librosa load+save if format supported
try:
# Try to read and re-save as WAV to ensure consistent format
import soundfile as sf
data, sr = sf.read(in_path)
sf.write(wav_path, data, sr)
except Exception:
# fallback to ffmpeg
import subprocess
subprocess.run(["ffmpeg", "-y", "-i", in_path, "-ar", "44100", "-ac", "2", wav_path], check=True)


# extract drums (MDX-B)
drums_wav = os.path.join(OUTPUT_DIR, uid + '_drums.wav')
try:
extract_drums(wav_path, drums_wav)
except Exception as e:
return jsonify({"error": "drum extraction failed", "detail": str(e)}), 500


# get onsets
try:
onsets = get_onsets_seconds(drums_wav)
except Exception as e:
return jsonify({"error": "onset detection failed", "detail": str(e)}), 500


# cleanup intermediate files optionally (keep for debugging)
# os.remove(in_path); os.remove(wav_path); os.remove(drums_wav)


return jsonify({"status": "ok", "onsets": onsets})




@app.route('/')
def index():
return jsonify({"status": "drum-extractor ready"})




if __name__ == '__main__':
port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port)
