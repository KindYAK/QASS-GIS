docker compose stop front
docker compose rm front
docker compose stop nginx
docker compose rm nginx
docker volume rm qass_front
docker compose up -d --build front nginx
