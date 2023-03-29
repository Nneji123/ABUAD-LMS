# Install pyenv and python 3.8.10
.PHONY: setup-linux

setup-linux:
	sh -c 'sudo apt-get update'
	sh -c 'sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git'
	sh -c 'curl https://pyenv.run | bash'
	sh -c 'echo "export PATH="$HOME/.pyenv/bin:$PATH"" >> ~/.bashrc'
	sh -c 'echo "eval "$(pyenv init -)"" >> ~/.bashrc'
	sh -c 'echo "eval "$(pyenv virtualenv-init -)"" >> ~/.bashrc'
	sh -c 'source ~/.bashrc'
	sh -c 'pyenv install 3.8.10'
	sh -c 'pyenv global 3.8.10'


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
	deactivate
	sh -c 'rm -rf env'

# Default target
all: venv activate install init start
