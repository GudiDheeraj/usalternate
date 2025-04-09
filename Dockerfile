FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r deployment_requirements.txt

ENV PORT=5000
ENV PYTHONUNBUFFERED=1

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT --reuse-port main:app