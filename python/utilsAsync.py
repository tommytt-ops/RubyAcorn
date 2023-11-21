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

async def get_replica_count_async(game_title):
        
    docker = aiodocker.Docker()
    services = await docker.services.list(filters={"name": game_title})
    if services:
        # Assuming that the service name is unique and we can take the first match.
        service = services[0]
        replicas = service['Spec']['Mode']['Replicated']['Replicas']
        return replicas
      
    await docker.close()

async def docker_instance_async(player_count, instance_capacity, game_title):
    
    docker = aiodocker.Docker()

    # Specify the new number of replicas you want
    new_num_replicas = math.ceil(player_count / instance_capacity)

     # List services and find the one we want to update
    services = await docker.services.list(filters={"name": game_title})
    if not services:
        print(f"No service found with the name {game_title}")
        return

    print()
    service = services[0]
    service_id = service['ID']
    version = service['Version']['Index']

    print(f"Service ID: {service_id}")
    print(f"Version: {version}")
    print(f"Service Spec: {service_spec}")


    # Update the service with the new number of replicas
    # The service spec needs to be obtained and modified, then passed back to the update method.
    service_spec = service['Spec']
    service_spec['Mode']['Replicated']['Replicas'] = new_num_replicas

    await docker.services.update(service_id, version, service_spec)
    print(f'Service "{game_title}" updated to have {new_num_replicas} replicas.')
    await docker.close()

