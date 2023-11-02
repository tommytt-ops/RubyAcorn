from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import time

antall_server_metric = Gauge('antall_server', ['title'])
antall_replica_metric = Gauge('antall_replica', ['title'])

start_http_server(8000)

def test():

    antall_server = 1.0
    antall_replica = 2.0

    antall_server_metric.labels(title="x").set(antall_server)
    antall_replica_metric.labels(title="y").set(antall_replica)

    custom_metrics = generate_latest(REGISTRY)

    


    return custom_metrics

while True:
    test()
    time.sleep(60)