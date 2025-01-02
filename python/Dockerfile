FROM python:3.10

# Installiere Systemabhängigkeiten
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libpq-dev \
    python3-dev \
    libffi-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*
# Setze Arbeitsverzeichnis
WORKDIR /app
# Kopiere requirements.txt und installiere Abhängigkeiten
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung
COPY . /app/

RUN pip install python-multipart
RUN pip install uvicorn
# Install vLLM from pip:
# Exponiere Port für Whisper (falls nötig, z. B. über FastAPI/Flask)
EXPOSE 8000

# Standard-Kommando: Bash
#CMD ["bash", "-c", "python myproject/app.py"  ]
#CMD ["bash", "-c", "uvicorn app:app --reload"  ]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
#CMD ["tail", "-f", "/dev/null"]