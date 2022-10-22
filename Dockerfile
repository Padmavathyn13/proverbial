FROM python:3.9.14-slim
WORKDIR /application
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . .
CMD [ "python", "./Proverbial_collection.py"]