FROM mysql

WORKDIR /usr/src/app

# curl
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y unzip;

# Java
RUN mkdir -p /usr/share/man/man1 && \
    (echo "deb http://http.debian.net/debian stretch-backports main" > /etc/apt/sources.list.d/backports.list) && \
    apt-get update -y && \
    apt-get install -t stretch-backports openjdk-8-jdk -y

# Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

# Pentaho
ENV PDI_RELEASE=8.1 \
    PDI_VERSION=8.1.0.0-365 \
    PDI_HOME=/opt/pentaho-di \
    KETTLE_HOME=/pentaho-di

RUN cd /tmp && \
	curl -LO https://downloads.sourceforge.net/project/pentaho/Pentaho%208.1/client-tools/pdi-ce-8.1.0.0-365.zip && \
	unzip -q /tmp/pdi-ce-8.1.0.0-365.zip -d ~/8.1 && \
	rm /tmp/pdi-ce-8.1.0.0-365.zip && \
	cd ~

ENV PATH=$PDI_HOME/data-integration:$PATH

# Python
RUN apt-get update
RUN apt-get install -y python3-pip

#COPY api_scripts/requirements.txt ./
#RUN pip3 install --no-cache-dir -r requirements.txt