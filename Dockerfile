# Используем лёгкий образ Python
FROM python:3.10-slim

WORKDIR /app

# Ставим системные зависимости для soundfile
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements (без torch/torchaudio)
COPY requirements.txt .

# Устанавливаем PyTorch CPU заранее, чтобы ускорить сборку
RUN pip install --no-cache-dir torch==2.1.0+cpu torchaudio==2.1.0+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Ставим остальные зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Порт для Railway
ENV PORT=5000

# Запуск
CMD ["python", "app.py"]

