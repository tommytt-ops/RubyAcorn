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

async def prometheus_player_count_fetch_async(game_title):
    url = "http://10.196.36.11/metrics"  # Replace with the URL you want to post to
    params = {"key": "value"}  # Replace with your data as needed

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                content = await response.text()
                lines = content.split("\n")
                for line in lines:
                    match = re.search(r'title="([^"]*)".* (\d+)$', line)
                    if match:
                        line_game_title, player_count = match.groups()
                        if line_game_title == game_title:
                            return player_count
            else:
                print(f"Error: {response.status}")



async def fetch_player_counts(game_names):
    player_count_dict = {}

    async with aiohttp.ClientSession() as session:
        tasks = [prometheus_player_count_fetch_async(game_name) for game_name in game_names]
        results = await asyncio.gather(*tasks)

    for game_name, result in zip(game_names, results):
        if result is not None:
            player_count_dict[game_name] = int(result)

    
    return player_count_dict

async def process_game_async(game_name, service_name, current_player_count, docker_instance_capacity, player_count_valve):
    
    if (
         math.ceil(current_player_count / docker_instance_capacity) !=
        await get_replica_count_async(service_name) and current_player_count != 0
    ):
        print(f"{game_name}: {current_player_count}")
        await docker_instance_async(current_player_count, docker_instance_capacity, service_name)

    replica_count = await get_replica_count_async(service_name)
    await prom_metrics(replica_count, player_count_valve, game_name)

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

start_http_server(8002)

async def main():

    predict_max_player = 0
    instance_capacity = 250000
    docker_instance_capacity = 1000
    loaded_model = xgboost.Booster()
    loaded_model.load_model("./python/reg_model_valve.json")
    data_arr = []

    player_count_valve = Gauge("player_count_valve", "player counts to diffrent valve games", ["title"])
    server_instance_valve = Gauge("server_instance_valve", "combined amount of servers running for valve games", ["title"])

    while True:
        current_datetime = datetime.datetime.now()
        current_time = current_datetime.time()
        formatted_time = current_time.strftime("%H:%M:%S")

        current_date = datetime.datetime.now()
        day = current_date.day
        month = current_date.month
        year = current_date.year    

        time_parts = formatted_time.split(":")
        hour = int(time_parts[0])
        min = int(time_parts[1])
        sec = int(time_parts[2])

        game_names = game_service_dict.keys()
        current_players = await fetch_player_counts(game_names)
        current_players_all = sum(current_players.values())

        if min == 0:

            predict_max_player = max_player_per_hour(year, month, day, hour, loaded_model, data_arr)
            print(hour)
            print("predicted: ", predict_max_player)
            print("current players: ",current_players_all)
            print("")

            if predict_max_player != 0:
                desired_instances_to_run = desired_instances(instance_capacity, predict_max_player)
                current_instances_running = len(server_list("ACTIVE")) -1
                print(current_players_all)
                scaler(desired_instances_to_run, current_instances_running)
                print("given servers: ",  desired_instances(instance_capacity, predict_max_player))
                await prom_metrics(len(server_list("ACTIVE")) -1, server_instance_valve, "Server instances")
                print("")

        if current_players_all != 0 and min % 5 == 0 and predict_max_player != 0:

            if (len(server_list("ACTIVE"))-1) * instance_capacity < current_players_all and predict_max_player != 0:

                print("need more servers")
                print(f"{hour}:{min}")
                print(predict_max_player)
                print(current_players_all)
                print("")
                desired_instances_to_run = desired_instances(instance_capacity, current_players_all)
                current_instances_running = len(server_list("ACTIVE")) -1
                scaler(desired_instances_to_run, current_instances_running)
                await prom_metrics(len(server_list("ACTIVE")) -1, server_instance_valve, "Server instances")

            await asyncio.gather(*[
                loop.create_task(process_game_async(game_name, service_name, current_players.get(game_name, 0), docker_instance_capacity, player_count_valve))
                for game_name, service_name in game_service_dict.items()
            ])

            time.sleep(60)


    



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())






        



