import joblib
import requests
import datetime
import time
import re
import random

loaded_model = joblib.load("./python/PUBG_week_random_forest_model.pkl")

while True:
    
    data_arr = []
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
                print(number)
                uio = 1
    else:
        print(f'Error: {response.status_code}')

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
        
        i = 0
        for i in range(12):
            new_data = [[2023, month, day, hour, i]]
            predictions = loaded_model.predict(new_data)
            predictions = predictions[0]  
            data_arr.append(predictions)       

    if len(data_arr) != 0:
        print(max(data_arr))
        time.sleep(10)
    
