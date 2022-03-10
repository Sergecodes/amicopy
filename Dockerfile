# syntax=docker/dockerfile:1

FROM python:3.10.2-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
