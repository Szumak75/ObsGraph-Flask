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

# Nagłówki wykresów
port_header1 = "TASK"
port_header2 = "Biuro"

# ID portów do wykresów
port_ids1 = "496,508"
port_ids2 = "677"

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

#### `port_header1` / `port_header2` (str, wymagane)
Nagłówki wyświetlane nad pierwszym i drugim wykresem.

#### `port_ids1` / `port_ids2` (str, wymagane)
Lista ID portów dla odpowiedniego wykresu.

- Jeśli wartość zawiera pojedynczy identyfikator, aplikacja generuje wykres `port_bits`.
- Jeśli wartość zawiera listę rozdzieloną przecinkami, aplikacja generuje wykres `multi-port_bits`.

Przykłady: `"677"` albo `"496,508"`

### Konfiguracja przy użyciu CLI

Użyj narzędzia `./bin/obsgraph-config.sh`:

```bash
./bin/obsgraph-config.sh \
  --url "https://observium.example.com" \
  --login "api_user" \
  --password "plain_password" \
  --header1 "TASK" \
  --ids1 "496,508" \
  --header2 "Biuro" \
  --ids2 "677"
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
- `port_header1`
- `port_header2`
- `port_ids1`
- `port_ids2`

Brakujące klucze są zgłaszane jako błędy w interfejsie użytkownika.
