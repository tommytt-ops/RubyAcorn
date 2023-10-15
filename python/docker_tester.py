import docker

# Initialize the Docker client for the Swarm
client = docker.from_env()

# Define the container configuration
container_config = {
    'image': 'busybox',
    'command': 'sleep 3600',  # Command to keep the container running
}

# Number of containers you want to run
num_containers = 50

# Create the specified number of containers in the Swarm
for i in range(num_containers):
    service = client.services.create(**container_config)
    print(f'Container service started with ID {service.id}')
