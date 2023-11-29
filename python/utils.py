import re
import requests
import math
import xgboost
import pandas
from linux_scripts.linux_scripts import start_servers, stop_servers

def prometheus_player_count_fetch(game_title):
 
    url = 'http://10.196.36.11/metrics'  
    data = {'key': 'value'}  
    response = requests.get(url, data=data)

    if response.status_code == 200:

        lines = response.text.split('\n')
        for line in lines:
            if game_title in line:
                match = re.search(r'\d+$', line)
                number = match.group()
                return number
    else:
        print(f'Error: {response.status_code}')

def max_player_per_hour(year, month, day, hour, loaded_model, data_arr):

    i = 0
    model = loaded_model
    for i in range(59):
        new_data = pandas.DataFrame([[year, month, day, hour, i]])
        new_data = xgboost.DMatrix(new_data)
        predictions = model.predict(new_data)
        predictions = predictions[0]  
        data_arr.append(predictions)       

    if len(data_arr) != 0:
        return(max(data_arr))

def desired_instances(instance_capacity, predicted_max_hour_player_count):

    player_count = predicted_max_hour_player_count / instance_capacity
    desired_isinstance = max(math.ceil(player_count),1)

    return desired_isinstance



def scaler(desiered_instance, current_instances):
    
    if desiered_instance > current_instances:
        start_servers(desiered_instance, current_instances)

    elif desiered_instance < current_instances:
        stop_servers(desiered_instance, current_instances)
    

