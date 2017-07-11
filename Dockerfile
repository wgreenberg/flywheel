FROM krallin/ubuntu-tini:xenial

# Upgrade packages, setup java repo
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y software-properties-common python-software-properties && \
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
    add-apt-repository -y ppa:webupd8team/java

# Install our dependencies
RUN apt-get update && apt-get install -y \
    oracle-java8-installer \
    python3 \
    python3-pip \
    unzip

RUN pip3 install --upgrade pip

# Install Gremlin
RUN wget http://mirrors.advancedhosters.com/apache/tinkerpop/3.2.5/apache-tinkerpop-gremlin-server-3.2.5-bin.zip
RUN unzip apache-tinkerpop-gremlin-server-3.2.5-bin.zip && \
    mv apache-tinkerpop-gremlin-server-3.2.5 /opt/gremlin-server

# Bust the docker cache if dependencies change
COPY requirements.txt /opt/flywheel/requirements.txt
WORKDIR /opt/flywheel
RUN pip3 install -r requirements.txt

RUN python3 -m nltk.downloader punkt

# Copy in the rest of the files
COPY . /opt/flywheel

# Python server
EXPOSE 5000
# Gremlin server
EXPOSE 8182

ENTRYPOINT ["/usr/local/bin/tini", "-g", "--"]
CMD ["/opt/flywheel/run.sh"]
