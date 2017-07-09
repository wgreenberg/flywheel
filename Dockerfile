FROM ubuntu:16.04

RUN apt-get update && apt-get dist-upgrade -y

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip

# Bust the docker cache if dependencies change
COPY requirements.txt /opt/flywheel/requirements.txt
WORKDIR /opt/flywheel
RUN pip3 install -r requirements.txt

# Copy in the rest of the files
COPY . /opt/flywheel

EXPOSE 8080

CMD ["/usr/bin/python3", "/opt/flywheel/main.py"]
