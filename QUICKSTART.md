# ObsGraph-Flask Quick Start

## Development

### 1. Install dependencies

```bash
cd ObsGraph-Flask
poetry install
```

### 2. Configure the application

Use the CLI directly:

```bash
poetry run python obsgraph_flask/tools/obsgraph_configurator.py \
  --url "https://observium.example.com/" \
  --login "api" \
  --password "your_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677" \
  --width 1024 \
  --height 600
```

Or use the wrapper:

```bash
./bin/osbgraph-config.sh \
  --url "https://observium.example.com/" \
  --login "api" \
  --password "your_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677"
```

### 3. Run the application

Development server:

```bash
poetry run python obsgraph_flask/app.py
```

Development Gunicorn run:

```bash
poetry run gunicorn --config gunicorn.conf.py "obsgraph_flask.wsgi:app"
```

## Production

### 1. Create the production virtual environment

```bash
./bin/osbgraph-config.sh \
  --url "https://observium.example.com/" \
  --login "api" \
  --password "your_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677"
```

This creates `.venv-prod`, installs runtime dependencies, and updates
`etc/obsgraph.conf`.

### 2. Start Gunicorn without Poetry

```bash
./bin/osbgraph-start.sh
```

Example with explicit bind:

```bash
./bin/osbgraph-start.sh --bind 0.0.0.0:8123
```

### 3. Run with systemd

Copy the sample unit:

```bash
sudo cp etc/systemd/obsgraph-flask.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now obsgraph-flask.service
```

Check service status:

```bash
sudo systemctl status obsgraph-flask.service
sudo journalctl -u obsgraph-flask.service -n 50 --no-pager
```

## Reverse Proxy Notes

The application can be published:

- on its own host name
- under a subpath such as `/flow/`

The HTML form posts back to the current URL, so reverse proxying under a
subpath works without additional application changes.

Example Nginx snippet:

```nginx
location /flow/ {
    proxy_pass http://backend-host:8123/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Test and Validation Commands

```bash
poetry run pytest
poetry run pytest --cov=obsgraph_flask --cov-report=html
poetry run mypy obsgraph_flask/
poetry run black .
poetry run isort .
poetry run pycodestyle obsgraph_flask/
```

## Minimal Project Structure

```text
obsgraph_flask/
├── app.py
├── wsgi.py
├── lib/
│   └── keys.py
├── templates/
│   └── index.html
└── tools/
    └── obsgraph_configurator.py

bin/
├── osbgraph-config.sh
└── osbgraph-start.sh

etc/
├── obsgraph.conf
└── systemd/obsgraph-flask.service
```
