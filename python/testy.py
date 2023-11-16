from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import datetime
import time
import xgboost
import math
from docker_tester import docker_instance, get_replica_count
from Utils import prometheus_player_count_fetch, max_player_per_hour, desired_instances, scaler
from linux_scripts.linux_scripts import server_list
from prom_metrics_ import prom_metrics
import asyncio
import aiohttp
from linux_scripts.linux_scripts import start_servers, stop_servers
from utilsAsync import get_replica_count_async, docker_instance_async, desired_instances_async

predict_max_player = 0
instance_capacity = 250000
docker_instance_capacity = 1000
loaded_model = xgboost.Booster()
loaded_model.load_model("./python/reg_model_valve.json")
data_arr = []

predict_max_player = max_player_per_hour(2023, 11, 16, 16, loaded_model, data_arr)
print(predict_max_player)