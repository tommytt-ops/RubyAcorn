import joblib
import requests
import datetime
import random

loaded_model = joblib.load("./python/random_forest_model.pkl")


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
               # print(line)
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
    sek = int(time_parts[2])


    if sek == 0 and min % 2 == 0:
        
        i = 0
        for i in range(60):
            new_data = [[2023, 9, day, random.randint(0, 23), i, 2017, 12, 21, 0, 1, 1, 0, 1, 0, 1]]
            predictions = loaded_model.predict(new_data)
            predictions = predictions[0]  
            data_arr.append(predictions)

    if len(data_arr) != 0:
        print(max(data_arr))
        data_arr = []

    
