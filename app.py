import os
from flask import Flask, request, send_file, jsonify, render_template_string
import torch
import torchaudio
import tempfile

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/input"
OUTPUT_FOLDER = "/tmp/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTML-форма для загрузки аудио
HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Drums Extractor</title>
</head>
<body>
    <h2>Загрузите аудио для выделения ударных</h2>
    <form action="/separate" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="audio/*" required>
        <input type="submit" value="Отделить барабаны">
    </form>
</body>
</html>
"""

model = None  # lazy loading

def get_model():
    global model
    if model is None:
        print("Loading drums model...")
        model = torch.jit.load("model/drums.pt", map_location="cpu")
        model.eval()
        print("Model loaded")
    return model

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/separate", methods=["POST"])
def separate_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Генерация выходного файла
    output_dir = os.path.join(OUTPUT_FOLDER, os.path.splitext(file.filename)[0])
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "drums.wav")

    # Загружаем модель
    model = get_model()

    # Загружаем аудио
    waveform, sr = torchaudio.load(input_path)

    # Простейший forward через модель (для drums-only модели)
    with torch.no_grad():
        separated = model(waveform)  # возвращает только барабаны
        # если выход tuple, берем первый элемент
        if isinstance(separated, (list, tuple)):
            separated = separated[0]
        torchaudio.save(output_path, separated.cpu(), sr)

    if not os.path.exists(output_path):
        return jsonify({"error": "Failed to separate"}), 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port)
