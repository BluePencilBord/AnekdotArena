from prometheus_client import Counter, Histogram, start_http_server

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
    start_http_server(port)
