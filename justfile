# Setup poetry
setup:
	poetry config virtualenvs.create true --local
	poetry config virtualenvs.in-project true --local

# Install dependencies
install: setup
	poetry install --no-root
	poetry run pip install 'transformers[torch]'
	poetry run pre-commit install

# Update configuration files
update:
	poetry update
	poetry run pip3 freeze > requirements.txt

# Lint files
lint:
	poetry run pre-commit run --all-files

# Run the program
run: run_analysis run_examination

run_analysis:
    poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser

run_examination:
    poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_examination

# Run tests
test:
	poetry run pytest -v -rs -n auto --show-capture=no

# Run tests with markers
test_marker MARKER:
	poetry run pytest -v -rs -n auto --show-capture=no -m {{MARKER}}

# Run tests with coverage
coverage:
	poetry run pytest -v -rs -n auto --show-capture=no --cov --cov-report=term --cov-fail-under=75

# Check the coverage of the tests and export to html
coverage_html:
	poetry run pytest -v -rs -n auto --show-capture=no --cov --cov-report=html:htmlcov --cov-report=term --cov-fail-under=75

ci: lint coverage
