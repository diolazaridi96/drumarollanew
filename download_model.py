import os
import requests

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "drums.pt")

GOOGLE_ID = os.environ.get("MODEL_ID")

if GOOGLE_ID is None:
    raise Exception("MODEL_ID variable not found! Set it in Railway → Variables.")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

def download_file_from_google_drive(file_id, destination):
    print("Downloading model from Google Drive...")

    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={"id": file_id}, stream=True)

    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value

    if token:
        response = session.get(URL, params={"id": file_id, "confirm": token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    print(f"Model downloaded to {destination}")


if not os.path.isfile(MODEL_PATH):
    download_file_from_google_drive(GOOGLE_ID, MODEL_PATH)
else:
    print("Model already exists. Skipping download.")

