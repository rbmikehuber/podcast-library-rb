FROM python:3.10-slim-buster

ENV PORT=8080

WORKDIR /usr/src/app

COPY * ./

RUN apt-get update
RUN apt-get -y install ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
