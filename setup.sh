#!/bin/bash
docker-compose build
docker-compose up -d
sleep 20 # give mysql container time to spin up db
docker exec -it reddit-recommender_reddit-mysql_1 /bin/bash -c \
'mysql -u root --password=password -e '\''CREATE USER "root"@"%" IDENTIFIED BY "password"; GRANT ALL PRIVILEGES ON *.* TO "root"@"%" WITH GRANT OPTION;'\'''
docker exec -it reddit-recommender_reddit-mysql_1 /bin/bash -c \
'mysql -u root --password=password < /tmp/sqlkomplett.sql'

echo "Done!"
