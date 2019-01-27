#!/bin/bash
docker-compose build
docker-compose up -d
sleep 20 # give mysql container time to spin up db
docker exec -it reddit-recommender-mysql /bin/bash -c \
'mysql -u root --password=password -e '\''CREATE USER "root"@"%" IDENTIFIED BY "password"; GRANT ALL PRIVILEGES ON *.* TO "root"@"%" WITH GRANT OPTION;'\'''
docker exec -it reddit-recommender-mysql /bin/bash -c \
'mysql -u root -ppassword < /tmp/sqlkomplett.sql'
docker exec -it reddit-recommender-mysql /bin/bash -c \
'mysql -u root -ppassword reddit_recommender < /tmp/subredditsBigger5.sql'
docker stop reddit-recommender-flask
docker stop reddit-recommender-pdi
docker stop reddit-recommender-mysql

echo "Done!"
