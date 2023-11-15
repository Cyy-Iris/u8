.PHONY: airflow_docker

include .env
export $(sed 's/=.*//' .env)


airflow_docker:
	docker compose --project-directory ./ -f ./services/airflow/docker-compose.yaml up --build -d

airflow_standalone:
	poetry run airflow standalone