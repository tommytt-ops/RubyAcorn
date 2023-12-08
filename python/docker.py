import docker
import math

def docker_instance(player_count, instance_capacity, title):
    client = docker.from_env()

   
    new_num_replicas = math.ceil(player_count/instance_capacity)

    
    service = client.services.get(title)

    
    service.scale(new_num_replicas)
    print(f'Service "{title}" updated to have {new_num_replicas} replicas.')

def get_replica_count(title):
    client = docker.from_env()
    service = client.services.get(title)
    replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
    return replicas
