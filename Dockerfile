# La copia oficial que Docker publica en ECR Public: Docker Hub limita las
# descargas sin cuenta por IP, y un servidor que comparte IP se queda sin
# cupo (429 Too Many Requests).
FROM public.ecr.aws/docker/library/python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER nobody
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
