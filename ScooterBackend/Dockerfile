FROM python:3.12

WORKDIR /backend_scooter

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /backend_scooter

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3, "main.py"]
