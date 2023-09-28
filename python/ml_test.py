import joblib
import datetime

loaded_model = joblib.load("./python/random_forest_model.pkl")

while True:
    data_arr= []
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    formatted_time = current_time.strftime('%H:%M:%S')

    time_parts = formatted_time.split(":")
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    sek = int(time_parts[2])

    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year 

    if sek == 0 and minute == 0:
        
        i = 0
        for i in range(60):
            new_data = [[2023, 9, 21, hour+1, i, 2017, 12, 21, 0, 1, 1, 0, 1, 0, 1]]
            predictions = loaded_model.predict(new_data)
            predictions = predictions[0]  
            data_arr.append(predictions)
        if len(data_arr) != 0:
            print(max(data_arr))

    
        

