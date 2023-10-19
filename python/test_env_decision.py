
import datetime
import time
import xgboost
from docker_tester import docker_instance
from Utils import prometheus_player_count_fetch, max_player_per_hour, desired_instances, scaler
from linux_scripts.linux_scripts import server_list

loaded_model = xgboost.Booster()
loaded_model.load_model("./python/reg_model.json")
instance_capacity = 500000
docker_instance_capacity = 21500
predict_max_player = 0

while True:

    data_arr = []
    current_players = prometheus_player_count_fetch("PLAYERUNKNOWNS BATTLEGROUNDS")

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
   
     

    if  sec == 0:

        predict_max_player = 0
        predict_max_player = max_player_per_hour(year, month, day, hour, loaded_model, data_arr)
        print(hour)
        print("predicted: ", predict_max_player)
        print("current players: ",current_players)
        print("")

        if predict_max_player != 0:

            desired_instances_to_run = desired_instances(instance_capacity, predict_max_player)
            current_instances_running = len(server_list("ACTIVE")) -1
            print(desired_instances_to_run)
            print(current_players)
            scaler(desired_instances_to_run, current_instances_running)
            print("given servers: ",  desired_instances(instance_capacity, predict_max_player))
            docker_instance(predict_max_player, docker_instance_capacity)
            print("")
            time.sleep(60)

    if current_players is not None and predict_max_player != 0:
   
        if (len(server_list("ACTIVE"))-1) * instance_capacity < int(current_players) and predict_max_player != 0 and min != 0 and min % 5 == 0:

            print("need more servers")
            print(f"{hour}:{min}")
            print(predict_max_player)
            print(current_players)
            print("")
            desired_instances_to_run = desired_instances(instance_capacity, int(current_players))
            current_instances_running = len(server_list("ACTIVE")) -1
            scaler(desired_instances_to_run, current_instances_running)
            time.sleep(60)
        


        #Doesnt fit the goal of the algorithm 
        #elif (len(server_list("ACTIVE"))-2) * instance_capacity > int(current_players) and predict_max_player != 0 and min != 0 and min % 5 == 0:
            
            #print("need fewer servers")
            #print(f"{hour}:{min}")
            #print(predict_max_player)
            #print(current_players)
            #print("")
            #desired_instances_to_run = desired_instances(instance_capacity, int(current_players))
            #current_instances_running = len(server_list("ACTIVE")) -1
            #scaler(desired_instances_to_run, current_instances_running)
    
    
        
   

    
