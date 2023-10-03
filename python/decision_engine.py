import joblib
import requests
import datetime
import time
import re
import random

from Utils import prometheus_player_count_fetch, max_player_per_hour

loaded_model = joblib.load("./python/PUBG_week_random_forest_model.pkl")
server_capacit = 50000

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


    if sec == 0 and min % 1 == 0:

        print(max_player_per_hour(year, month, day, hour, loaded_model, data_arr))

        time.sleep(10)
        
   

    
