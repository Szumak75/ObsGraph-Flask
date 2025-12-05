# ObsGraph-Flask

ObsGraph-Flask is a Flask-based web application for Observium network monitoring graph visualization and analysis. The application fetches and displays network traffic graphs from Observium API with an intuitive date selection interface. The project embraces strong automation support through a dedicated AI agent configuration (`AGENTS.md`) that mirrors the standards defined in the JskToolBox ecosystem.

## Features

- **Interactive Date Selection**: Choose year and month to view network traffic data
- **Observium API Integration**: Seamlessly fetches multi-port traffic graphs from Observium
- **Responsive UI**: Clean, modern interface with real-time error feedback
- **Secure Configuration**: Encrypted password storage using JskToolBox crypto utilities
- **Configuration Tool**: CLI utility for managing application settings

## Project Overview

- **Language**: Python 3.11+
- **Framework**: Flask 3.0+
- **Primary Utility Library**: `jsktoolbox@^1.2.0`
- **HTTP Client**: `requests@^2.31.0`
- **Package Name**: `obsgraph_flask`
- **Dependency & Environment Manager**: Poetry
- **Delivery Methodology**: Test-Driven Development (TDD)

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management and tool execution)

## Quick Start

### 1. Installation

```bash
git clone <repository-url>
cd ObsGraph-Flask
poetry install
```

This command sequence creates an isolated virtual environment and installs all runtime and development dependencies declared in `pyproject.toml`.

### 2. Configuration

Configure the application using the CLI tool:

```bash
poetry run python obsgraph_flask/tools/obsgraph_configurator.py \
  --url "https://observium.example.com" \
  --login "api_user" \
  --password "api_password" \
  --ids "496,508" \
  --width 1024 \
  --height 600
```

Or manually edit `etc/obsgraph.conf`:

```ini
[ObsGraphFlaskApp]
salt = 5083235041753769
observium_url = "https://observium.example.com/"
api_login = "api_user"
api_password = "encrypted_password_here"
port_ids = "496,508"
graph_width = 1024
graph_height = 600
```

**Configuration Options:**

- `salt` - Application salt for password encryption (auto-generated)
- `observium_url` - Base URL of Observium API
- `api_login` - Observium API username
- `api_password` - Encrypted API password
- `port_ids` - Comma-separated port IDs for multi-port graphs
- `graph_width` - Width of generated graphs in pixels (default: 1024)
- `graph_height` - Height of generated graphs in pixels (default: 600)

### 3. Run the Application

#### Development Mode

```bash
poetry run python obsgraph_flask/app.py
```

The application will be available at `http://127.0.0.1:5000/`

#### Production Mode with Gunicorn

```bash
# Using default configuration
poetry run gunicorn "obsgraph_flask.app:app"

# Using custom configuration file
poetry run gunicorn --config gunicorn.conf.py "obsgraph_flask.app:app"

# Quick start with custom workers
poetry run gunicorn --workers 4 --bind 0.0.0.0:8000 "obsgraph_flask.app:app"
```

The application will be available at `http://0.0.0.0:5000/` (or configured port)

## Development Toolkit

The project relies on the following tools:

- `black` – opinionated code formatter (88-character line length)
- `pytest` – primary test runner
- `pytest-cov` – coverage reporting
- `mypy` – static typing enforcement
- `pycodestyle` – PEP 8 compliance checks
- `isort` – import ordering

### Frequently Used Commands

```bash
# Run the full test suite with coverage
poetry run pytest --cov=obsgraph_flask --cov-report=html

# Static type checking
poetry run mypy obsgraph_flask/

# Automatic formatting and import hygiene
poetry run black obsgraph_flask/ tests/
poetry run isort obsgraph_flask/ tests/

# Style linting
poetry run pycodestyle obsgraph_flask/
```

## Configuration Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `salt` | int | Yes | Salt value for password encryption |
| `observium_url` | str | Yes | Base URL of Observium instance |
| `api_login` | str | Yes | API username |
| `api_password` | str | Yes | Encrypted API password |
| `port_ids` | str | Yes | Comma-separated port IDs for graphs |

## Usage

### Run the Application

```bash
# Option 1: Direct execution
poetry run python obsgraph_flask/app.py

# Option 2: Flask development server
poetry run flask run

# Option 3: Activated virtual environment
poetry shell
python obsgraph_flask/app.py
```

### Configure the Application

```bash
# Using CLI tool
poetry run python obsgraph_flask/tools/obsgraph_configurator.py --help

# Using shell wrapper
./bin/osbgraph-config.sh --url "https://observium.example.com" --login "api" --password "secret" --ids "496,508"
```

### Execute Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=obsgraph_flask --cov-report=html
```

### Apply Formatting

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Check style
poetry run pycodestyle obsgraph_flask/
```

## Project Layout

```
ObsGraph-Flask/
├── obsgraph_flask/              # Application package
│   ├── app.py                   # Main Flask application
│   ├── lib/                     # Library modules
│   │   └── keys.py              # Configuration keys
│   ├── templates/               # Jinja2 templates
│   │   └── index.html           # Main page template
│   └── tools/                   # CLI utilities
│       └── obsgraph_configurator.py  # Configuration tool
├── bin/                         # Shell scripts
│   └── osbgraph-config.sh       # Configuration wrapper script
├── etc/                         # Configuration files
│   ├── obsgraph.conf            # Main configuration
│   └── README.md                # Configuration documentation
├── tests/                       # Test suite (pytest)
│   ├── test_app.py              # Application tests
│   └── test_basic.py            # Basic functionality tests
├── pyproject.toml               # Poetry configuration and dependencies
├── poetry.lock                  # Locked dependencies
├── README.md                    # Project overview and guidelines
├── QUICKSTART.md                # Quick start guide
└── AGENTS.md                    # AI assistant configuration
```

## Contributing Guidelines

The development process is anchored in **TDD**:

1. **Red** – write a failing test that captures the desired behaviour.
2. **Green** – implement the minimal code required to satisfy the test.
3. **Refactor** – improve structure while keeping the suite green and coverage ≥ 80%.

Additional expectations:

- Follow PEP 8, leverage full static typing, and document public behaviour with English docstrings.
- Keep formatting consistent by running `poetry run black` and `poetry run isort` before pushing changes.
- Ensure `poetry run pytest`, `poetry run mypy`, and `poetry run pycodestyle` all pass locally.

## Maintaining `AGENTS.md`

`AGENTS.md` stores the automation playbook for AI agents collaborating on ObsGraph-Flask. The content is derived from the canonical Python template once distributed as `AGENTS-PYTEMPLATE.md`. The instructions below consolidate that template so the standalone file is no longer required.

### Purpose

- Document include/exclude file patterns for assistants.
- Capture formatting, typing, and documentation standards.
- Preserve project-specific architectural patterns (notably JskToolBox usage).
- Define communication rules, TDD requirements, and review expectations.

### Placeholder Values for ObsGraph-Flask

| Placeholder        | Value                    |
| ------------------ | ------------------------ |
| `{PROJECT_NAME}`   | `ObsGraph-Flask`         |
| `{PACKAGE_NAME}`   | `obsgraph_flask`         |
| `{AUTHOR_NAME}`    | `Jacek Kotlarski`        |
| `{AUTHOR_EMAIL}`   | `jacek.kotlarski@bioseco.com` |
| `{PYTHON_VERSION}` | `3.11+`                  |
| `{TEST_DIR}`       | `tests`                  |
| `{DOCS_DIR}`       | `docs`                   |
| `{EXAMPLES_DIR}`   | `examples` (omit if unused) |

### Update Workflow

1. **Source the latest template**  
   Obtain the newest `AGENTS-PYTEMPLATE.md` from the JskToolBox knowledge base or the internal templates repository.
2. **Copy to the project root**  
   Place the template alongside `AGENTS.md` to ease comparison.
3. **Replace placeholders**  
   Substitute all `{PLACEHOLDER}` entries with the values above. Example commands (GNU `sed`):
   ```bash
   sed -i 's/{PROJECT_NAME}/ObsGraph-Flask/g' AGENTS.md
   sed -i 's/{PACKAGE_NAME}/obsgraph_flask/g' AGENTS.md
   sed -i 's/{AUTHOR_NAME}/Jacek Kotlarski/g' AGENTS.md
   sed -i 's/{AUTHOR_EMAIL}/jacek.kotlarski@bioseco.com/g' AGENTS.md
   sed -i 's/{PYTHON_VERSION}/3.11+/g' AGENTS.md
   sed -i 's/{TEST_DIR}/tests/g' AGENTS.md
   sed -i 's/{DOCS_DIR}/docs/g' AGENTS.md
   sed -i 's/{EXAMPLES_DIR}/examples/g' AGENTS.md
   ```
4. **Tailor project-specific sections**  
   - Keep the “Use JskToolBox” chapter; it applies directly to ObsGraph-Flask.  
   - Expand “Project-specific rules” with any new architectural or domain guidelines.  
   - Remove template comment blocks (`<!-- ... -->`) after verification.
5. **Verify consistency**  
   Confirm that docstring, testing, and formatting directives align with current tooling.
6. **Delete the temporary template**  
   Remove `AGENTS-PYTEMPLATE.md` once the transfer is complete to avoid duplication.
7. **Commit the changes**  
   Example message: `docs: refresh AI agent configuration`.

### Customisation Checklist

- [ ] Docstrings updated first, then API docs, then Markdown (documentation-first rule).
- [ ] Sections about `ReadOnlyClass`, `BData`, lazy imports, and `Raise.error` remain accurate.
- [ ] Testing and coverage thresholds in `AGENTS.md` reflect the current project expectations.
- [ ] Communication language rules mirror project policy (Polish responses, English code/docs).
- [ ] Git workflow details stay aligned with the repository conventions.

### Template Compatibility

The integrated instructions are validated with:

- GitHub Copilot
- Google Gemini
- Claude (Anthropic)
- OpenAI models (Codex, GPT)
- Any assistant that consumes Markdown configuration files

## License

[Specify license here]

## Author

Jacek Kotlarski `<jacek.kotlarski@bioseco.com>`
