import subprocess
import json

def server_list(status):

    server_info_list = []

    command = "openstack server list --format json"

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    if result.returncode == 0:
        try:
            server_data = json.loads(result.stdout)
            for server_json in server_data:
                server_id = server_json['ID']
                server_name = server_json['Name']
                server_status = server_json['Status']

                if server_status == status:   
                    server_info_list.append({"ID": server_id, "Name": server_name, "Status": server_status})
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
      
        print(f"Command failed with error: {result.stderr}")

    return server_info_list

def all_server_list():
  
    server_info_list = []

    command = "openstack server list --format json"

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    if result.returncode == 0:
        try:
            
            server_data = json.loads(result.stdout)
            for server_json in server_data:
                server_id = server_json['ID']
                server_name = server_json['Name']
                server_status = server_json['Status']
  
                server_info_list.append({"ID": server_id, "Name": server_name, "Status": server_status})
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:

        print(f"Command failed with error: {result.stderr}")

    return server_info_list

def start_servers(amount, amount_unpaused):

    first_server = amount_unpaused +1
    server_to_start ="openstack server unpause "

    for i in range(first_server, amount+1):

        string ="Server"
        num = i
        server_name = string + str(num)+" "
        server_to_start += server_name

    try:
        subprocess.run(server_to_start, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    
    return server_to_start

def stop_servers(amount, amount_unpaused):

    amount_to_pause = amount_unpaused - amount
    server_to_pause ="openstack server pause "

    for i  in range(amount_to_pause+1, amount_unpaused+1):

        string ="Server"
        server_name = string + str(i)+" "
        server_to_pause += server_name


    try:
        subprocess.run(server_to_pause, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    
    return server_to_pause









