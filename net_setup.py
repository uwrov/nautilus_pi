# Script which reads net_config as the desired network configuration
# and adjusts files in the OS to match that config

# requries a command line specifiing which device on the network this machine is
# example:
#
#           sudo python3 net_setup.py main
#
# This will change this machine's hostname to 'main', and request
# a static ip as defined in net_config

import sys

if len(sys.argv) != 3:
    print("Usage: sudo python3 net_setup.py [hostname]")
    sys.exit()

hn = sys.argv[2]

with open('net_config') as config_file:

    hosts = ()
    for line in config_file:
        _, hostname = line.split()
        hosts.add(hostname)
    if hn not in hosts:
        print("Given hostname not found in net_config file")
        sys.exit()

    # edit /etc/hosts
    config_file.seek(0)
    with open('/etc/hosts', 'w') as host_file:
        host_file.seek(11)
        for line in config_file:
            host_file.write(line)

    # edit /etc/hostname
    config_file.seek(0)
    with open('/etc/hostname', 'w') as hostname_file:
        hostname_file.write(hn)

    # change files to request a static ip