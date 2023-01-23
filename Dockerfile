FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000
CMD ["python", "main.py"]
