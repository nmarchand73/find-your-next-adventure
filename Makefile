.PHONY: help install install-dev test test-cov lint format type-check clean build run
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
	@echo "Cleaning build artifacts..."
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@if exist *.egg-info rmdir /s /q *.egg-info
	@if exist htmlcov rmdir /s /q htmlcov
	@if exist .coverage del .coverage
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .mypy_cache rmdir /s /q .mypy_cache
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"

build: clean ## Build package
	python -m build

run: ## Run the parser with sample PDF
	python run.py

run-custom: ## Run the parser with custom PDF (usage: make run-custom PDF=myfile.pdf OUTPUT=./output/)
	python run.py "$(PDF)" "$(OUTPUT)"

setup-dev: ## Set up development environment
	pip install -e ".[dev]"
	@echo "Development environment set up successfully!"
