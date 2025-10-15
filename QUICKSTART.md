# ObsGraph Flask - Quick Start

## Uruchomienie aplikacji

### Opcja 1: Bezpośrednio przez Poetry
```bash
poetry run python obsgraph_flask/app.py
```

### Opcja 2: Przez aktywowane środowisko wirtualne
```bash
poetry shell
python obsgraph_flask/app.py
```

Aplikacja będzie dostępna pod adresem: http://127.0.0.1:5000/

## Funkcjonalność

- **Wybór roku**: Lista rozwijana z bieżącym rokiem i 3 latami wstecz
- **Wybór miesiąca**: Lista rozwijana z miesiącami w formacie cyfrowym (01-12)
- **Przycisk Submit**: Zatwierdza wybór i przeładowuje stronę zachowując selekcję
- **Wyświetlanie daty**: Wybrana data wyświetlana w formacie YYYY-MM na środku strony

## Walidacja kodu

### Sprawdzanie typów (mypy)
```bash
poetry run mypy obsgraph_flask/
```

### Formatowanie kodu (black)
```bash
poetry run black obsgraph_flask/
```

### Sprawdzanie stylu (pycodestyle)
```bash
poetry run pycodestyle obsgraph_flask/
```

### Sortowanie importów (isort)
```bash
poetry run isort obsgraph_flask/
```

### Testy z pokryciem kodu
```bash
# Uruchom wszystkie testy
poetry run pytest

# Testy z raportem pokrycia
poetry run pytest --cov=obsgraph_flask

# Testy z HTML raportem pokrycia
poetry run pytest --cov=obsgraph_flask --cov-report=html
# Raport: htmlcov/index.html
```

## Test-Driven Development (TDD)

Projekt stosuje metodologię TDD. Przy dodawaniu nowej funkcjonalności:

### Krok 1: Napisz test (RED)
```bash
# Utwórz test w tests/test_feature.py
poetry run pytest tests/test_feature.py
# Test powinien nie przejść (RED)
```

### Krok 2: Implementuj funkcjonalność (GREEN)
```python
# Napisz minimalny kod w obsgraph_flask/feature.py
# aby test przeszedł
```

### Krok 3: Sprawdź czy test przechodzi
```bash
poetry run pytest tests/test_feature.py
# Test powinien przejść (GREEN)
```

### Krok 4: Refaktoryzacja
```python
# Popraw kod zachowując przechodzące testy
# Uruchamiaj testy po każdej zmianie
```

### Krok 5: Walidacja kompletna
```bash
# Wszystkie testy
poetry run pytest

# Pokrycie kodu (cel: ≥80%)
poetry run pytest --cov=obsgraph_flask --cov-report=term-missing

# Sprawdzenie typów
poetry run mypy obsgraph_flask/

# Formatowanie
poetry run black obsgraph_flask/
```

## Struktura projektu

```
obsgraph_flask/
├── app.py                  # Główna aplikacja Flask
└── templates/
    └── index.html          # Szablon HTML z formularzem

tests/
└── test_*.py              # Testy jednostkowe
```

## Wymogi dotyczące typowania

Projekt wymaga **pełnego typowania** zgodnie z PEP 484 i PEP 526:
- Wszystkie zmienne muszą mieć zadeklarowany typ
- Wszystkie argumenty funkcji muszą mieć type hints
- Wszystkie funkcje muszą mieć zadeklarowany typ zwracany
- Konfiguracja mypy wymusza te zasady poprzez `disallow_untyped_defs`

## Wymogi dotyczące testów

- **Metodologia**: TDD - testy przed implementacją
- **Framework**: pytest
- **Lokalizacja**: katalog `tests/`
- **Pokrycie**: minimum 80%
- **Typowanie**: testy też muszą być w pełni typowane

