# Script which reads net_config as the desired network configuration
# and adjusts files in the OS to match that config

# requries a command line specifiing which device on the network this machine is
# example:
#
#           sudo python3 net_setup.py main
#
# This will change this machine's hostname to 'main', and request
# a static ip as defined in net_config
import os
import sys

if len(sys.argv) != 2:
    print("Usage: sudo python3 net_setup.py [hostname]")
    sys.exit()

hn = sys.argv[1]
target_ip = None

with open('config/net_config') as config_file:

    for line in config_file:
        ip, hostname = line.split()
        if hostname == hn:
            target_ip = ip

    if target_ip is None:
        print("Given hostname not found in net_config file")
        sys.exit()

    # edit /etc/hosts
    config_file.seek(0)
    with open('/etc/hosts', 'a') as host_file:
        for line in config_file:
            host_file.write(line)

# edit /etc/hostname
with open('/etc/hostname', 'w') as hostname_file:
    hostname_file.write(hn)

# change files to request a static ip
try:
    with open('/etc/netplan/01-netcfg.yaml', 'w+') as netplan_file:
        with open('config/netplan', 'r') as target:
            for line in target:
                if line[-2] == '-':
                    line = line + target_ip + '/24'
                netplan_file.write(line)
    os.system("sudo netplan apply")
except:
    with open('/etc/dhcpcd.conf', 'a') as file:
        with open('config/dhcpcd', 'r') as target:
            for line in target:
                if len(line) >= 2 and line[-2] == '=':
                    line = line[:-1] + target_ip + '/24\n'
                file.write(line)

# change the docker-compose environment variables file
with open('./.env', 'w') as env_file:
    env_file.write(f'HOSTNAME={hn}')
    env_file.write(f'IP={target_ip}')
    env_file.write(f'URI=http://192.168.0.69:11311') # NOTE: Hardcoded

    env_file.truncate()

print("Network Configuration Complete, run ifconfig and make sure desired ip is correct")
