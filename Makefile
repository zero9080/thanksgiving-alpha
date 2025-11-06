.PHONY: setup lint fix test run
setup:
	poetry install
lint:
	poetry run ruff check . && poetry run black --check . && poetry run mypy src
fix:
	poetry run ruff check . --fix && poetry run black .
test:
	poetry run pytest -q --maxfail=1
run:
	poetry run tgalpha run --config configs/example_djia.yaml --top 20
