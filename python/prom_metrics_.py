from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import time

antall_server_metric = Gauge('antall_server', 'Description of antall_server', ['title'])
antall_replica_metric = Gauge('antall_replica', 'Description of antall_replica', ['title'])

start_http_server(8000)

def prom_metrics(antall_server, antall_replica, antall_server_metric_prom, antall_replica_metric_prom, game_title):

    antall_server_metric_prom.labels(title=game_title).set(antall_server)
    antall_replica_metric_prom.labels(title=game_title).set(antall_replica)