# ObsGraph-Flask Configuration Reference

## Configuration File

The application reads `etc/obsgraph.conf` in INI format.

Example:

```ini
[ObsGraphFlaskApp]
salt = 123456789
observium_url = "https://observium.example.com/"
api_login = "api_user"
api_password = "encrypted_api_password"
port_header1 = "TASK"
port_header2 = "Office"
port_ids1 = "496,508"
port_ids2 = "677"
graph_width = 1024
graph_height = 600
```

## Parameters

### Required Parameters

#### `salt`

Integer salt used by `SimpleCrypto` to encrypt and decrypt the stored API
password.

#### `observium_url`

Base URL of the Observium instance. Use a trailing slash to keep the generated
graph URLs predictable.

Example:

```ini
observium_url = "https://observium.example.com/"
```

#### `api_login`

Observium API user name.

#### `api_password`

Encrypted Observium API password. Generate it through the configurator or by
calling `SimpleCrypto.multiple_encrypt`.

Example:

```python
from jsktoolbox.stringtool import SimpleCrypto

encrypted_password = SimpleCrypto.multiple_encrypt(salt_value, "plain_password")
```

#### `port_header1`, `port_header2`

Section headers displayed above the first and second chart.

#### `port_ids1`, `port_ids2`

Port identifiers used to build chart requests.

- One port ID produces a `port_bits` graph.
- Multiple comma-separated port IDs produce a `multi-port_bits` graph.

Examples:

```ini
port_ids1 = "677"
port_ids2 = "496,508"
```

### Optional Parameters

#### `graph_width`

Chart width in pixels. Default: `1024`.

#### `graph_height`

Chart height in pixels. Default: `600`.

## Configuration with the CLI Wrapper

Use the shell wrapper when preparing a production host:

```bash
./bin/osbgraph-config.sh \
  --url "https://observium.example.com/" \
  --login "api_user" \
  --password "plain_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Office" \
  --ids2 "677" \
  --width 1024 \
  --height 600
```

The wrapper:

- creates `.venv-prod` when missing
- installs packages from `requirements.txt`
- runs the Python configurator
- updates `etc/obsgraph.conf`

## Validation Performed by the Application

During startup the application checks the presence of these required keys:

- `salt`
- `observium_url`
- `api_login`
- `api_password`
- `port_header1`
- `port_header2`
- `port_ids1`
- `port_ids2`

Missing values are reported in the web UI footer.

## Runtime Notes

- The configuration file is loaded once when the application process starts.
- After editing `etc/obsgraph.conf`, restart Gunicorn or the `systemd` service.
- If the application runs behind a reverse proxy under a subpath such as
  `/flow/`, no special configuration is required in `obsgraph.conf`.
