import joblib
import requests
import datetime
import time
import re
import random
import xgboost

from Utils import prometheus_player_count_fetch, max_player_per_hour, desired_instances, scaler
from linux_scripts.linux_scripts import server_list

loaded_model = xgboost.Booster()
loaded_model.load_model("./python/reg_model.json")
instance_capacity = 500000
predict_max_player = 0

while True:

    data_arr = []
    current_players = prometheus_player_count_fetch()

    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    formatted_time = current_time.strftime('%H:%M:%S')

    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year    

    time_parts = formatted_time.split(":")
    hour = int(time_parts[0])
    min = int(time_parts[1])
    sec = int(time_parts[2])

    if sec == 0 and min == 0:

        predict_max_player = 0
        predict_max_player = max_player_per_hour(year, month, day, hour, loaded_model, data_arr)
        desired_instances(instance_capacity, predict_max_player)
        print(f"{hour}:{min}")
        print("predicted: ", predict_max_player)
        print("current players: ",current_players)
        print("given servers: ", desired_instances)
        print("")
        time.sleep(10)