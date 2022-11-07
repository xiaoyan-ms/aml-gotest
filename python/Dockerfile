
FROM mcr.microsoft.com/mirror/docker/library/python:3.9-buster

WORKDIR /usr/app/
COPY src ./src
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "flask", "--app", "./src/main", "run",  "--host", "0.0.0.0", "--port", "8000"]

