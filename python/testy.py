from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import datetime
import time
import xgboost
import math
from docker_tester import docker_instance, get_replica_count
from Utils import prometheus_player_count_fetch, max_player_per_hour, desired_instances, scaler
from linux_scripts.linux_scripts import server_list
from prom_metrics_ import prom_metrics
import asyncio
import aiohttp
from linux_scripts.linux_scripts import start_servers, stop_servers
from utilsAsync import get_replica_count_async, docker_instance_async, desired_instances_async

import re


# Function to fetch player count for a specific game
async def prometheus_player_count_fetch_async(game_title):
    url = 'http://10.196.36.11/metrics'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                lines = content.split('\n')
                for line in lines:
                    # Check if the line contains the game title
                    if f'title="{game_title}"' in line:
                        # Extract the last number from the line
                        match = re.search(r'(\d+)$', line)
                        if match:
                            number = match.group(1)  # Get the matched number
                            return int(number)  # Convert to int for consistency
                return 0  # Return 0 if not found
            else:
                print(f'Error fetching {game_title}: HTTP {response.status}')
                return 0  # Return 0 in case of HTTP errors



async def fetch_player_counts(game_names):
    player_count_dict = {}

    async with aiohttp.ClientSession() as session:
        tasks = [prometheus_player_count_fetch_async(game_name) for game_name in game_names]
        results = await asyncio.gather(*tasks)

    for game_name, result in zip(game_names, results):
        if result is not None:
            player_count_dict[game_name] = int(result)

    
    return player_count_dict

async def main():
        
        game_service_dict = {
    "Counter-Strike": "counter_strike", 
    "Counter-Strike: Source": "counter_strike_source", 
    "Counter-Strike: Condition Zero Deleted Scenes": "counter_strike_condition_zero_deleted_scenes",
    "Source Filmmaker": "source_filmmaker" , 
    "Team Fortress Classic": "team_fortress_classic", 
    "Half-Life 2": "half_life_2", 
    "Half-Life: Source": "half_life_source", 
    "Day of Defeat": "day_of_defeat",
    "Day of Defeat: Source": "day_of_defeat_source", 
    "Half-Life 2: Deathmatch": "half_life_2_deathmatch", 
    "Half-Life 2: Episode One": "half_life_2_episode_one", 
    "Portal": "portal",
    "Half-Life 2: Episode Two": "half_life_2_episode_two", 
    "Team Fortress 2": "team_fortress_2", 
    "The Lab": "the_lab", 
    "Left 4 Dead": "left_4_dead", 
    "Left 4 Dead 2": "left_4_dead_2",
    "Portal 2": "portal_2", 
    "Alien Swarm": "alien_swarm", 
    "Half-Life": "half_life", 
    "Counter-Strike: Global Offensive": "counter_strike_global_offensive", 
    "Counter-Strike: Condition Zero": "counter_strike_condition_zero",
    "Dota 2": "dota_2"
}

        game_names = game_service_dict.keys()
        current_players = await fetch_player_counts(game_names)
        print(sum(current_players.values()))
            


if __name__ == "__main__":
    asyncio.run(main())