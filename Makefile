# Create virtual environment
.PHONY: venv

venv:
	sh -c 'python -m venv env'


# Activate virtual environment
.PHONY: activate

activate:
	sh -c 'source env/Scripts/activate'

# Lint files
.PHONY: lint

lint:
	sh -c 'black src'
	sh -c 'isort src'

# Install requirements
.PHONY: install

install:
	sh -c 'cd src && pip install -r requirements.txt'

# Run init script
.PHONY: init

init:
	sh -c 'cd src && ./init.sh'

# Start application
.PHONY: start

start:
	sh -c 'cd src && python app.py'

# Run tests
.PHONY: test

test:
	sh -c 'cd src/tests && pytest . -W ignore::DeprecationWarning --verbose --html=report.html'

# Cleanup
.PHONY: clean

clean:
	sh -c 'rm -rf env'

# Default target
all: venv activate install init start
