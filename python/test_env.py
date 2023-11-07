from prometheus_client import start_http_server, generate_latest, REGISTRY, Gauge
import datetime
import time
import xgboost
from docker_tester import docker_instance, get_replica_count
from Utils import prometheus_player_count_fetch, max_player_per_hour, desired_instances, scaler
from linux_scripts.linux_scripts import server_list
from prom_metrics_ import prom_metrics
import asyncio
import aiohttp
from linux_scripts.linux_scripts import start_servers, stop_servers

import re

async def prometheus_player_count_fetch_async(game_title):
    url = 'http://10.196.36.11/metrics'  # Replace with the URL you want to post to
    params = {'key': 'value'}  # Replace with your data as needed

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                content = await response.text()
                lines = content.split('\n')
                for line in lines:
                    match = re.search(r'title="([^"]*)".* (\d+)$', line)
                    if match:
                        line_game_title, player_count = match.groups()
                        if line_game_title == game_title:
                            return player_count
            else:
                print(f'Error: {response.status}')



async def fetch_player_counts(game_names):
    player_count_dict = {}

    async with aiohttp.ClientSession() as session:
        tasks = [prometheus_player_count_fetch_async(game_name) for game_name in game_names]
        results = await asyncio.gather(*tasks)

    for game_name, result in zip(game_names, results):
        if result is not None:
            player_count_dict[game_name] = int(result)

    
    return player_count_dict

game_names = [
    "Counter-Strike",
    "Counter-Strike: Source",
    "Counter-Strike: Condition Zero Deleted Scenes",
    "Counter-Strike: Source",
    "Source Filmmaker",
    "Team_Fortress_Classic",
    "Half-Life 2",
    "Half-Life: Source",
    "Day_of_Defeat",
    "Day of Defeat: Source",
    "Half-Life 2: Deathmatch",
    "Half-Life 2: Episode One",
    "Portal",
    "Half-Life 2: Episode Two",
    "Team Fortress 2",
    "The Lab",
    "Left 4 Dead",
    "Left 4 Dead 2",
    "Portal 2",
    "Alien Swarm",
    "Half-Life",
    "Counter-Strike: Global Offensive",
    "Counter-Strike: Condition Zero",
    "Dota 2"
]

start_http_server(8001)


while True:
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    formatted_time = current_time.strftime('%H:%M:%S')

    current_date = datetime.datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year    

    time_parts = formatted_time.split(":")
    hour = int(time_parts[0])
    min = int(time_parts[1])
    sec = int(time_parts[2])

    if min == 0:
        



