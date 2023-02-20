FROM python:3.9-slim-buster

RUN mkdir -p /app /dist
WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN curl https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/linux-amd64/mpy-cross.static-amd64-linux-8.0.0 --output mpy-cross-8
RUN curl https://adafruit-circuit-python.s3.amazonaws.com/bin/mpy-cross/linux-amd64/mpy-cross.static-amd64-linux-7.0.0 --output mpy-cross-7


RUN chmod +x mpy-cross-8

RUN chmod +x mpy-cross-7


COPY ./docker_mpy_build.sh /app/build.sh
# COPY ./kmk /app/kmk/

CMD ["bash", "build.sh"]
