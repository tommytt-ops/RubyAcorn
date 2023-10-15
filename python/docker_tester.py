import docker

# Initialize the Docker client for the Swarm
client = docker.DockerClient(base_url='tcp://<Swarm-Manager-IP>:<Swarm-Manager-Port>')

# Specify the service name you want to update
service_name = 'my_service'

# Specify the new number of replicas you want
new_num_replicas = 3

# Get the existing service
service = client.services.get(service_name)

# Update the service with the new number of replicas
service.update(mode=docker.types.ServiceMode(replicated=docker.types.ReplicatedMode(
    replicas=new_num_replicas
)))

print(f'Service "{service_name}" updated to have {new_num_replicas} replicas.')
