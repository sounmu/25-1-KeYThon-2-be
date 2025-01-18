FROM python:3.10

WORKDIR /app/src

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]