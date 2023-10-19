import subprocess

command = "openstack server list"
subprocess.run(command, shell=True)