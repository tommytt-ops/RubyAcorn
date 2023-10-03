import math

current_player_count = 3001000
instance_capacity = 500000
predicted_max_hour_player_count = 2522578

player_count = predicted_max_hour_player_count / instance_capacity
desired_isinstance = math.ceil(player_count)

print(desired_isinstance)

next_instance_needed = desired_isinstance * instance_capacity

