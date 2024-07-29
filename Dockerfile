FROM python:3.9-slim-bullseye

RUN \
 apt-get update && \
 apt-get -y upgrade &&\
 apt-get -y install libpq-dev gcc

RUN pip3 install --upgrade pip

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=postgres://postgres:1@host.docker.internal:5432/gispik

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "testproj.wsgi"]