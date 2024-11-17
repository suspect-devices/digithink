# Replace ubuntu with debian on home server.

Utah is my secondary home file server. It is a cheeze grater style mac with 3 2t ssds on a pci card that are the boot disks and then mirrored 8T and 14T zfs disks. Like the other 2 home servers it is an appletalk server as well as providing lxc containers and running docker processes. 

*I attempted to repeat the process used at the colo on utah but since there is no ipmi interface on the old mac pro it was not possible*.

## Initial setup.
I started with a fresh install on one of the 3 nvme disks and then referenced/copied some things around from the old os boot disk and the first attempt to install debian trixie. 

```
fdisk -l|grep Disk
mkdir /mnt/ubuntu
mkdir /mnt/wtfdebian
mount /dev/sde2 /mnt/ubuntu/
mount /dev/nvme0n1p2 /mnt/wtfdebian/
```

## convert from netplan back to /etc/network/interfaces

Somewhere along the last few ubuntu updates ubuntus netplan started becoming unusable. Sometimes the updates would overwrite the existing configuration without backing it up. When I tried to set up a fresh bridge configuration it refused. 

```
cat /mnt/ubuntu/etc/network/interfaces
cat /mnt/ubuntu/etc/netplan/
cat /mnt/ubuntu/etc/netplan/50-cloud-init.yaml
...
nano /etc/network/interfaces
...
source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug enp7s0f1
auto enp7s0f1
iface enp7s0f1 inet dhcp


auto br0
iface br0 inet static
     address 192.168.129.100
     network 192.168.128.0
     netmask 255.255.128.0
     broadcast 192.168.255.255
     gateway 192.168.128.1
     bridge_ports enp7s0f0
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
```
YOU ARE HERE!!! 
```
parted /dev/nvme0n1
apt install parted
nano /etc/apt/sources.list
apt updte
apt update
apt install parted
parted /dev/nvme0n1
cd /mnt/wtfdebian/
ls
cat etc/network/interfaces
df -k
fdisk -l|grep Disk
df -k
parted /dev/sde
apt install bridge-utils
nano /usr/local/bin/update.sh
nano /usr/local/bin/update.sh
chmod uog+x /usr/local/bin/update.sh
update.sh
apt install netatalk
update.sh
apt install netatalk
apt search netatalk
apt search appletalk
visudo
vigr
exit
visudo
exit
vigr
visudo
vigr
exit
exit
visudo
su - feurig
cd
cat ~feurig/.ssh/authorized_keys >>.ssh/authorized_keys
exit
visudo
visudo
su - feurig
exit
apt install sudo
update.sh
ip a
dhclient enp7s0f1
bg
ip a
nano /etc/network/interfaces
systemctl restart network
systemctl restart networking
journalctl -xeu networking.service
nano /etc/network/interfaces
ip a
systemctl restart networking
ip a
nano /etc/apt/sources.list
ip a
ip a
systemctl status sshd
ip a
ping digithink.com
reboot
apt update
apt-cache search netatalk
apt-cache search appletalk
lsmod | grep appletalk
apt search afpd
nano /etc/apt/sources.list
exit
wget https://github.com/Netatalk/netatalk/releases/download/netatalk-4-0-0/netatalk_4.0.0.ds-1_amd64.
ls
dpkg --install netatalk_4.0.0.ds-1_amd64.deb
dpkg --install netatalk_4.0.0.ds-1_amd64.deb
dpkg --help
dpkg -I ./netatalk_4.0.0.ds-1_amd64.deb
apt-get init-system-helpers libpam-modules netbase libacl1 libavahi-client3 perl libavahi-common3 libc6 libcrack2
apt-get install init-system-helpers libpam-modules netbase libacl1 libavahi-client3 perl libavahi-common3 libc6 libcrack2
apt --fix-broken install
dpkg install ./netatalk_4.0.0.ds-1_amd64.deb
dpkg --install ./netatalk_4.0.0.ds-1_amd64.deb
systemctl enable netatalk
ls
apt-cache search zfs
apt get zfsutils-linux
apt install zfsutils-linux
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
zpool import
zpool import -f tank
zpool import -f reddisk
nano /etc/netatalk/afp.conf
systemctl restart netatalk
zpool import
nano /etc/netatalk/afp.conf
systemctl restart netatalk
apt install avahi-daemon
apt enable appletalk
systemctl enable appletalk
systemctl enable netatalk
systemctl start netatalk
systemctl status netatalk
ls
cd ~feurig
ls
cd /filebox
ls
zpool status
ls /tank
zpool list
history|cut -c8-100
systemctl enable avhi-daemon
systemctl enable avahi-daemon
systemctl start avahi-daemon
systemctl status avahi-daemon
history|cut -c8-200
hostname

apt update
apt -t bookworm-backports install incus incus-tools qemu-system
```