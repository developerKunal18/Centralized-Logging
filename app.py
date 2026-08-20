import json
import logging
import sys
import time
import uuid

from flask import Flask, g, jsonify, request

app = Flask(__name__)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime(record.created),
            ),
            "level": record.levelname,
            "service": "day305-api",
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None)
        if request_id:
            data["request_id"] = request_id

        return json.dumps(data)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

app.logger.handlers.clear()
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


@app.before_request
def before_request():
    g.request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4()),
    )
    g.started_at = time.perf_counter()

    app.logger.info(
        "request_started",
        extra={"request_id": g.request_id},
    )


@app.after_request
def after_request(response):
    duration_ms = round(
        (time.perf_counter() - g.started_at) * 1000,
        2,
    )

    app.logger.info(
        f"request_completed method={request.method} "
        f"path={request.path} status={response.status_code} "
        f"duration_ms={duration_ms}",
        extra={"request_id": g.request_id},
    )

    response.headers["X-Request-ID"] = g.request_id
    return response


@app.get("/")
def home():
    return jsonify(
        service="day305-api",
        message="Centralized logging demo",
    )


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/ready")
def ready():
    return jsonify(status="ready")


@app.get("/error")
def error():
    app.logger.error(
        "demo_error",
        extra={"request_id": g.request_id},
    )
    return jsonify(error="demo error"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
