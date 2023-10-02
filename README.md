# proxy-python

[![Coverage](https://github.com/hawks-atlanta/proxy-python/actions/workflows/coverage.yaml/badge.svg)](https://github.com/hawks-atlanta/proxy-python/actions/workflows/coverage.yaml)
[![Release](https://github.com/hawks-atlanta/proxy-python/actions/workflows/release.yaml/badge.svg)](https://github.com/hawks-atlanta/proxy-python/actions/workflows/release.yaml)
[![Tagging](https://github.com/hawks-atlanta/proxy-python/actions/workflows/tagging.yaml/badge.svg)](https://github.com/hawks-atlanta/proxy-python/actions/workflows/tagging.yaml)
[![Test](https://github.com/hawks-atlanta/proxy-python/actions/workflows/testing.yaml/badge.svg)](https://github.com/hawks-atlanta/proxy-python/actions/workflows/testing.yaml)
[![codecov](https://codecov.io/gh/hawks-atlanta/proxy-python/graph/badge.svg?token=JODBEVCYCF)](https://codecov.io/gh/hawks-atlanta/proxy-python)

## Description

Proxy service intended to forward traffic between clients and `gateway-java` so they don't need to suffer `SOAP`

## Development

You will follow this guide as you are in the root of repository.

### Python environment

First of all you need to setup your python environment.

```shell
python -m venv venv
```

Once created, activate it:

- Windows

```shell
# If you prefer CMD
./venv/Scripts/activate.bat

# If you prefer PowerShell
./venv/Scripts/Activate/ps1
```

- Linux

```shell
source ./venv/bin/activate
```

Finally install the dependencies

```shell
pip install -r requirements.txt
```

### Services

Make sure you setup the needed services.

```shell
docker compose up -d
```

### Testing

```shell
coverage run -m pytest
```

### Formatting and linting

If you installed the recommended extensions for VSCode, you may have the formatting and linting configured out of the box.

Additionally, you may need to configure `black` to format `python` files with the following steps:

- Open the command palette (Ctrl + Shift + P)
- Search Format Document With...
- Search Configure Default Formatter...
- Select "Black Formatter"

You can also run the following commands to format and lint the code from the console:

```bash
# Check format
black --check .

# Format all python files
black .

# Check lint
ruff check .

# Fix lint (if possible)
ruff check --fix .
```

## Coverage

| [![circle](https://codecov.io/gh/hawks-atlanta/proxy-python/graphs/sunburst.svg?token=JODBEVCYCF)](https://app.codecov.io/gh/hawks-atlanta/proxy-python) | [![square](https://codecov.io/gh/hawks-atlanta/proxy-python/graphs/tree.svg?token=JODBEVCYCF)](https://app.codecov.io/gh/hawks-atlanta/proxy-python) |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
