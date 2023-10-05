def stop_servers(amount, amount_unpaused):

    amount_to_pause = amount_unpaused - amount
    server_to_pause ="openstack server pause "



    for i  in range(amount_to_pause+1, amount_unpaused+1):

        print(i)

        string ="Server"
        

        server_name = string + str(i)+" "

        server_to_pause += server_name

    return server_to_pause

print(stop_servers(2, 4))