FROM python:3.12.5-slim
COPY src/ /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR app/
