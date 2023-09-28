import datetime
 
current_datetime = datetime.datetime.now()
current_time = current_datetime.time()
formatted_time = current_time.strftime('%H:%M:%S')

time_parts = formatted_time.split(":")
hour = int(time_parts[0])
minute = int(time_parts[1])
sek = int(time_parts[2])

print(current_datetime)
print(f"{hour} {minute} {sek}")