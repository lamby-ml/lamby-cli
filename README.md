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
python ./lamby/lamby.py command arg1 arg2 ...
```

### Building the application

```bash
# Create the executable (found in the dist folder)
make
```

### Run Tests

```bash
# Set the appropriate testing environment variables
echo "export MINIO_SERVER_URI=<MINIO_SERVER_URI>\n" \
     "export MINIO_ACCESS_KEY=<MINIO_ACCESS_KEY>\n" \
     "export MINIO_SECRET_KEY=<MINIO_SECRET_KEY>\n" > lamby/config/testing.env
```

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
