import docker

client = docker.from_env()

# Define the container configurations
container_config = {
    'image': 'nginx',  # Replace with the desired Docker image
}

# Define service options

def service_options(name):
    service_options = {
        'name': name,  # Specify the service name
        'mode': docker.types.ServiceMode('replicated', replicas=3),  # Set the service mode and number of replicas
        'constraints': ['node.role != manager'],
    }

    return service_options


game_names = [
    "counter_strike",
    "counter_strike_source",
    "counter_strike_condition_zero_deleted_scenes",
    "source_filmmaker",
    "team_fortress_classic",
    "half_life_2",
    "half_life_source",
    "day_of_defeat",
    "day_of_defeat_source",
    "half_life_2_deathmatch",
    "half_life_2_episode_one",
    "portal",
    "half_life_2_episode_two",
    "team_fortress_2",
    "the_lab",
    "left_4_dead",
    "left_4_dead_2",
    "portal_2",
    "alien_swarm",
    "half_life",
    "counter_strike_global_offensive",
    "counter_strike_condition_zero",
    "dota_2"
]

for names in game_names:
    service = client.services.create(**container_config, **service_options(names))
    print(f'Service "{service.name}" created with ID {service.id}')
