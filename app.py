import random
import time

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency in seconds", ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        # use the route pattern, not the raw path, to keep label cardinality low
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        LATENCY.labels(endpoint).observe(time.time() - request.start_time)
        REQUESTS.labels(request.method, endpoint, response.status_code).inc()
    return response


@app.route("/")
def home():
    return "Metrics demo app\n"


@app.route("/work")
def work():
    time.sleep(random.uniform(0.05, 0.6))
    if random.random() < 0.10:
        return jsonify(error="simulated failure"), 500
    return jsonify(status="ok")


@app.route("/health")
def health():
    return jsonify(status="UP")


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
