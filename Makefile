.PHONY: help sync format format-check lint tests

help:
	@echo "Targets: sync format format-check lint tests"

sync:
	uv sync

format:
	uv run ruff format
	uv run ruff check --fix

format-check:
	uv run ruff format --check

lint:
	uv run ruff check

tests:
	uv run pytest