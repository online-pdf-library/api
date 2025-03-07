APP_NAME=api

# Generate help info from comments, source - https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Help information about make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONE: clean
clean: ## Deletes __pycache__ directories
	@uv run python -Bc "import pathlib; import shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

.PHONY: build
build: ## Build docker image
	@docker build -f ./deployments/Dockerfile . -t ${APP_NAME}
	@docker tag ${APP_NAME} ${APP_NAME}:latest

.PHONY: up
up: ## Start all docker containers
	@docker compose -f deployments/local/compose.yaml -p ${APP_NAME} up --build -d

.PHONY: down
down: ## Stop all docker containers
	@docker compose -f deployments/local/compose.yaml -p ${APP_NAME} down

.PHONY: rebuild
rebuild: ## Rebuild docker image and restart all docker containers
	make down
	make build
	make up

.PHONY: sh
sh: ## Open shell for specified container
	@read -p "Enter a container name: " container; \
	docker compose -f deployments/local/compose.yaml -p ${APP_NAME} exec $$container sh

.PHONY: logs
logs: ## Show logs for specified container
	@read -p "Enter a container name: " container; \
	docker compose -f deployments/local/compose.yaml -p ${APP_NAME} logs $$container -f

.PHONY: generate_migration
generate_migration: ## Generate a migration
	@read -p "Enter a migration name: " migration; \
	docker compose -f deployments/local/compose.yaml -p ${APP_NAME} exec ${APP_NAME} alembic revision --autogenerate -m "$$migration"

.PHONY: migrate
migrate: ## Apply all migrations
	@docker compose -f deployments/local/compose.yaml -p ${APP_NAME} exec ${APP_NAME} alembic upgrade head

.PHONY: test
test: ## Run all tests
	PYTHONDONTWRITEBYTECODE=1 pytest -v

.PHONY: cov
cov: ## Run all tests and produce coverage report
	PYTHONDONTWRITEBYTECODE=1 pytest -v --cov=api
