FROM python:3.9-alpine

# Dentro del contenedor el directorio "/app" pasa a ser el directorio de trabajo.
WORKDIR /app
COPY ./requirements.txt /app

# Instalamos dependencias para que funcione la librería "cffi" y finalmente instalamos los requirements.
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo
RUN pip install -r requirements.txt

CMD ["flask", "run"]
