import logging
from prometheus_client import Counter, Histogram, start_http_server

# Настроим логирование, если оно еще не настроено в main.py
# logging.basicConfig(level=logging.INFO) # Возможно, это уже есть в main.py

logger = logging.getLogger(__name__)

processed_messages_total = Counter(
    "processed_messages_total", "Total number of processed messages"
)

command_response_time_seconds = Histogram(
    "command_response_time_seconds",
    "Time spent processing commands",
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
        float("inf"),
    ),
)


def start_metrics_server(port: int = 8000):
    """
    Starts a simple HTTP server to expose Prometheus metrics.
    """
    try:
        start_http_server(port)
        logger.info(f"Prometheus metrics server started successfully on port {port}")
    except Exception as e:
        logger.error(f"Failed to start Prometheus metrics server on port {port}: {e}")
