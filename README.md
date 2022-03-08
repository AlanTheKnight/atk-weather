# ATK Weather

![Preview](preview.png)

Install dependencies

```bash
poetry install
```

Create ``config.toml`` with the following content:

```toml
[settings]
token = "<OpenWeatherMap API token>"
city = "<any city>"
```

Run the app

```bash
poetry run python main.py
```
