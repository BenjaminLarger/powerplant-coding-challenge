SHELL	= /bin/sh

NAME	= powerplant

# Variables
APP_URL = http://localhost:8888/productionplan
PAYLOAD_FILE = ./utils/payload1.json

send-request:
	curl -X POST $(APP_URL) -H "Content-Type: application/json" -d @$(PAYLOAD_FILE)

all:
	cd srcs && docker compose up --build

down:
	cd srcs && docker compose down -v
stop:
	cd srcs && docker compose stop
logs:
	cd srcs && docker-compose logs -f
prune:
	docker image prune
routine:
	docker system prune -a
reset:
	docker stop $$(docker ps -qa); \
	docker rm $$(docker ps -qa); \
	docker rmi -f $$(docker images -qa); \
	docker volume rm $$(docker volume ls -q); \
	docker network rm $$(docker network ls -q) 2>/dev/null

