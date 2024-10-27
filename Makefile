.PHONY: lint
lint: ## Run linters
	isort .
	flake8
	mypy .


.PHONY: run-dev
run-dev: ## Run backend on development
	uvicorn run:app --port 8500 --reload 

	
.PHONY: run-prod
run-prod: ## Run backend on production
	gunicorn run:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8500


.PHONY: migrate-up
migrate-up: ## Run migrations
	alembic revision --autogenerate -m "never" && alembic upgrade head


.PHONY: push
push: ## push commit to repository
	git -c http.sslVerify=false push origin


.PHONY: docker-run
docker-run:
	docker-compose -f docker-compose.yaml up -d