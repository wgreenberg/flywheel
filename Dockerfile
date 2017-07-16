FROM krallin/ubuntu-tini:xenial

# Upgrade packages, setup java repo
RUN apt-get update && \
    apt-get dist-upgrade -y

# Install our dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip

# Bust the docker cache if dependencies change
COPY requirements.txt /opt/flywheel/requirements.txt
WORKDIR /opt/flywheel
RUN pip3 install -r requirements.txt

RUN python3 -m nltk.downloader punkt

# Copy in the rest of the files
COPY . /opt/flywheel

# Python server
EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/tini", "-g", "--"]
CMD ["/opt/flywheel/run.sh"]
