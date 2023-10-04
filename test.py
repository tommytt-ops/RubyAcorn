def start_servers(amount, amount_unpaused):

    first_server = amount_unpaused +1
    server_to_start ="openstack server unpause "

    for i  in range(first_server, amount+1):

        string ="Server"
        num = i
        server_name = string + str(num)+" "
        server_to_start += server_name

    print(server_to_start)

start_servers(4, 1)