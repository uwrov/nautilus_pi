before=$1;
after=$2;

echo "changing hostname from ${before} to ${after}"
sudo sed -i "s/${before}/${after}/g" /etc/hosts /etc/hostname