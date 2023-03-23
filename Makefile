# Create virtual environment
venv:
    python -m venv env

# Activate virtual environment
activate:
	source env/Scripts/activate

# Lint files
lint:
    black src && isort src

# Install requirements
install:
	cd src && pip install -r requirements.txt

# Run init script
init:
	sh init.sh

# Start application
start:
	python app.py

tests:
	cd tests && pytest . -W ignore::DeprecationWarning --verbose --html=report.html

# Default target
all: venv activate install init start