.PHONY: install test migrate run-api run-dashboard up down lint

install:
	pip install -r requirements.txt

test:
	pytest --cov=backend --cov=analytics tests/

migrate:
	cd backend && alembic upgrade head

run-api:
	uvicorn backend.app.main:app --reload

run-dashboard:
	streamlit run dashboard/app.py

up:
	docker compose -f infra/docker/docker-compose.yml up -d

down:
	docker compose -f infra/docker/docker-compose.yml down

lint:
	ruff check .
	black --check .
