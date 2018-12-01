FROM mysql

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python3-pip

COPY api_scripts/requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt