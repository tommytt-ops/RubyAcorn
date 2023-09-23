import joblib
import requests
import datetime
import time


while True:
    url = 'http://10.196.36.11/metrics'  # Replace with the URL you want to post to
    data = {'key': 'value'}  # Replace with your data
    response = requests.get(url, data=data)

    if response.status_code == 200:
        # Split the response content into lines
        lines = response.text.split('\n')
    
        # Iterate through the lines and filter data for the desired title
        for line in lines:
            if 'PLAYERUNKNOWNS BATTLEGROUNDS' in line:
                print(line)
    else:
        print(f'Error: {response.status_code}')

    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    formatted_time = current_time.strftime('%H:%M:%S')
    print(formatted_time)

    time_parts = formatted_time.split(":")
    hour = int(time_parts[0])
    minute = int(time_parts[1])


    loaded_model = joblib.load("./python/random_forest_model.pkl")

    # Preprocess input data (e.g., format it as a NumPy array)
    new_data = [[2023, 9, 21, hour, minute, 2017, 12, 21, 0, 1, 1, 0, 1, 0, 1]]

    # Use the model for predictions
    predictions = loaded_model.predict(new_data)

    print(predictions)
    time.sleep(5)