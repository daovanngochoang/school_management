FROM python:3.9
LABEL authors="andreas"
WORKDIR app
COPY . .
RUN apt-get update
RUN apt-get install build-essential cargo -y
RUN pip install -r requirement.txt
CMD ["python", "./main.py"]