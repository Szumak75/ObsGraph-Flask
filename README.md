# ObsGraph-Flask

A Flask-based web application for Observium graph visualization and analysis.

## Project Information

- **Language**: Python 3.11+
- **Framework**: Flask
- **Main Utility Library**: jsktoolbox@^1.2.0
- **Project Management**: Poetry
- **Development Methodology**: TDD (Test-Driven Development)

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
- **pytest**: Testing framework with coverage support
- **pytest-cov**: Code coverage measurement
- **mypy**: Static type checker
- **pycodestyle**: PEP 8 compliance checker
- **isort**: Import sorting

### Code Quality Commands

```bash
# Run tests with coverage
poetry run pytest --cov=obsgraph_flask --cov-report=html

# Type checking
poetry run mypy obsgraph_flask/

# Code formatting
poetry run black obsgraph_flask/

# Import sorting
poetry run isort obsgraph_flask/

# Style checking
poetry run pycodestyle obsgraph_flask/
```

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

This project follows **Test-Driven Development (TDD)** methodology.

### Development Workflow

1. **Write Tests First** (RED phase)
   - Write unit tests for the new functionality
   - Tests should fail initially

2. **Implement Functionality** (GREEN phase)
   - Write minimal code to make tests pass
   - All tests must pass

3. **Refactor** (REFACTOR phase)
   - Improve code quality while keeping tests green
   - Maintain or improve code coverage

### Code Quality Requirements

- ✅ Follow PEP 8 style guidelines
- ✅ **Required**: Full type hints (typing module) for all variables, arguments, and return values
- ✅ **Required**: Write tests BEFORE implementing new features
- ✅ **Required**: Maintain minimum 80% code coverage
- ✅ Format code with `black` before committing
- ✅ Ensure all tests pass: `poetry run pytest`
- ✅ Ensure type checking passes: `poetry run mypy obsgraph_flask/`
- ✅ Write descriptive docstrings in English (Google style)

### Testing Standards

- Location: `tests/` directory
- Naming: `test_*.py`
- Framework: pytest
- Coverage target: ≥ 80%
- Run tests: `poetry run pytest --cov=obsgraph_flask`

## License

[Specify license here]

## Author

Jacek Kotlarski <jacek.kotlarski@bioseco.com>
