.PHONY: start stop build

start:
	docker compose up --build

stop:
	docker compose down

build:
	docker compose build
