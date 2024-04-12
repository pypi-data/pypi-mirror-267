FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt clean && apt update && \
    apt install --no-install-recommends --assume-yes \
    wget \
    python3-pip \
    python3-matplotlib \
    python3-pandas \
    python3-statsmodels \
    python3-sklearn \
    python3-pysam \
    python3-venv

WORKDIR /opt/

RUN pip3 install --break-system-packages --no-dependencies SigProfilerPlotting
RUN pip3 install --break-system-packages --no-dependencies SigProfilerMatrixGenerator


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Install `GRCh37`, may take a long time!
RUN python3 -c 'from SigProfilerMatrixGenerator import install; install.install("GRCh37", rsync=False, bash=True)'
RUN pip3 install --break-system-packages vcfpy

RUN pip3 install --break-system-packages build
COPY . /opt/bearclaw/
WORKDIR /opt/bearclaw/
RUN python3 -m build
RUN pip3 install --break-system-packages .

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
