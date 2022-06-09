FROM python:3.8-slim-buster
WORKDIR /app
RUN apt update && apt install -y build-essential
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python3", "main.py"]