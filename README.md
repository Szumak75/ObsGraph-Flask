# ObsGraph-Flask

ObsGraph-Flask is a small Flask application that renders monthly traffic charts
fetched from the Observium graph endpoint. It is designed to run behind
Gunicorn and an HTTP reverse proxy and to be configured through a dedicated CLI
tool.

## What the application does

- Displays two configurable Observium traffic charts for a selected year and
  month.
- Fetches graph images from Observium over HTTP Basic authentication.
- Stores the Observium password in encrypted form inside `etc/obsgraph.conf`.
- Shows backend and configuration errors directly in the web UI.

## Architecture Summary

- Web framework: Flask
- WSGI server: Gunicorn
- Runtime Python: 3.11+
- Dependency manager for development: Poetry
- Production runtime: pre-created virtual environment, no Poetry required
- Reverse proxy model: standalone virtual host or subpath such as `/flow/`

## Main Components

- [`obsgraph_flask/app.py`](obsgraph_flask/app.py)
  contains the Flask application, configuration loading, Observium requests,
  and chart generation flow.
- [`obsgraph_flask/wsgi.py`](obsgraph_flask/wsgi.py)
  provides the WSGI entry point for Gunicorn.
- [`obsgraph_flask/tools/obsgraph_configurator.py`](obsgraph_flask/tools/obsgraph_configurator.py)
  updates the configuration file and encrypts the API password.
- [`bin/osbgraph-config.sh`](bin/osbgraph-config.sh)
  prepares the production virtual environment and runs the configurator.
- [`bin/osbgraph-start.sh`](bin/osbgraph-start.sh)
  starts Gunicorn from `.venv-prod`.
- [`etc/systemd/obsgraph-flask.service`](etc/systemd/obsgraph-flask.service)
  contains a sample `systemd` unit for Linux deployments.

## Configuration Model

The application reads `etc/obsgraph.conf` with the main section
`[ObsGraphFlaskApp]`.

Required values:

- `salt`
- `observium_url`
- `api_login`
- `api_password`
- `port_header1`
- `port_header2`
- `port_ids1`
- `port_ids2`

Optional values:

- `graph_width` default `1024`
- `graph_height` default `600`

`port_ids1` and `port_ids2` drive chart type selection:

- one ID results in `port_bits`
- multiple comma-separated IDs result in `multi-port_bits`

See [`etc/README.md`](etc/README.md)
for the full configuration reference.

## Development Setup

Install dependencies with Poetry:

```bash
git clone <repository-url>
cd ObsGraph-Flask
poetry install
```

Configure the application:

```bash
poetry run python obsgraph_flask/tools/obsgraph_configurator.py \
  --url "https://observium.example.com/" \
  --login "api_user" \
  --password "api_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677" \
  --width 1024 \
  --height 600
```

Run the development server:

```bash
poetry run python obsgraph_flask/app.py
```

## Production Deployment

Production deployment does not require Poetry on the target host.

### 1. Prepare the runtime environment

```bash
./bin/osbgraph-config.sh \
  --url "https://observium.example.com/" \
  --login "api_user" \
  --password "api_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677"
```

This script:

- creates `.venv-prod` if needed
- installs runtime dependencies from `requirements.txt`
- updates `etc/obsgraph.conf`

### 2. Start Gunicorn

```bash
./bin/osbgraph-start.sh
```

Override bind address or workers when needed:

```bash
./bin/osbgraph-start.sh --bind 0.0.0.0:8123 --workers 4
```

The wrapper always uses [`gunicorn.conf.py`](gunicorn.conf.py)
as the baseline configuration.

### 3. Run under systemd

Use the sample unit from
[`etc/systemd/obsgraph-flask.service`](etc/systemd/obsgraph-flask.service)
and adjust at least:

- `User`
- `Group`
- `WorkingDirectory`
- `ExecStart`

Install it on the host:

```bash
sudo cp etc/systemd/obsgraph-flask.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now obsgraph-flask.service
```

### 4. Place it behind a reverse proxy

ObsGraph-Flask works both:

- on a dedicated virtual host
- on a URL subpath such as `/flow/`

The HTML form was adjusted to post back to the current URL, so subpath proxying
is supported without rewriting the form action to `/`.

Example Nginx location:

```nginx
location /flow/ {
    proxy_pass http://10.0.0.20:8123/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

If the backend is reachable over a routed network, expose the Gunicorn port only
to the reverse proxy and not to the public Internet.

## Testing and Quality Checks

Run the test suite:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=obsgraph_flask --cov-report=html
```

Static analysis and formatting:

```bash
poetry run mypy obsgraph_flask/
poetry run black .
poetry run isort .
poetry run pycodestyle obsgraph_flask/
```

## Project Layout

```text
ObsGraph-Flask/
├── bin/
│   ├── osbgraph-config.sh
│   └── osbgraph-start.sh
├── etc/
│   ├── obsgraph.conf
│   ├── systemd/
│   │   └── obsgraph-flask.service
│   └── README.md
├── obsgraph_flask/
│   ├── app.py
│   ├── wsgi.py
│   ├── lib/
│   │   └── keys.py
│   ├── templates/
│   │   └── index.html
│   └── tools/
│       └── obsgraph_configurator.py
├── tests/
├── gunicorn.conf.py
├── pyproject.toml
└── QUICKSTART.md
```

## Notes

- The shell wrappers intentionally use the historical `osbgraph-*` naming kept
  by the repository.
- The project documentation is written in English; code comments and docstrings
  should remain in English as well.
- Development follows TDD: write the failing test first, then implement, then
  refactor.

## License

MIT
