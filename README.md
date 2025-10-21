# ObsGraph-Flask

ObsGraph-Flask is a Flask-based web application for Observium graph visualization and analysis. The project embraces strong automation support through a dedicated AI agent configuration (`AGENTS.md`) that mirrors the standards defined in the JskToolBox ecosystem.

## Project Overview

- **Language**: Python 3.11+
- **Framework**: Flask
- **Primary Utility Library**: `jsktoolbox@^1.2.0`
- **Package Name**: `obsgraph_flask`
- **Dependency & Environment Manager**: Poetry
- **Delivery Methodology**: Test-Driven Development (TDD)

## Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management and tool execution)

## Quick Start

```bash
git clone <repository-url>
cd ObsGraph-Flask
poetry install
```

This command sequence creates an isolated virtual environment and installs all runtime and development dependencies declared in `pyproject.toml`.

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

## Usage

### Run the Application

```bash
poetry run flask run
```

### Execute Tests

```bash
poetry run pytest
```

### Apply Formatting

```bash
poetry run black .
```

## Project Layout

```
ObsGraph-Flask/
├── obsgraph_flask/       # Application package
├── tests/                # Test suite (pytest)
├── pyproject.toml        # Poetry configuration and dependencies
├── README.md             # Project overview and guidelines
└── AGENTS.md             # AI assistant configuration (see below)
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
