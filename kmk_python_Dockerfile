FROM python:3.9-slim-buster

ARG KMKPY_REF
ARG KMKPY_URL

ENV KMKPY_REF ${KMKPY_REF}
ENV KMKPY_URL ${KMKPY_URL}

RUN mkdir -p /app /dist
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl gettext git git-lfs rsync wget zip lbzip2
RUN pip install pipenv

# Pull CircuitPython-designated ARM GCC to avoid mismatches/weird
# inconsistencies with upstream
RUN curl -L -o /tmp/gcc-arm.tar.bz2 https://adafruit-circuit-python.s3.amazonaws.com/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2 && \
	tar -C /usr --strip-components=1 -xaf /tmp/gcc-arm.tar.bz2 && \
	rm -rf /tmp/gcc-arm.tar.bz2

# Get a local copy of KMKPython and its dependencies. We don't provide MPY
# builds for kmkpython anymore, so we can get away with being opinionated
# here.
RUN git init /opt/kmkpython && \
	git -C /opt/kmkpython remote add origin ${KMKPY_URL} && \
	git -C /opt/kmkpython fetch --depth 1 origin ${KMKPY_REF} && \
	git -C /opt/kmkpython checkout FETCH_HEAD && \
	git -C /opt/kmkpython submodule update --init --recursive

# Build the MPY compiler
RUN make -C /opt/kmkpython/mpy-cross

ENV PATH=/opt/kmkpython/mpy-cross:${PATH}

RUN mkdir -p /opt/kmkpython/frozen/kmk/kmk
COPY ./build_kmkpython_release.sh /app/
COPY ./kmk /opt/kmkpython/frozen/kmk/kmk

CMD /app/build_kmkpython_release.sh
