FROM python:3.12-slim

WORKDIR /app

COPY app.py ip_updater.py requirements.txt ./

RUN pip install -r requirements.txt

# Environment variables
ENV IP_FILE=/app/allowed_ips.json
ENV AWS_REGION=eu-west-1
ENV PORT=5000
ENV FORWARDED_HEADER=X-Forwarded-For

CMD ["sh", "-c", "python ip_updater.py & python app.py"]