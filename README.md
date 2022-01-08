# nautilus_pi
Repo for UWROV's ROV's onboard code

## Dependencies
Assumes you have a quad-core Raspberry Pi (or other ARM system), a Pi 4 or a Pi Zero 2 should both work fine

- Docker
- Docker Compose

## Usage
### Network Setup
First edit the `net_config` file to mirror the network configuration you desire, then run `sudo python3 net_setup.py [hostname]` to set up the network, this will edit the hostname files on your device and attempt to make them mirror the `net_config` file.

Note that the `net_setup.py` script currently doesn't support running multiple times - if things need to be changed, either update the script or edit the following files:

- `/etc/hosts`
- `/etc/hostname`
- `/etc/dhcpcd.conf` (if on raspbian) or `/etc/netplan/01-netcfg.yaml` (if on ubuntu)
- `.env`

### Using the Container
The container will build itself on the first run of `sudo docker-compose up`, future builds must be triggered manually with `sudo docker-compose build`.

Launch the container with `sudo docker-compose up`, then use the alias `con` to connect to the container's terminal (`con` is a shortcut for `sudo docker exec -it pi_container /bin/bash`).

Once the container is up and running, we have a nice little with ROS and OpenCV, which has been preconfigured to work with our surface node.

When finished, detach from the container and run `sudo docker-compose down` to clean up.

