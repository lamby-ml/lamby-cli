# lamby-cli

CLI for Lamby. Built with python.

## Setup

### Creating the development environment

```bash
# Create the virtualenv
pipenv --python 3.7

# Activate the virtualenv
pipenv shell

# Install all project dependencies
pipenv install --dev

# Configure linter
flake8 --install-hook git
git config --bool flake8.strict true
```

## Development

### Running the application

```bash
python ./lamby/lamby.py command arg1 arg2 ...
```

### Building the application

```bash
# Create the executable (found in the dist folder)
make
```

### Run Tests

```bash
# Run all tests
pytest
```

### Linting the code

```bash
# Lint all the code
flake8 .
```

```bash
# Automatically format your code (fix linting errors)
autopep8 --recursive --in-place .
```
