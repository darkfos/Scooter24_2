FROM python:3.10

WORKDIR /backend_scooter

COPY . /backend_scooter

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5678"]