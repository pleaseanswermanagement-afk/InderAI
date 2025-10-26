from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
REQ_COUNTER = Counter('inderai_requests_total', 'Total requests', ['endpoint'])

def inc(endpoint):
    try:
        REQ_COUNTER.labels(endpoint=endpoint).inc()
    except Exception:
        pass

def metrics_endpoint():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
