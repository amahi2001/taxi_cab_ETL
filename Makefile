.ONESHELL:
.DEFAULT_GOAL := run

init-poetry:
	rm -rf env venv .venv
	poetry config virtualenvs.in-project true --local
	poetry config virtualenvs.prefer-active-python true --local
	poetry install
	poetry update
	${MAKE} freeze

#* Format the codebase with Ruff
format:
	poetry run ruff check --select I --fix .
	poetry run ruff format .

#* Create/update a requirements.txt file
freeze:
	poetry export -f requirements.txt --output requirements.txt
