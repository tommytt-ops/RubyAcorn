from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import time

async def prom_metrics(antall, prom, title):
    prom.labels(title=title).set(antall)
   