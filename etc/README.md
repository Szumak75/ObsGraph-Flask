# ObsGraph-Flask Configuration

## Configuration File: `obsgraph.conf`

Konfiguracja aplikacji przechowywana w formacie INI.

### Struktura pliku

```ini
[ObsGraphFlaskApp]
# Salt value używany do szyfrowania/deszyfrowania haseł
salt = 123

# URL bazowy instancji Observium (z końcowym /)
observium_url = "https://observium.local/"

# Login do API Observium
api_login = "api_user_name"

# Zaszyfrowane hasło API (użyj SimpleCrypto.multiple_encrypt)
api_password = "encrypted_api_password"

# ID portów do wykresów (rozdzielone przecinkami)
port_ids = "496,508"

# Wymiary wykresów w pikselach
graph_width = 1024
graph_height = 600
```

### Parametry

#### `salt` (int, wymagany)
Wartość salt używana przez `SimpleCrypto` z `jsktoolbox` do szyfrowania i deszyfrowania haseł.

#### `observium_url` (str, wymagany)
Pełny URL bazowy instancji Observium. Musi kończyć się znakiem `/`.

Przykład: `"https://observium.example.com/"`

#### `api_login` (str, wymagany)
Nazwa użytkownika API Observium.

#### `api_password` (str, wymagany)
Zaszyfrowane hasło API. Hasło musi być zaszyfrowane przy użyciu:
```python
from jsktoolbox.stringtool import SimpleCrypto
encrypted = SimpleCrypto.multiple_encrypt(salt_value, "plain_password")
```

#### `port_ids` (str, wymagany)
Lista ID portów rozdzielona przecinkami, dla których będą generowane wykresy multi-port.

Przykład: `"496,508"` lub `"100,200,300"`

### Konfiguracja przy użyciu CLI

Użyj narzędzia `./bin/obsgraph-config.sh`:

```bash
./bin/obsgraph-config.sh \
  --url "https://observium.example.com" \
  --login "api_user" \
  --password "plain_password" \
  --ids "496,508"
```

Narzędzie automatycznie:
- Wygeneruje wartość salt
- Zaszyfruje hasło
- Zapisze konfigurację do pliku

### Walidacja konfiguracji

Aplikacja sprawdza obecność wszystkich wymaganych kluczy podczas uruchamiania:
- `salt`
- `observium_url`
- `api_login`
- `api_password`
- `port_ids`

Brakujące klucze są zgłaszane jako błędy w interfejsie użytkownika.
