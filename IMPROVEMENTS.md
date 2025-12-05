# Propozycje ulepszeń projektu ObsGraph-Flask

**Data analizy**: 2025-12-05  
**Wersja projektu**: 0.1.0  
**Autor analizy**: ObsGraph Team

---

## 1. Architektura i struktura kodu

### ✅ Mocne strony
- Wykorzystanie wzorców z JskToolBox (BData, ReadOnlyClass, Raise)
- Separacja logiki biznesowej (ObsGraphApp) od warstwy prezentacji (Flask routes)
- Typowanie statyczne we wszystkich funkcjach
- Dobra organizacja katalogów (lib/, templates/, tools/)

### 🔄 Proponowane ulepszenia

#### 1.1. Separacja konfiguracji
**Priorytet: Średni**

Wydzielenie zarządzania konfiguracją do osobnej klasy:

```python
# obsgraph_flask/lib/config_manager.py
class ConfigManager(BData):
    """Manages application configuration with validation and decryption."""
    
    def __init__(self, config_path: str):
        # Configuration loading and validation logic
        pass
    
    @property
    def observium_url(self) -> str:
        ...
    
    @property
    def api_credentials(self) -> Tuple[str, str]:
        """Returns (login, decrypted_password) tuple."""
        ...
```

**Korzyści**:
- Lepsza testowalność
- Możliwość ponownego wykorzystania w innych narzędziach
- Łatwiejsza zmiana źródła konfiguracji (plik/env/baza danych)

#### 1.2. Service Layer dla API Observium
**Priorytet: Wysoki**

Utworzenie dedykowanego serwisu do komunikacji z Observium:

```python
# obsgraph_flask/services/observium_service.py
class ObserviumService:
    """Handles all communication with Observium API."""
    
    def __init__(self, base_url: str, auth: Tuple[str, str]):
        self.base_url = base_url
        self.auth = auth
        self.session = requests.Session()
    
    def get_multi_port_graph(
        self, 
        port_ids: str, 
        start_ts: int, 
        end_ts: int,
        width: int = 1024,
        height: int = 600
    ) -> Optional[bytes]:
        """Fetch graph image from Observium API."""
        ...
    
    def get_device_list(self) -> List[Dict]:
        """Fetch list of devices from Observium."""
        ...
```

**Korzyści**:
- Możliwość łatwego dodania innych endpointów API
- Lepsze zarządzanie sesją HTTP
- Testowanie bez uruchamiania Flask app

---

## 2. Funkcjonalność

### 🔄 Proponowane rozszerzenia

#### 2.1. Konfigurowalne wymiary wykresów
**Priorytet**: Średni**

```python
# etc/obsgraph.conf
[ObsGraphFlaskApp]
graph_width = 1024
graph_height = 600
```

#### 2.2. Cache wykresów
**Priorytet: Wysoki**

Implementacja cache'owania pobranych wykresów:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class ObsGraphApp(BData):
    def __init__(self):
        self._cache: Dict[str, Tuple[str, datetime]] = {}
        self._cache_ttl: timedelta = timedelta(minutes=15)
    
    def get_observium_charts(self, year: int, month: int) -> Optional[str]:
        cache_key: str = f"{year}-{month}"
        
        if cache_key in self._cache:
            image, timestamp = self._cache[cache_key]
            if datetime.now() - timestamp < self._cache_ttl:
                return image
        
        # Fetch from API
        ...
```

**Korzyści**:
- Zmniejszenie obciążenia API Observium
- Szybsza odpowiedź aplikacji
- Mniejsze zużycie zasobów sieciowych

#### 2.3. Wybór zakresu dat
**Priorytet: Niski**

Dodanie możliwości wyboru konkretnego zakresu dat zamiast tylko miesiąca:

```html
<input type="date" name="start_date" />
<input type="date" name="end_date" />
```

#### 2.4. Eksport wykresów
**Priorytet: Niski**

Dodanie funkcji pobierania wykresu jako pliku PNG:

```python
@app.route("/export/<year>/<month>")
def export_chart(year: int, month: int) -> Response:
    """Export chart as PNG file."""
    chart_data = obs_app.get_observium_charts(year, month)
    # Decode base64 and return as file
    ...
```

---

## 3. Obsługa błędów i logowanie

### 🔄 Proponowane ulepszenia

#### 3.1. Strukturalne logowanie
**Priorytet: Wysoki**

```python
import logging
from pythonjsonlogger import jsonlogger

# obsgraph_flask/lib/logger.py
def setup_logger() -> logging.Logger:
    logger = logging.getLogger("obsgraph")
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
```

**Użycie**:
```python
logger.info("Fetching chart", extra={
    "year": year,
    "month": month,
    "port_ids": port_ids
})
```

#### 3.2. Retry logic dla API calls
**Priorytet: Średni**

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ObserviumService:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def get_multi_port_graph(self, ...) -> Optional[bytes]:
        ...
```

#### 3.3. Kategoryzacja błędów
**Priorytet: Średni**

```python
class ObsGraphError(Exception):
    """Base exception for ObsGraph errors."""
    pass

class ConfigurationError(ObsGraphError):
    """Configuration related errors."""
    pass

class APIError(ObsGraphError):
    """Observium API communication errors."""
    pass
```

---

## 4. Testy

### ✅ Obecny stan
- 18 testów przechodzących
- Podstawowe testy routes i formatowania
- Testy jednostkowe dla kalkulacji timestampów

### 🔄 Proponowane rozszerzenia

#### 4.1. Testy integracyjne z mockowaniem API
**Priorytet: Wysoki**

```python
# tests/test_integration.py
@responses.activate
def test_successful_chart_retrieval():
    """Test end-to-end chart retrieval with mocked API."""
    responses.add(
        responses.GET,
        "https://observium.example.com/graph.php",
        body=b"fake_image_data",
        status=200,
        content_type="image/png"
    )
    
    with app.test_client() as client:
        response = client.post("/", data={"year": "2025", "month": "11"})
        assert b"data:image/png;base64," in response.data
```

#### 4.2. Testy wydajnościowe
**Priorytet: Niski**

```python
# tests/test_performance.py
def test_response_time_under_2_seconds():
    """Ensure page loads within acceptable time."""
    with app.test_client() as client:
        start = time.time()
        response = client.get("/")
        duration = time.time() - start
        
        assert duration < 2.0
        assert response.status_code == 200
```

#### 4.3. Pokrycie testami >80%
**Priorytet: Wysoki**

Obecne pokrycie należy sprawdzić i uzupełnić brakujące testy:

```bash
poetry run pytest --cov=obsgraph_flask --cov-report=term-missing
```

---

## 5. UI/UX

### 🔄 Proponowane ulepszenia

#### 5.1. Loading indicator
**Priorytet: Średni**

Dodanie wskaźnika ładowania podczas pobierania wykresu:

```html
<div id="loading" style="display:none;">
    <div class="spinner"></div>
    <p>Loading chart...</p>
</div>

<script>
document.querySelector('form').addEventListener('submit', function() {
    document.getElementById('loading').style.display = 'block';
});
</script>
```

#### 5.2. Lepsze wyświetlanie błędów
**Priorytet: Niski**

Kategoryzacja błędów z ikonami:

```html
<div class="error-item error-config">
    <span class="icon">⚙️</span>
    <span class="message">Configuration error: ...</span>
</div>

<div class="error-item error-network">
    <span class="icon">🌐</span>
    <span class="message">Network error: ...</span>
</div>
```

#### 5.3. Dark mode
**Priorytet: Niski**

```css
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    .chart-container {
        background-color: #2a2a2a;
    }
}
```

#### 5.4. Responsywność mobile
**Priorytet: Średni**

Obecnie wykres może być za duży na urządzeniach mobilnych:

```css
@media (max-width: 768px) {
    .chart-image {
        max-width: 100%;
        height: auto;
    }
    .top-controls {
        flex-direction: column;
        width: 90%;
    }
}
```

---

## 6. Bezpieczeństwo

### 🔄 Proponowane ulepszenia

#### 6.1. Rate limiting
**Priorytet: Wysoki**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def index() -> str:
    ...
```

#### 6.2. HTTPS enforcement
**Priorytet: Wysoki**

```python
from flask_talisman import Talisman

if not app.config.get("TESTING"):
    Talisman(app, force_https=True)
```

#### 6.3. Input validation
**Priorytet: Wysoki**

```python
from marshmallow import Schema, fields, validate, ValidationError

class DateSelectionSchema(Schema):
    year = fields.Int(
        required=True,
        validate=validate.Range(min=2020, max=2030)
    )
    month = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=12)
    )

@app.route("/", methods=["POST"])
def index() -> str:
    schema = DateSelectionSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as err:
        # Handle validation error
        ...
```

---

## 7. Dokumentacja

### 🔄 Proponowane ulepszenia

#### 7.1. API Documentation
**Priorytet: Niski**

Dodanie dokumentacji API przy użyciu Swagger/OpenAPI:

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "ObsGraph-Flask"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

#### 7.2. Rozszerzenie README
**Priorytet: Niski**

Dodanie sekcji:
- Screenshots aplikacji
- Troubleshooting guide
- FAQ
- Contributing guidelines

---

## 8. DevOps i deployment

### 🔄 Proponowane ulepszenia

#### 8.1. Docker support
**Priorytet: Średni**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:5000", "obsgraph_flask.app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  obsgraph:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./etc:/app/etc
    environment:
      - FLASK_ENV=production
```

#### 8.2. CI/CD Pipeline
**Priorytet: Średni**

``yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest --cov=obsgraph_flask
      - name: Check code style
        run: poetry run black --check .
      - name: Type checking
        run: poetry run mypy obsgraph_flask/
```

#### 8.3. Health check endpoint
**Priorytet: Średni**

```python
@app.route("/health")
def health_check() -> Tuple[Dict[str, Any], int]:
    """Health check endpoint for monitoring."""
    health_status = {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }
    
    # Check Observium API connectivity
    try:
        # Quick ping to Observium
        ...
        health_status["observium_api"] = "available"
    except Exception:
        health_status["observium_api"] = "unavailable"
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return health_status, status_code
```

---

## 9. Monitoring i metryki

### 🔄 Proponowane ulepszenia

#### 9.1. Prometheus metrics
**Priorytet: Niski**

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Custom metrics
chart_requests = metrics.counter(
    'obsgraph_chart_requests_total',
    'Total chart requests',
    labels={'year': lambda: request.form.get('year')}
)

@app.route("/", methods=["POST"])
@chart_requests
def index() -> str:
    ...
```

#### 9.2. Error tracking
**Priorytet: Średni**

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

---

## 10. Podsumowanie priorytetów

### 🔴 Wysoki priorytet (do zaimplementowania w pierwszej kolejności)
1. Service Layer dla API Observium
2. Cache wykresów
3. Strukturalne logowanie
4. Pokrycie testami >80%
5. Rate limiting
6. HTTPS enforcement
7. Input validation

### 🟡 Średni priorytet
1. Separacja konfiguracji
2. Konfigurowalne wymiary wykresów
3. Retry logic
4. Kategoryzacja błędów
5. Loading indicator
6. Responsywność mobile
7. Docker support
8. CI/CD Pipeline
9. Health check endpoint
10. Error tracking

### 🟢 Niski priorytet
1. Wybór zakresu dat
2. Eksport wykresów
3. Testy wydajnościowe
4. Lepsze wyświetlanie błędów
5. Dark mode
6. API Documentation
7. Rozszerzenie README
8. Prometheus metrics

---

## 11. Szacowane nakłady pracy

| Kategoria | Nakład (person-days) |
|-----------|---------------------|
| Architektura (Service Layer, Config Manager) | 2-3 dni |
| Cache i optymalizacja | 1-2 dni |
| Bezpieczeństwo (rate limiting, validation) | 1-2 dni |
| Testy (pokrycie >80%, integracyjne) | 2-3 dni |
| Logowanie i monitoring | 1 dzień |
| Docker i CI/CD | 1-2 dni |
| UI/UX (responsive, loading) | 1-2 dni |
| **RAZEM (high + medium priority)** | **9-15 dni** |

---

## 12. Zalecenia końcowe

1. **Rozpocznij od testów**: Zwiększenie pokrycia testami ułatwi refaktoryzację
2. **Implementuj stopniowo**: Nie próbuj wszystkiego na raz
3. **Zachowaj kompatybilność wsteczną**: Szczególnie w API i konfiguracji
4. **Dokumentuj zmiany**: Aktualizuj CHANGELOG.md dla każdej nowej funkcjonalności
5. **Code review**: Wszystkie zmiany powinny przejść przez review
6. **Monitoring**: Dodaj metryki przed wdrożeniem na produkcję

---

**Koniec dokumentu**
