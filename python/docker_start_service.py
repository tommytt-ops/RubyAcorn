import docker

client = docker.from_env()

# Define the container configurations
container_config = {
    'image': 'nginx',  # Replace with the desired Docker image
}

# Define service options
service_options = {
    'name': 'PLAYERUNKNOWNS_BATTLEGROUNDS',  # Specify the service name
    'mode': docker.types.ServiceMode('replicated', replicas=3),  # Set the service mode and number of replicas
    'constraints': ['node.role != manager'],
}

service = client.services.create(**container_config, **service_options)
print(f'Service "{service.name}" created with ID {service.id}')
