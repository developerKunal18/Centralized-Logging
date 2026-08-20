# Centralized Logging

Flask service with structured JSON logging and Loki/Grafana.

## Run

```bash
docker compose up --build
```

API: http://localhost:5000
Grafana: http://localhost:3000
Loki: http://localhost:3100

Grafana default login:

```text
admin
admin
```

Logs are available in Grafana through the preconfigured Loki data source.

Query:

```text
{service="day305-api"}
```

Generate logs:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/error
```

Stop:

```bash
docker compose down
```

Day 305 / 365
