# pull official base image
FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
# prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Exposez le port sur lequel le serveur FastAPI écoute
EXPOSE 8000

# Démarrez l'application FastAPI lorsque le conteneur est exécuté
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]