import math
import xgboost
import pandas
from linux_scripts.linux_scripts import start_servers, stop_servers
import math
import docker
import asyncio
import aiodocker


async def max_player_per_hour_async(year, month, day, hour, loaded_model, data_arr):
    i = 0
    model = loaded_model
    for i in range(59):
        new_data = pandas.DataFrame([[year, month, day, hour, i]])
        new_data = xgboost.DMatrix(new_data)
        predictions = model.predict(new_data)
        predictions = predictions[0]  
        data_arr.append(predictions)       

    if len(data_arr) != 0:
        return max(data_arr)

async def desired_instances_async(instance_capacity, predicted_max_hour_player_count):
    player_count = predicted_max_hour_player_count / instance_capacity
    desired_instance = max(math.ceil(player_count), 1)
    return desired_instance

async def scaler(desired_instance, current_instances):
    if desired_instance > current_instances:
        await start_servers(desired_instance, current_instances)
    elif desired_instance < current_instances:
        await stop_servers(desired_instance, current_instances)

async def docker_instance_async(player_count, instance_capacity, game_title):
    # Connect to Docker using the aiodocker library
    docker = aiodocker.Docker()

    try:
        # Specify the new number of replicas you want
        new_num_replicas = math.ceil(player_count / instance_capacity)

        # Get the existing service
        service = await docker.services.get(game_title)

        # Update the service with the new number of replicas
        await service.scale(new_num_replicas)
        print(f'Service "{game_title}" updated to have {new_num_replicas} replicas.')
    finally:
        # Always close the Docker connection when you're done
        await docker.close()

async def get_replica_count_async(game_title):
    # Connect to Docker using the aiodocker library
    docker = aiodocker.Docker()

    try:
        # Get the existing service
        service = await docker.services.get(game_title)

        # Access the service attributes to get the number of replicas
        replicas = service['Spec']['Mode']['Replicated']['Replicas']
        return replicas
    finally:
        # Always close the Docker connection when you're done
        await docker.close()

