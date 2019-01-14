#!/bin/bash
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d
sleep 20 # give mysql container time to spin up db
docker exec -it docker_reddit-mysql_1 /bin/bash -c \
'mysql -u root --password=password -e '\''CREATE USER "root"@"%" IDENTIFIED BY "password"; GRANT ALL PRIVILEGES ON *.* TO "root"@"%" WITH GRANT OPTION;'\'''

echo "Done!"