# Setup poetry
setup:
	poetry config virtualenvs.create true --local
	poetry config virtualenvs.in-project true --local

# Install dependencies
install: setup
	poetry install --no-root
	poetry run pre-commit install
	poetry run pip install django-admin-honeypot-updated-2021

# Update configuration files
update:
	poetry update
	poetry run pip3 freeze > requirements.txt

# Lint files
lint:
	poetry run pre-commit run --all-files

# Initiate database with docker
db_up:
    docker compose -f docker-compose.dev.yml up -d

# Stop database
db_down:
    docker compose -f docker-compose.dev.yml down

# Run the program
run: db_up
    poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser

# Run tests
test:
	poetry run pytest -v -rs -n auto --show-capture=no

# Run tests with markers
test_marker MARKER:
	poetry run pytest -v -rs -n auto --show-capture=no -m {{MARKER}}

# Run tests with coverage
coverage:
	poetry run pytest -v -rs -n auto --show-capture=no --cov --cov-report=term --cov-fail-under=100

# Check the coverage of the tests and export to html
coverage_html:
	poetry run pytest -v -rs -n auto --show-capture=no --cov --cov-report=html:htmlcov --cov-report=term --cov-fail-under=100
