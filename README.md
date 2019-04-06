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
# Set the appropriate environment variables
export MINIO_SERVER_URI=<MINIO_SERVER_URI>
export MINIO_ACCESS_KEY=<MINIO_ACCESS_KEY>
export MINIO_SECRET_KEY=<MINIO_SECRET_KEY>
```

```bash
# Or use dotenv to load environment variables on startup
echo "export MINIO_SERVER_URI=<MINIO_SERVER_URI>\n" \
     "export MINIO_ACCESS_KEY=<MINIO_ACCESS_KEY>\n" \
     "export MINIO_SECRET_KEY=<MINIO_SECRET_KEY>\n" > lamby/config/development.env
```

```bash
pip install --editable .

# Run commands
lamby --help
```

### Run Tests

```bash
# Run all tests
pytest -v
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

```bash
# Fix imports
isort -rc --atomic .
```
