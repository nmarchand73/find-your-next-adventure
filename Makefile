.PHONY: help install install-dev test test-cov lint format type-check clean build docs
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=find_your_next_adventure --cov-report=html --cov-report=term-missing

test-fast: ## Run tests excluding slow tests
	pytest -m "not slow"

lint: ## Run linting
	flake8 find_your_next_adventure tests

format: ## Format code
	black find_your_next_adventure tests
	isort find_your_next_adventure tests

format-check: ## Check code formatting
	black --check find_your_next_adventure tests
	isort --check-only find_your_next_adventure tests

type-check: ## Run type checking
	mypy find_your_next_adventure

check: format-check lint type-check test ## Run all checks

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	python -m build

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

run-example: ## Run example with sample data
	python pdf_to_json_parser.py "Find Your Next Adventure.pdf" "./output/"

pre-commit: format lint type-check test ## Run pre-commit checks

release-check: clean build ## Check package is ready for release
	python -m twine check dist/*

.PHONY: setup-dev
setup-dev: ## Set up development environment
	pip install -e ".[dev]"
	pre-commit install
	@echo "Development environment set up successfully!"
