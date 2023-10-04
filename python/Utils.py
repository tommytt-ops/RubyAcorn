import re
import requests
import math
from linux_scripts.linux_scripts import start_servers, stop_servers

def prometheus_player_count_fetch():
 
    url = 'http://10.196.36.11/metrics'  # Replace with the URL you want to post to
    data = {'key': 'value'}  # Replace with your data
    response = requests.get(url, data=data)

    if response.status_code == 200:
        # Split the response content into lines
        lines = response.text.split('\n')
    
        # Iterate through the lines and filter data for the desired title
        for line in lines:
            if 'PLAYERUNKNOWNS BATTLEGROUNDS' in line:
                match = re.search(r'\d+$', line)
                number = match.group()
                return number
    else:
        print(f'Error: {response.status_code}')

def max_player_per_hour(year, month, day, hour, loaded_model, data_arr):

    i = 0
    for i in range(11):
        new_data = [[year, month, day, hour, i*5]]
        predictions = loaded_model.predict(new_data)
        predictions = predictions[0]  
        data_arr.append(predictions)       

    if len(data_arr) != 0:
        return(max(data_arr))

def desired_instances(instance_capacity, predicted_max_hour_player_count):
    
    instance_capacity = 500000
    predicted_max_hour_player_count = 2522578

    player_count = predicted_max_hour_player_count / instance_capacity
    desired_isinstance = max(math.ceil(player_count),1)

    return desired_isinstance



def scaler(desiered_instance, current_instances):
    
    if desiered_instance > current_instances:

        start_servers(desiered_instance, current_instances)

    elif desiered_instance < current_instances:

        stop_servers(desiered_instance)
    

