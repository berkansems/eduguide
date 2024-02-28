FROM python:3.8-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
