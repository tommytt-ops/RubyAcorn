import docker
import math

def docker_instance(player_count, instance_capacity):
    client = docker.from_env()

    # Specify the service name you want to update
    service_name = 'my_service'

    # Specify the new number of replicas you want
    new_num_replicas = math.ceil(player_count/instance_capacity)

    # Get the existing service
    service = client.services.get(service_name)

    # Update the service with the new number of replicas
    service.scale(new_num_replicas)
    print(f'Service "{service_name}" updated to have {new_num_replicas} replicas.')

def get_replica_count():
    client = docker.from_env()
    service = client.services.get("my_service")
    replicas = service.attrs['Spec']['Mode']['Replicated']['Replicas']
    return replicas
