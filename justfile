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
    docker.exe compose up -d

# Stop database
db_down:
    docker.exe compose down

# Run the program
run: db_up
    poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser
