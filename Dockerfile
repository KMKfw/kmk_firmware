FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN apk update && apk add alpine-sdk coreutils curl gettext git git-lfs openssh rsync wget zip

RUN pip install pipenv

### Get a local copy of CircuitPython and its dependencies
# Our absolute baseline is 4.0.0, which (as of writing) shares MPY compat
# with all future versions. Our baseline will need to update as MPY compat
# changes
RUN git clone --branch 4.0.0 --depth 1 https://github.com/adafruit/CircuitPython /opt/circuitpython
RUN git -C /opt/circuitpython submodule update --init

### Build the MPY compiler
RUN make -C /opt/circuitpython/mpy-cross

ENV PATH=/opt/circuitpython/mpy-cross:${PATH}
