# Konfiguracja AI Agents - Uniwersalny szablon projektu

## Informacje o projekcie

- **Nazwa projektu**: `ObsGraph-Flask`
- **Główny język**: `Python`
- **Wersja języka**: `3.11+`
- **Framework**: `Flask`
- **Główna biblioteka narzędziowa**: `jsktoolbox@^1.2.0`
- **System zarządzania**: `Poetry`
- **Repozytorium**: `git`

---

## Konfiguracja plików

### Automatyczna detekcja typu projektu

Uwzględnij pliki na podstawie wykrytej struktury projektu:

**files.include** - Pliki źródłowe i testy:

<!-- Dla projektów Python -->

- `**/*.py` (gdy istnieje `pyproject.toml` lub `setup.py`)
- `tests/**/*.py`
- `test_*.py`

<!-- Dla projektów Shell -->

- `**/*.sh` (skrypty bash)
- `**/*.bash`
- `**/*.zsh`
- `**/*.csh`
- `bin/*` (skrypty bez rozszerzenia z shebang)

<!-- Dla projektów Perl -->

- `**/*.pl`
- `**/*.pm`
- `lib/**/*.pl`
- `lib/**/*.pm`

<!-- Dokumentacja (wszystkie projekty) -->

- `README.md`
- `docs/**/*.md`
- `*.md` (pliki markdown w głównym katalogu)

<!-- Konfiguracja (wszystkie projekty) -->

- `pyproject.toml`
- `.shellcheckrc`
- `.perlcriticrc`
- `Makefile`

**files.exclude** - Wykluczenia uniwersalne:

<!-- Środowiska wirtualne i cache Python -->

- `.venv/**`
- `venv/**`
- `env/**`
- `.pytest_cache/**`
- `__pycache__/**`
- `*.pyc`
- `*.pyo`
- `dist/**`
- `build/**`
- `*.egg-info/**`

<!-- Git i systemy kontroli wersji -->

- `.git/**`
- `.svn/**`
- `.gitignore`

<!-- IDE i edytory -->

- `.vscode/**`
- `.idea/**`
- `*.swp`
- `*~`

<!-- Logi i pliki tymczasowe -->

- `*.log`
- `*.tmp`
- `tmp/**`
- `temp/**`

<!-- Node modules (jeśli używasz narzędzi JS) -->

- `node_modules/**`

<!-- Przykłady i dane testowe (opcjonalnie) -->

- `examples/**` (odkomentuj jeśli chcesz wykluczyć)
- `sample_data/**`

---

## Instrukcje dotyczące zachowania

### Język i zarządzanie projektem

<!-- Python z Poetry -->

**Dla projektów Python z Poetry:**

- **Język**: Python 3.10+ (lub wersja określona w `pyproject.toml`)
- **Zarządzanie projektem**: Projekt używa Poetry
- **Uruchamianie narzędzi**: `poetry run <polecenie>` (np. `poetry run pytest`)
- **Instalacja zależności**: `poetry install`
- **Aktualizacja**: `poetry update`

<!-- Python bez Poetry -->

**Dla projektów Python bez Poetry:**

- **Język**: Python 3.x
- **Środowisko wirtualne**: Aktywuj `.venv/bin/activate` lub `venv/bin/activate`
- **Instalacja zależności**: `pip install -r requirements.txt`
- **Uruchamianie testów**: `pytest` lub `python -m pytest`

<!-- Shell Scripts -->

**Dla projektów Shell:**

- **Język**: Bash/sh (zgodny z POSIX gdy możliwe)
- **Interpreter**: Zawsze używaj shebang: `#!/usr/bin/env bash` lub `#!/bin/sh`
- **Bezpieczeństwo**: Używaj `set -euo pipefail` na początku skryptów bash
- **Walidacja**: `shellcheck` dla wszystkich skryptów

<!-- Perl -->

**Dla projektów Perl:**

- **Język**: Perl 5.x
- **Pragma**: Zawsze używaj `use strict;` i `use warnings;`
- **Wersja**: Określ minimalną wersję: `use 5.030;` (lub inna)
- **Moduły**: Instalacja przez `cpan` lub `cpanm`

### Styl kodowania

#### Python

**Formatowanie i walidacja:**

- **Formatter**: `black` - automatyczne formatowanie kodu
  - Uruchamianie: `poetry run black .` lub `black .`
  - Konfiguracja: Sprawdź `[tool.black]` w `pyproject.toml`
- **Linter**: `pycodestyle` lub `flake8` - zgodność z PEP 8
  - Uruchamianie: `poetry run pycodestyle .` lub `flake8 .`
- **Type checking**: `mypy` - sprawdzanie typów (opcjonalnie)
  - Uruchamianie: `poetry run mypy .`
- **Import sorting**: `isort` - sortowanie importów (opcjonalnie)
  - Uruchamianie: `poetry run isort .`

**Konwencje kodowania:**

- Przestrzegaj PEP 8 (Style Guide for Python Code)
- Dodawaj adnotacje typów do nowych funkcji i metod
- Używaj type hints zgodnie z PEP 484
- Preferuj pojedyncze cudzysłowy `'string'`, chyba że podwójne są wymagane
- Maksymalna długość linii: 88 znaków (black default) lub 79 (PEP 8)
- Używaj f-strings do formatowania stringów (Python 3.6+)

**Docstringi:**

- Format: Google style lub NumPy style (określ preferowany)
- Struktura: Krótka linia streszczenia, następnie sekcje
- Sekcje: `### Arguments`, `### Returns`, `### Raises`, `### Examples`
- Język: Angielski (kod i dokumentacja techniczna)

#### Shell Scripts

**Formatowanie i walidacja:**

- **Formatter**: `shfmt` - formatowanie skryptów shell
  - Uruchamianie: `shfmt -w -i 2 script.sh`
  - Styl: 2 spacje wcięcia, POSIX when possible
- **Linter**: `shellcheck` - analiza statyczna
  - Uruchamianie: `shellcheck script.sh`
  - Poziom: Napraw wszystkie błędy i ostrzeżenia

**Konwencje kodowania:**

- Zawsze używaj cudzysłowów wokół zmiennych: `"$variable"`
- Używaj `[[ ]]` zamiast `[ ]` w bash (gdy nie wymaga POSIX)
- Definiuj funkcje jako: `function_name() { ... }`
- Sprawdzaj kody wyjścia: `if command; then ...`
- Używaj `readonly` dla stałych
- Komentuj nieoczywiste konstrukcje

**Bezpieczeństwo:**

```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined var, pipe fail
IFS=$'\n\t'        # Bezpieczny Internal Field Separator
```

#### Perl

**Formatowanie i walidacja:**

- **Formatter**: `perltidy` - formatowanie kodu Perl
  - Uruchamianie: `perltidy script.pl`
  - Konfiguracja: `.perltidyrc` w głównym katalogu
- **Linter**: `perlcritic` - analiza jakości kodu
  - Uruchamianie: `perlcritic script.pl`
  - Poziom: Severity 3 lub wyższy (configurable)

**Konwencje kodowania:**

- Zawsze: `use strict;` i `use warnings;`
- Określ wersję: `use 5.030;`
- Używaj `my` dla zmiennych lokalnych
- Unikaj globalnych zmiennych
- Dokumentacja POD (Plain Old Documentation) dla modułów
- Nazwy zmiennych: `$scalar`, `@array`, `%hash`
- Nazwy funkcji: `snake_case`

#### Markdown

**Formatowanie:**

- **Formatter**: `prettier` - formatowanie dokumentacji
  - Uruchamianie: `poetry run prettier --write *.md` lub `prettier --write *.md`
  - Konfiguracja: `.prettierrc` lub `package.json`
- Maksymalna długość linii: 80-100 znaków
- Używaj referencyjnych linków dla powtarzających się URL-i
- Dodawaj puste linie między sekcjami dla czytelności

### Testowanie

#### Python

**Framework i organizacja:**

- **Framework**: `pytest` (zalecane) lub `unittest`
- **Lokalizacja testów**: `tests/` w głównym katalogu lub obok kodu jako `test_*.py`
- **Nazewnictwo**: `test_*.py` lub `*_test.py`
- **Uruchamianie**: `poetry run pytest` lub `pytest`
- **Pokrycie kodu**: `pytest --cov=.` (wymaga `pytest-cov`)

**Konwencje testowe:**

- Klasy testowe dziedziczą po `unittest.TestCase` (unittest) lub są funkcjami (pytest)
- Jeden test = jedna funkcjonalność
- Używaj fixtures dla konfiguracji testowej
- Testy jednostkowe (unit) oraz integracyjne (integration) w osobnych katalogach
- Zapewnij pokrycie testami każdej nowej funkcjonalności (cel: >80%)

#### Shell Scripts

**Framework i organizacja:**

- **Framework**: `bats` (Bash Automated Testing System) lub `shunit2`
- **Lokalizacja testów**: `tests/` lub `test/`
- **Nazewnictwo**: `test_*.bats` lub `*_test.sh`
- **Uruchamianie**: `bats tests/` lub `./run_tests.sh`

**Konwencje testowe:**

- Testuj skrypty w izolowanym środowisku
- Używaj mock-ów dla zewnętrznych komend
- Sprawdzaj zarówno sukces jak i obsługę błędów
- Testuj exit codes

#### Perl

**Framework i organizacja:**

- **Framework**: `Test::More` lub `Test2::Suite`
- **Lokalizacja testów**: `t/` (standardowa konwencja Perl)
- **Nazewnictwo**: `*.t`
- **Uruchamianie**: `prove -l t/` lub `perl -Ilib t/test_file.t`

**Konwencje testowe:**

- Plan testów: `use Test::More tests => 10;` lub `done_testing();`
- Testy jednostkowe w `t/unit/`
- Testy integracyjne w `t/integration/`

### Obsługa błędów

#### Python

**Strategia obsługi błędów:**

- Używaj specyficznych wyjątków zamiast ogólnego `Exception`
- Twórz własne klasy wyjątków gdy potrzebne: `class CustomError(Exception)`
- Dokumentuj wyjątki w docstringach (sekcja `### Raises`)
- Używaj `try-except-finally` odpowiednio
- Unikaj "gołych" `except:` - zawsze określ typ wyjątku
- Loguj błędy przed re-raise lub obsługą

**Przykład dla projektów z własnym mechanizmem:**

```python
# Jeśli projekt ma własny mechanizm (jak w JskToolBox):
from raisetool import Raise
raise Raise.error(message, exception_type, class_name, frame)
```

#### Shell Scripts

**Strategia obsługi błędów:**

- Używaj `set -e` aby zatrzymać skrypt przy błędzie
- Sprawdzaj kody wyjścia: `if ! command; then handle_error; fi`
- Używaj `trap` dla cleanup: `trap cleanup EXIT ERR`
- Wypisuj informacyjne komunikaty błędów na stderr: `echo "Error" >&2`
- Zwracaj odpowiednie exit codes (0=sukces, 1-255=błąd)

#### Perl

**Strategia obsługi błędów:**

- Używaj `die` dla krytycznych błędów
- Używaj `warn` dla ostrzeżeń
- Sprawdzaj wartości zwrotne: `open my $fh, '<', $file or die "Cannot open: $!"`
- Używaj `eval` dla try-catch: `eval { ... }; if ($@) { handle_error($@); }`
- Moduły: `Try::Tiny` dla czytelniejszej obsługi wyjątków

### Kontrola wersji (Git)

**Jeśli projekt używa Git:**

**Konwencje commitów:**

- Format: `type(scope): subject` (Conventional Commits)
- Typy: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Przykład: `feat(parser): add support for JSON input`
- Długość subject: max 50 znaków
- Body (opcjonalnie): szczegółowy opis po pustej linii

**Branche:**

- `main`/`master` - stabilna wersja produkcyjna
- `develop` - główna gałąź rozwojowa (jeśli używasz git-flow)
- `feature/*` - nowe funkcjonalności
- `bugfix/*` - poprawki błędów
- `hotfix/*` - pilne poprawki do produkcji

**Pull Requests / Merge Requests:**

- Opisuj zmiany szczegółowo
- Linkuj do issues jeśli dotyczy
- Wykonaj review przed merge
- Uruchom testy przed PR

**Pre-commit hooks (opcjonalnie):**

Użyj `pre-commit` framework dla automatycznej walidacji:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.x.x
    hooks:
      - id: black
  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: vx.x.x
    hooks:
      - id: shellcheck
```

### Dokumentacja

**Struktura dokumentacji:**

- `README.md` - główny plik projektu (co, dlaczego, jak używać)
- `docs/` - szczegółowa dokumentacja techniczna
- `CHANGELOG.md` - historia zmian (Keep a Changelog format)
- `CONTRIBUTING.md` - przewodnik dla kontrybutorów
- `LICENSE` - licencja projektu
- `AGENTS.md` lub `AGENTS-TEMPLATE.md` - ten plik (konfiguracja AI)

**Format dokumentacji kodu:**

- API: Generuj ze źródeł (Sphinx dla Python, POD dla Perl)
- Przykłady użycia w `examples/` lub `samples/`
- Diagramy w `docs/diagrams/` (PlantUML, Mermaid, lub obrazy)

### Ogólne zalecenia

**Komunikacja z AI Assistant:**

- **Język odpowiedzi**: `Polski`
- **Język kodu**: Angielski (komentarze, nazwy zmiennych, dokumentacja)
- **Język dokumentacji projektu**: Angielski (README, docs)
- **Język konfiguracji**: Polski (AGENTS.md)

**Podejście do zmian:**

- Zachowuj zwięzłą, techniczną formę odpowiedzi
- Przy zmianach obejmujących wiele plików przedstaw plan i poproś o akceptację
- Testuj zmiany przed commitem
- Dokumentuj nieoczywiste decyzje projektowe
- Refaktoryzuj kod zgodnie z DRY (Don't Repeat Yourself)
- Preferuj czytelność nad "sprytne" rozwiązania

**Code Review Checklist:**

- [ ] Kod jest zgodny z konwencjami projektu
- [ ] Testy zostały dodane/zaktualizowane
- [ ] Dokumentacja jest aktualna
- [ ] Brak ostrzeżeń z linterów
- [ ] Zmiany nie psują istniejącej funkcjonalności
- [ ] Obsługa błędów jest poprawna
- [ ] Kod jest czytelny i zrozumiały

---

## Szablony dokumentacji

### Python Docstring Template

Docstringi tworzymy w języku angielskim według poniższych wzorców.

#### Module-level Docstring

```python
"""
Author:  [Author Name] --<[author_email@example.com]>
Created: [YYYY-MM-DD]

Purpose: [Short, one-line summary of the module's purpose.]

[Optional: More detailed description of the module's functionality,
its components, and how they fit into the larger project.]
"""
```

#### Class-level Docstring

```python
"""[Short, one-line summary of the class's purpose.]

[Optional: More detailed description of the class's responsibilities,
design choices, and its role (e.g., utility, data structure).]
"""
```

#### Function/Method-level Docstring

````python
"""[Short, one-line summary of what the function does.]

[Optional: More detailed explanation of the function's logic,
its use cases, or any important algorithms used.]

### Arguments:
* arg1: [type] - [Description of the first argument.]
* arg2: Optional[[type]] - [Description of the second, optional argument. Defaults to [DefaultValue].]

### Returns:
[type] - [Description of the returned value.]

### Raises:
* [ExceptionType]: [Description of the condition that causes this exception to be raised.]

### Examples:
```python
>>> function_name(arg1, arg2)
expected_result
````

"""

````

### Shell Script Documentation Template

```bash
#!/usr/bin/env bash
#
# Script: script_name.sh
# Author: [Author Name] <author@example.com>
# Created: [YYYY-MM-DD]
#
# Purpose:
#   [Short, one-line summary of what the script does.]
#
# Usage:
#   script_name.sh [options] <arguments>
#
# Options:
#   -h, --help      Display this help message
#   -v, --verbose   Enable verbose output
#   -d, --debug     Enable debug mode
#
# Examples:
#   script_name.sh --verbose input.txt
#   script_name.sh -d file1 file2
#
# Dependencies:
#   - Required commands: grep, awk, sed
#   - Optional: jq (for JSON processing)
#

set -euo pipefail
IFS=$'\n\t'

# Function documentation
# Usage: function_name <arg1> [arg2]
# Description: What the function does
# Arguments:
#   arg1 - Description of argument 1
#   arg2 - Optional description of argument 2
# Returns:
#   0 on success, 1 on failure
function_name() {
    local arg1="$1"
    local arg2="${2:-default}"
    # Function implementation
}
````

### Perl Documentation Template (POD)

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use 5.030;

=head1 NAME

ModuleName - Short description of the module

=head1 SYNOPSIS

    use ModuleName;

    my $obj = ModuleName->new();
    $obj->method();

=head1 DESCRIPTION

Detailed description of what the module does and why it's useful.

=head1 METHODS

=head2 new

Constructor. Creates a new instance.

    my $obj = ModuleName->new(
        param1 => 'value1',
        param2 => 'value2',
    );

=head2 method_name

Description of what the method does.

B<Arguments:>

=over 4

=item * arg1 - Description of first argument

=item * arg2 - Description of second argument

=back

B<Returns:> Description of return value

B<Example:>

    my $result = $obj->method_name($arg1, $arg2);

=head1 AUTHOR

[Author Name] <author@example.com>

=head1 LICENSE

[License information]

=cut

package ModuleName;
# Implementation here
```

### Markdown Documentation Template

Szablon dla dokumentacji `.md`, z naciskiem na czytelność, kontekst i przykłady.

````markdown
# [Module/Component Name]

**Source:** `[path/to/source/file]`

**[High-Level Introduction]:**
_(A user-friendly paragraph explaining what this module/component helps accomplish. Focus on the "why" and benefits, not just technical function.)_

## Getting Started

_(Explanation of installation, imports, and initial setup.)_

```language
# Installation (if applicable)
pip install package_name
# or
cpan install Module::Name
# or
npm install package-name

# Import/Usage
from module import Class
# or
use Module::Name;
```

## Prerequisites

- Requirement 1
- Requirement 2
- Optional: Requirement 3

---

## Usage

### Basic Example

```language
# Simple usage example
result = function(argument)
print(result)
```

### Advanced Example

```language
# More complex scenario
# Step-by-step explanation in comments
```

---

## API Reference

### `ClassName`

**Description:**
_(Detailed description of the class/component and its purpose.)_

#### `method_name(arg1, arg2)`

**Description:**
_(Full paragraph explaining the method's purpose, behavior, and use cases.)_

**Parameters:**

- `arg1` (type): Description of first parameter
- `arg2` (type, optional): Description of second parameter. Default: `default_value`

**Returns:**

- `return_type`: Description of return value

**Raises/Throws:**

- `ExceptionType`: When this exception occurs

**Example:**

```language
# Practical example with output
result = obj.method_name("value1", "value2")
print(result)
# Output: expected output
```

---

## Configuration

_(If applicable: configuration options, environment variables, config files)_

## Troubleshooting

### Common Issues

**Issue 1:**

- **Symptom:** Description
- **Cause:** Explanation
- **Solution:** How to fix

---

## Contributing

_(Guidelines for contributors if this is an open project)_

## License

_(License information)_

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
````

---

## Narzędzia deweloperskie - Zalecane zestawy

### Python Tools

**Podstawowe (zawsze):**

- `black` - code formatter
- `pytest` - testing framework
- `pycodestyle` lub `flake8` - linting

**Rozszerzone (zalecane):**

- `mypy` - type checking
- `isort` - import sorting
- `bandit` - security linting
- `coverage` lub `pytest-cov` - code coverage
- `sphinx` - documentation generator
- `pre-commit` - git hooks framework

**Poetry dependencies example:**

```toml
[tool.poetry.group.dev.dependencies]
black = "^23.0.0"
pytest = "^7.0.0"
pycodestyle = "^2.11.0"
mypy = "^1.5.0"
isort = "^5.12.0"
pytest-cov = "^4.1.0"
```

### Shell Script Tools

**Podstawowe:**

- `shellcheck` - static analysis
- `shfmt` - formatter

**Rozszerzone:**

- `bats` - testing framework
- `bashate` - style checker
- `checkbashisms` - POSIX compliance

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install shellcheck shfmt

# macOS
brew install shellcheck shfmt bats-core

# Using snap
snap install shellcheck shfmt
```

### Perl Tools

**Podstawowe:**

- `perltidy` - code formatter
- `perlcritic` - static analysis

**Rozszerzone:**

- `Test::More` - testing
- `Devel::Cover` - coverage
- `Perl::Tidy` - advanced formatting
- `Pod::Checker` - POD validation

**Installation:**

```bash
# CPAN
cpan Perl::Tidy Perl::Critic Test::More Devel::Cover

# cpanminus
cpanm Perl::Tidy Perl::Critic Test::More Devel::Cover
```

### Universal Tools

**Wszystkie projekty:**

- `git` - version control
- `prettier` - markdown/JSON/YAML formatter
- `editorconfig` - consistent editor settings
- `pre-commit` - git hooks (multi-language)

**CI/CD Tools:**

- GitHub Actions
- GitLab CI
- Jenkins
- Travis CI

---

## Konfiguracja per język - Quick Start

### Python Project Checklist

```bash
# Initial setup
poetry init  # or python -m venv .venv
poetry install  # or pip install -r requirements.txt

# Create basic structure
mkdir -p src tests docs
touch README.md CHANGELOG.md .gitignore

# Configure tools
poetry add --group dev black pytest pycodestyle
poetry run black --version

# Setup pre-commit (optional)
poetry add --group dev pre-commit
pre-commit install

# First commit
git init
git add .
git commit -m "chore: initial project setup"
```

### Shell Project Checklist

```bash
# Install tools
# (system-specific, see Shell Script Tools above)

# Create structure
mkdir -p bin lib tests docs
touch README.md .shellcheckrc

# Create .shellcheckrc
cat > .shellcheckrc << 'EOF'
# Enable all optional checks
enable=all

# Disable specific checks if needed
# disable=SC2034  # Unused variables
EOF

# Make scripts executable
chmod +x bin/*.sh

# Test
shellcheck bin/*.sh
```

### Perl Project Checklist

```bash
# Create standard Perl structure
mkdir -p lib t bin docs

# Create basic files
touch README.md Changes Makefile.PL

# Configure perltidy
cat > .perltidyrc << 'EOF'
-pbp     # Perl Best Practices
-nst     # no space before semicolon
-bt=2    # brace tightness
-pt=2    # parenthesis tightness
EOF

# Configure perlcritic
cat > .perlcriticrc << 'EOF'
severity = 3
only = 1
EOF

# Test
perlcritic lib/
```

---

## Adaptacja szablonu

### Jak dostosować ten szablon do swojego projektu:

1. **Skopiuj plik**: `cp AGENTS-TEMPLATE.md AGENTS.md`

2. **Uzupełnij sekcję "Informacje o projekcie"**:
   - Wpisz nazwę projektu
   - Określ główny język
   - Wybierz system zarządzania

3. **Dostosuj sekcje files.include/exclude**:
   - Odkomentuj odpowiednie wzorce dla używanego języka
   - Dodaj specyficzne ścieżki projektu
   - Usuń nieużywane sekcje

4. **Wybierz preferencje językowe**:
   - Określ język komunikacji z AI
   - Zachowaj język dokumentacji

5. **Skonfiguruj narzędzia**:
   - Zainstaluj zalecane narzędzia dla swojego języka
   - Utwórz pliki konfiguracyjne (`.shellcheckrc`, `.perltidyrc`, etc.)

6. **Dostosuj konwencje**:
   - Zmodyfikuj style guide według preferencji zespołu
   - Dodaj specyficzne reguły projektu

7. **Usuń nieużywane sekcje**:
   - Jeśli nie używasz danego języka, usuń jego sekcję
   - Uprość dokument do rzeczywistych potrzeb

### Przykład: Projekt Shell-only

```markdown
## Informacje o projekcie

- **Nazwa projektu**: `SystemTools`
- **Główny język**: `Shell`
- **Wersja języka**: `bash 5+`
- **System zarządzania**: `Manual`
- **Repozytorium**: `git`

**files.include**

- `**/*.sh`
- `bin/*`
- `*.md`

**files.exclude**

- `.git/**`
- `*.log`
- `tmp/**`
```

---

## Wersjonowanie szablonu

- **Wersja**: 1.0.0
- **Data utworzenia**: 2025-10-15
- **Autor**: Jacek Kotlarski
- **Ostatnia aktualizacja**: 2025-10-15

### Historia zmian

- `1.0.0` (2025-10-15): Dostosowanie konfiguracji dla projektu ObsGraph-Flask

---

## Dodatkowe zasoby

### Style Guides

- **Python**: [PEP 8](https://peps.python.org/pep-0008/), [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- **Shell**: [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- **Perl**: [Perl Best Practices](http://shop.oreilly.com/product/9780596001735.do)

### Narzędzia i dokumentacja

- **Poetry**: https://python-poetry.org/
- **ShellCheck**: https://www.shellcheck.net/
- **Perl::Critic**: https://metacpan.org/pod/Perl::Critic
- **Pre-commit**: https://pre-commit.com/
- **Conventional Commits**: https://www.conventionalcommits.org/

---

**Uwaga**: Ten szablon jest punktem wyjścia. Dostosuj go do specyficznych potrzeb swojego projektu, zespołu i organizacji.
