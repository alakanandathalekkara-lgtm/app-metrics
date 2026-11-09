# App metrics with Prometheus and Grafana

A Flask app instrumented with `prometheus_client`, scraped by Prometheus and shown
in a pre-provisioned Grafana dashboard.

## Metrics
- `http_requests_total{method,endpoint,status}` (counter)
- `http_request_duration_seconds{endpoint}` (histogram)

## Dashboard panels
- Request rate: `sum(rate(http_requests_total[1m])) by (endpoint)`
- Latency p95: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`
- Error rate: `100 * sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))`

## Run
    cp .env.example .env     # then set a real Grafana password
    docker compose up -d --build

- App: http://localhost:5000 (`/metrics` for Prometheus)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (user `admin`)

A `loadgen` container sends constant traffic. About 10% of `/work` calls fail on
purpose, so the error-rate panel has data.
