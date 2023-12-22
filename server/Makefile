DC := $(if $(shell command -v docker-compose 2> /dev/null),docker-compose,docker compose)
D = docker

DC_DEV_FILE = docker-compose-dev.yml


down: 
	$(DC) down
clean: down
	$(D) volume rm server_collector-tool server_opensearch-data1 server_opensearch-data2

up:
	$(DC) up

dev-down: 
	$(DC) -f $(DC_DEV_FILE) down
dev-clean: dev-down
	$(D) volume rm server_collector-tool server_opensearch-data1 server_opensearch-data2

dev-up:
	$(DC) -f $(DC_DEV_FILE) up