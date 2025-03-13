SHELL := /usr/bin/env bash
STAGE ?= local

.DEFAULT_GOAL := all
.PHONY: all

all: format test deploy

test: test-format test-quality test-unit

deploy: clean package terraform-apply

install:
	@if command -v pyenv >/dev/null 2>&1; then \
		echo "pyenv is installed. Setting up Python 3.12..."; \
		if ! pyenv versions --bare | grep -q 3.12; then \
			echo "Python 3.12 not found. Installing..."; \
			pyenv install; \
		else \
			echo "Python 3.12 already installed."; \
		fi; \
		pyenv local; \
	else \
		PYTHON_VERSION=$$(python3 --version 2>/dev/null | grep -o '3.12.*' || echo ""); \
		if [[ "$$PYTHON_VERSION" = "3.12"* ]]; then \
			echo "Python version 3.12 is installed. pyenv will not be used."; \
		else \
			echo "Neither pyenv is installed nor is Python version 3.12 available. Build aborted."; \
			echo "Installed Python version: $$PYTHON_VERSION"; \
			exit 1; \
		fi; \
	fi
	poetry config virtualenvs.in-project true
	poetry self add poetry-plugin-export
	poetry self add poetry-plugin-shell
	poetry self add poetry-plugin-up
	poetry self update
	poetry install --with dev

update:
	poetry update --with dev,central_reporting_lambda --latest

clear-poetry-cache:
	poetry env remove --all
	poetry cache clear pypi --all

format:
	# find . -name "*.tf" -not -path "*.terraform*" | xargs -r terraform fmt
	-poetry run docformatter --config pyproject.toml .
	poetry run autoflake --in-place --recursive --remove-all-unused-imports .
	poetry run isort . --profile black
	poetry run black .

test-format:
	find . -name "*.sh" | xargs -r shellcheck
	# find . -name "*.tf" -not -path "*.terraform*" | xargs -r terraform fmt -check
	poetry run docformatter --config pyproject.toml --check .
	poetry run autoflake --recursive --check .
	poetry run isort . --check-only --profile black
	poetry run black . --check

test-quality:
	poetry run bandit -r bookworm
	poetry run bandit -r tests
	poetry run pylint --rcfile pyproject.toml bookworm
	poetry run pylint --rcfile pyproject.toml tests

test-unit:
	poetry run pytest tests/unit --disable-pytest-warnings

