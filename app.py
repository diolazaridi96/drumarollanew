from flask import Flask, request, send_file, jsonify, render_template_string
import torch
import torchaudio
import os

app = Flask(__name__)

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "drums.pt")

UPLOAD_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTML-страница для браузера
HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Drums Splitter</title>
</head>
<body>
<h2>Загрузите аудио для выделения ударных</h2>
<form action="/separate" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept="audio/*" required>
    <input type="submit" value="Выделить ударные">
</form>
</body>
</html>
"""

# Загрузка модели с логами
model = None
try:
    print("Checking for model at:", MODEL_PATH)
    if os.path.isfile(MODEL_PATH):
        print("Loading model...")
        model = torch.jit.load(MODEL_PATH, map_location="cpu")
        model.eval()
        print("Model loaded successfully")
    else:
        print("Model file not found. Please place drums.pt in the 'model/' folder.")
except Exception as e:
    print("Error loading model:", e)

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/separate", methods=["POST"])
def separate_audio():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0] + "_drums.wav")
    file.save(input_path)

    try:
        print(f"Processing {input_path}...")
        waveform, sr = torchaudio.load(input_path)

        # Мини-модель выделяет только ударные
        with torch.no_grad():
            drums = model(waveform.unsqueeze(0))  # [1, 1, samples]

        torchaudio.save(output_path, drums.squeeze(0), sr)
        print(f"Saved drums to {output_path}")

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        print("Error during separation:", e)
        return jsonify({"error": "Failed to separate audio", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port)


