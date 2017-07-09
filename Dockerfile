FROM ubuntu:16.04

RUN apt-get update && apt-get dist-upgrade -y

RUN apt-get update && apt-get install -y \
    python \
    python-pip

# Bust the docker cache if dependencies change
COPY requirements.txt /opt/flywheel/requirements.txt
WORKDIR /opt/flywheel
RUN pip install -r requirements.txt

# Copy in the rest of the files
COPY . /opt/flywheel

EXPOSE 8080

CMD ["/usr/bin/python", "/opt/flywheel/main.py"]
