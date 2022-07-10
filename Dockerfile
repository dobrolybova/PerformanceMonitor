FROM python:latest

WORKDIR /WebServer

COPY requirements.txt ./
COPY README.md ./

run pip install --no-cache-dir -r requirements.txt
run pip install gunicorn

COPY ./src ./src

CMD ["python3", "src/main.py"]