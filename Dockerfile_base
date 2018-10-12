# vim: ft=dockerfile

# Not using python:3.7 here because team-gcc-arm-embedded/ppa does not support
# Ubuntu Cosmic or Debian Stretch, and Alpine, bizarrely, does not seem to
# package GCC cross compilers
FROM ubuntu:bionic

# Set up PPAs we'll need for Python and for GCC ARM
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN add-apt-repository ppa:team-gcc-arm-embedded/ppa

# Install Python
RUN apt-get update && apt-get install -y python3.7 python3.7-dev build-essential pkg-config libffi-dev curl
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.7
# Downgrade pip to work around https://github.com/pypa/pipenv/issues/2924
RUN python3.7 -m pip install pip==18.0
RUN python3.7 -m pip install pipenv==2018.7.1

# Install KMK CI and/or build-time dependencies
RUN apt-get install -y gcc-arm-embedded gettext ssh wget unzip rsync git locales libusb-dev
