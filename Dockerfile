FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -e .