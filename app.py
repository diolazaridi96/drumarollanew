from flask import Flask, request, send_file, render_template
import torch
import torchaudio
import soundfile as sf
import os
from download_model import download_model_if_missing

# --- download model at runtime ---
download_model_if_missing()

MODEL_PATH = "model/drums.pt"
device = "cpu"

# --- load PyTorch model ---
print("Loading model...")
model = torch.load(MODEL_PATH, map_location=device)
model.eval()
print("Model loaded.")

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/separate", methods=["POST"])
def separate():
    if "audio" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio"]
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, "drums.wav")

    file.save(input_path)

    # Load audio
    wav, sr = torchaudio.load(input_path)
    wav = wav.mean(dim=0, keepdim=True).to(device)  # convert to mono

    # Inference
    with torch.no_grad():
        drums = model(wav)

    drums = drums.cpu().numpy().squeeze()

    # Save output
    sf.write(output_path, drums, sr)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

