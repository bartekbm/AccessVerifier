FROM python:3.12-slim

WORKDIR /app

COPY app.py ip_updater.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python ip_updater.py & python app.py"]
