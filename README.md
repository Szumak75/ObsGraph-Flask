# ObsGraph-Flask

A Flask-based web application for Observium graph visualization and analysis.

## Project Information

- **Language**: Python 3.11+
- **Framework**: Flask
- **Main Utility Library**: jsktoolbox@^1.2.0
- **Project Management**: Poetry

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ObsGraph-Flask
```

2. Install dependencies using Poetry:
```bash
poetry install
```

This will create a virtual environment and install all necessary dependencies including development tools.

## Development Tools

The project uses the following development tools:

- **black**: Code formatter
- **pytest**: Testing framework
- **pycodestyle**: PEP 8 compliance checker (optional)
- **isort**: Import sorting (optional)

## Usage

### Running the Application

```bash
poetry run flask run
```

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black .
```

## Project Structure

```
ObsGraph-Flask/
├── obsgraph_flask/     # Main application package
├── tests/              # Test files
├── pyproject.toml      # Poetry configuration
├── README.md           # This file
└── AGENTS.md           # AI assistant configuration
```

## Contributing

When contributing to this project, please:

1. Follow PEP 8 style guidelines
2. Use type hints for all functions and methods
3. Write tests for new functionality
4. Format code with `black` before committing
5. Ensure all tests pass

## License

[Specify license here]

## Author

Jacek Kotlarski <jacek.kotlarski@bioseco.com>
