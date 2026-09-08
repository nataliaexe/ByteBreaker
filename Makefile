.PHONY: help install test lint format clean run docker

help:
	@echo "ByteBreaker Commands:"
	@echo "  make install    Install dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linters"
	@echo "  make format     Format code"
	@echo "  make clean      Clean up"
	@echo "  make run        Run CLI"
	@echo "  make docker     Build Docker image"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=./ --cov-report=html

lint:
	black --check .
	mypy core modules utils cli api
	bandit -r .

format:
	black .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov

run:
	python cli/main.py --help

docker:
	docker build -t bytebreaker:latest .

docker-run:
	docker run -it --rm bytebreaker:latest
