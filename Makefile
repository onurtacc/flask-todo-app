# Makefile for V&V project
# Note: On Windows, use: make -f Makefile <target>

PYTHON = .venv/Scripts/python.exe
PIP = .venv/Scripts/pip.exe

.PHONY: run test cov ui formal all clean

run:
	$(PYTHON) app.py

test:
	$(PYTHON) -m pytest -q

cov:
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage xml -o artifacts/coverage.xml
	$(PYTHON) -m coverage html

ui:
	$(PYTHON) -m pytest -q tests/test_ui_playwright.py

formal:
	$(PYTHON) -m crosshair check domain_contracts.py

junit:
	$(PYTHON) -m pytest --junitxml=artifacts/junit.xml

all: test cov junit formal

clean:
	rm -rf artifacts/*.xml artifacts/*.png htmlcov .coverage .pytest_cache
	rm -rf __pycache__ tests/__pycache__
