FROM python:3.8-slim-buster

EXPOSE 8503

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /main

COPY . /main

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8503", "--server.address=0.0.0.0"]