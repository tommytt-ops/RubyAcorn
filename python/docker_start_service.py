import docker

client = docker.from_env()

# Define the container configuration
container_config = {
    'image': 'nginx',  # Replace with the desired Docker image
}

# Define service options
service_options = {
    'name': 'my_service',  # Specify the service name
    'mode': docker.types.ServiceMode('replicated', replicas=3),  # Set the service mode and number of replicas
}

service = client.services.create(**container_config, **service_options)
print(f'Service "{service.name}" created with ID {service.id}')
