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

if len(sys.argv) != 3:
    print("Usage: sudo python3 net_setup.py [hostname]")
    sys.exit()

hn = sys.argv[2]
target_ip = None

with open('net_config') as config_file:

    for line in config_file:
        ip, hostname = line.split()
        if hostname == hn:
            target_ip = ip

    if target_ip is None:
        print("Given hostname not found in net_config file")
        sys.exit()

    # edit /etc/hosts
    config_file.seek(0)
    with open('/etc/hosts', 'w') as host_file:
        host_file.seek(11)
        for line in config_file:
            host_file.write(line)

# edit /etc/hostname
with open('/etc/hostname', 'w') as hostname_file:
    hostname_file.write(hn)

# change files to request a static ip
with open('/etc/netplan/01-netcfg.yaml', 'w+') as netplan_file:
    with open('netplan', 'r') as target:
        for line in target:
            if line == 'CHANGE_ME_IP':
                line = hn + '/24'
            netplan_file.write(line)

os.system("sudo netplan apply")

print("Network Configuration Complete, run ifconfig and make sure desired ip is correct")