


# Config

In your own project, there should be a `settings.toml` and a `.env` file.

- `settings.toml` stores the common config.  
    - To use connections module, `[default.db]` is a must.
- `.env` stores secret things like passwords.

# Usage


## connections module

mysqldb connection example toml:

```toml
[default.db]
host = "replace with your host"
port = 3306
user = "root"
password = "@format {env[MYSQLDB_PASSWORD]}"
```

Usage in your code:

```python

from xchtools import XCHConnections
xc = XCHConnections(os.path.dirname(os.path.abspath(__file__)))
config = xc.settings
print(config.db)

xc.sql2df("show databases")
```





# For developer

## Build and Release

1. Config pypi API token `poetry config pypi-token.pypi <token>`
2. `poetry build`
3. `poetry publish`
