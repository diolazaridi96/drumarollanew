import os
import requests

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "drums.pt")


def download_model_if_missing():
    """
    Проверяет наличие модели и скачивает её из Google Drive,
    если файла нет.
    """

    google_id = os.getenv("MODEL_ID")
    if not google_id:
        raise Exception("MODEL_ID variable not found! Add it in Railway → Variables.")

    # Создаём папку для модели, если её нет
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # Если модель уже скачана — выходим
    if os.path.isfile(MODEL_PATH):
        print("Model already exists. Skipping download.")
        return

    print("Downloading model from Google Drive...")
    download_file_from_google_drive(google_id, MODEL_PATH)


def download_file_from_google_drive(file_id: str, destination: str):
    """
    Скачивание файла большого размера из Google Drive.
    """

    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)

    # Проверка токена подтверждения
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value

    # Если есть токен, повторяем запрос с подтверждением
    if token:
        response = session.get(
            URL,
            params={"id": file_id, "confirm": token},
            stream=True
        )

    # Пишем файл
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    print(f"Model downloaded to {destination}")


