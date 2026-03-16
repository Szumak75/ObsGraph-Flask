# ObsGraph-Flask Improvement Proposals

**Analysis date**: 2025-12-05  
**Project version**: 0.1.0  
**Analysis author**: ObsGraph Team

---

## 1. Architecture and Code Structure

### Current Strengths

- Consistent use of JskToolBox patterns such as `BData`, `ReadOnlyClass`, and
  `Raise`
- Clear separation between business logic (`ObsGraphApp`) and presentation
  logic (Flask routes)
- Static typing across the codebase
- Clean top-level directory layout with `lib/`, `templates/`, and `tools/`

### Proposed Improvements

#### 1.1. Extract Configuration Management

**Priority**: Medium

Move configuration loading, validation, and decryption into a dedicated class.

```python
# obsgraph_flask/lib/config_manager.py
class ConfigManager(BData):
    """Manage application configuration with validation and decryption."""

    def __init__(self, config_path: str) -> None:
        # Configuration loading and validation logic
        pass

    @property
    def observium_url(self) -> str:
        ...

    @property
    def api_credentials(self) -> Tuple[str, str]:
        """Return a tuple of login and decrypted password."""
        ...
```

Benefits:

- Better testability
- Easier reuse from CLI tools or future services
- Cleaner migration path if the configuration source changes later

#### 1.2. Introduce an Observium Service Layer

**Priority**: High

Move all Observium communication into a dedicated service object.

```python
# obsgraph_flask/services/observium_service.py
class ObserviumService:
    """Handle communication with the Observium API."""

    def __init__(self, base_url: str, auth: Tuple[str, str]) -> None:
        self.base_url = base_url
        self.auth = auth
        self.session = requests.Session()

    def get_multi_port_graph(
        self,
        port_ids: str,
        start_ts: int,
        end_ts: int,
        width: int = 1024,
        height: int = 600,
    ) -> Optional[bytes]:
        """Fetch a graph image from Observium."""
        ...

    def get_device_list(self) -> List[Dict]:
        """Fetch a device list from Observium."""
        ...
```

Benefits:

- Easier addition of future Observium API endpoints
- Better HTTP session reuse
- Simpler unit testing without going through Flask

---

## 2. Functionality

### Proposed Enhancements

#### 2.1. Configurable Chart Dimensions

**Priority**: Medium

This feature already exists in the current implementation and should remain a
first-class documented capability.

```ini
[ObsGraphFlaskApp]
graph_width = 1024
graph_height = 600
```

#### 2.2. Chart Caching

**Priority**: High

Add a cache layer for downloaded graph images.

```python
from datetime import datetime, timedelta

class ObsGraphApp(BData):
    def __init__(self) -> None:
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

Benefits:

- Lower load on Observium
- Faster response times
- Less repeated network traffic

#### 2.3. Custom Date Range Selection

**Priority**: Low

Allow the user to select an explicit start and end date instead of a calendar
month only.

```html
<input type="date" name="start_date" />
<input type="date" name="end_date" />
```

#### 2.4. Chart Export

**Priority**: Low

Add an endpoint that returns the rendered chart as a downloadable PNG file.

```python
@app.route("/export/<year>/<month>")
def export_chart(year: int, month: int) -> Response:
    """Export a chart as a PNG file."""
    chart_data = obs_app.get_observium_charts(year, month)
    # Decode base64 and return as file
    ...
```

---

## 3. Error Handling and Logging

### Proposed Improvements

#### 3.1. Structured Logging

**Priority**: High

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

Usage:

```python
logger.info(
    "Fetching chart",
    extra={"year": year, "month": month, "port_ids": port_ids},
)
```

#### 3.2. Retry Logic for API Calls

**Priority**: Medium

```python
from tenacity import retry, stop_after_attempt, wait_exponential

class ObserviumService:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_multi_port_graph(self, ...) -> Optional[bytes]:
        ...
```

#### 3.3. Error Categorization

**Priority**: Medium

```python
class ObsGraphError(Exception):
    """Base exception for ObsGraph errors."""


class ConfigurationError(ObsGraphError):
    """Configuration-related errors."""


class APIError(ObsGraphError):
    """Observium API communication errors."""
```

---

## 4. Testing

### Current State

- Core route tests are present
- Timestamp calculations are covered
- Configuration and configurator flows are covered

### Proposed Improvements

#### 4.1. Integration Tests with API Mocking

**Priority**: High

```python
# tests/test_integration.py
@responses.activate
def test_successful_chart_retrieval() -> None:
    """Test end-to-end chart retrieval with a mocked API."""
    responses.add(
        responses.GET,
        "https://observium.example.com/graph.php",
        body=b"fake_image_data",
        status=200,
        content_type="image/png",
    )

    with app.test_client() as client:
        response = client.post("/", data={"year": "2025", "month": "11"})
        assert b"data:image/png;base64," in response.data
```

#### 4.2. Performance Tests

**Priority**: Low

```python
# tests/test_performance.py
def test_response_time_under_2_seconds() -> None:
    """Ensure the page loads within an acceptable time."""
    with app.test_client() as client:
        start = time.time()
        response = client.get("/")
        duration = time.time() - start

        assert duration < 2.0
        assert response.status_code == 200
```

#### 4.3. Coverage Above 80 Percent

**Priority**: High

Coverage should be measured regularly and expanded where gaps remain.

```bash
poetry run pytest --cov=obsgraph_flask --cov-report=term-missing
```

---

## 5. UI and UX

### Proposed Improvements

#### 5.1. Loading Indicator

**Priority**: Medium

Add a visible loading state while the chart request is being processed.

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

#### 5.2. Better Error Presentation

**Priority**: Low

Group errors visually by type.

```html
<div class="error-item error-config">
    <span class="icon">Config</span>
    <span class="message">Configuration error: ...</span>
</div>

<div class="error-item error-network">
    <span class="icon">Network</span>
    <span class="message">Network error: ...</span>
</div>
```

#### 5.3. Dark Mode

**Priority**: Low

Add an optional alternate theme if the application is expected to stay open on
wall displays or operator dashboards for long periods.
