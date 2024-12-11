FROM python:3.12-slim

WORKDIR /app

COPY app.py requirements.txt ./

RUN pip install -r requirements.txt

ENV IP_FILE=/app/allowed_ips.json
ENV FORWARDED_HEADER=X-Forwarded-For

CMD ["python", "app.py"]
