FROM python:3.12.5-slim
COPY src/ /app/
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR app/
CMD ["python", "-u", "main.py"]
