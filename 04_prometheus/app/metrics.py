from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

RESPONSE_TIME = Histogram(
    "http_response_time_seconds",
    "Response time in seconds",
    ["method", "endpoint"]
)

CUSTOM_METRIC = Counter(
    "custom_metric_total",
    "Custom metric example"
)