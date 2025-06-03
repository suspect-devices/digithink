# Nick Cave -- My personal datacenter 
YOU ARE HERE DESCRIBING standing up a debian trixie server with appletalk, incus, and zfs
```
apt update
# DONT MODERNIZE THE FRACKING LIST TRIXIE TRASHES IT
apt install sudo nano wget curl
apt install avahi-daemon
apt install avahi-daemon avahi-utils
apt install libnss-mdns
apt install htop
apt install openssh-server
apt install ca-certificates
apt install curl
apt install gpg
apt install sudo
apt install parted
apt install htop
apt install bridge-utils
```
Install the zfs stuff.
```sh
nano /etc/apt/sources.list
apt update
apt install zfs-dkms
apt install zfsutils-linux
modprobe zfs
zfs list
apt -o Acquire::Check-Valid-Until=false update
apt policy linux-headers-*
apt install linux-headers-$(uname -r)
apt install --reinstall zfsutils-linux
zpool import
zpool import -f tank
zpool import -f local
zpool import -f reddisk
zpool clear tank ; zpool clear reddisk ; zpool status -v
```
replace the bad disk and replace the bad zfs partitions
```sh
sgdisk --replicate=/dev/sde /dev/sdb
sgdisk -G /dev/sde
ls -ls /dev/disk/by-id|grep sde
zpool status tank
zpool replace tank -o ashift=12 ata-ST12000NM000J-2TY103_ZRT0GC3A-part3 ata-WDC_WD120EFBX-68B0EN0_D7JVX9MN-part3
zpool replace reddisk -o ashift=12 9814339977262587103 ata-WDC_WD120EFBX-68B0EN0_D7JVX9MN-part4
```
...

```sh
wget https://github.com/Netatalk/netatalk/releases/download/netatalk-4-0-0/netatalk_4.0.0.ds-1_amd64.deb
dpkg --install ./netatalk_4.0.0.ds-1_amd64.deb
apt --fix-broken install
dpkg --install ./netatalk_4.0.0.ds-1_amd64.deb
apt install avahi-daemon
apt --fix-broken install
nano .ssh/authorized_keys
apt install avahi-daemon avahi-utils
apt install libnss-mdns
systemctl status avahi-daemon
nano /etc/netatalk/afp.conf
systemctl restart netatalk
systemctl status netatalk
```

```sh
zpool status
zpool upgrade local
zpool clear tank ; zpool clear reddisk ; zpool clear local ; zpool status -v
zfs mount -a
zfs list
zpool list
nano /etc/netatalk/afp.conf
ip a
cat .ssh/authorized_keys
df -k
zfs list
reboot
su - feurig
ip a
dhclient
nano /etc/default/networking
ifup
ip a
ifup enp12s0
ifup enp12s0
shutdown -h now
zpool status
zpool clear tank ; zpool clear reddisk ; zpool clear local ; zpool status -v
visudo
vigr
exit
visudo
cp .ssh/authorized_keys ~feurig/.ssh/authorized_keys
cd
cp .ssh/authorized_keys ~feurig/.ssh/authorized_keys
chown -R feurig:feurig ~feurig/.ssh
exit
ls -lsa
cd
ls -ls
ls -lsa
ls -lsa .ssh/
ls -ls ~feurig/.ssh/
nano /etc/ssh/sshd_config
ls
cat .ssh/authorized_keys
nano .ssh/authorized_keys
exit
zpool status
ls /dev/disk/
```
attempt to use tbolt 2 enclosure.

```sh
apt update
apt install thunderbolt-tools

apt install bolt
boltctl
boltctl list
boltctl enroll
boltctl enroll 00000000-0000-0018-80fa-1c134c238952
boltctl list
fdisk -l
boltctl info 00000000-0000-0018-80fa-1c134c238952
boltctl list
boltctl list --all
```

### FAIL

```sh
reboot
fdisk -l
nano .ssh/authorized_keys
apt install incus incus-tools qemu-system
curl  -fsSL https://pkgs.zabbly.com/key.asc -o /etc/apt/keyrings/zabbly.asc
sh -c 'cat <<EOF > /etc/apt/sources.list.d/zabbly-incus-stable.sources
Enabled: yes
Types: deb
URIs: https://pkgs.zabbly.com/incus/stable
Suites: $(. /etc/os-release && echo ${VERSION_CODENAME})
Components: main
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/zabbly.asc
EOF'
apt update
apt install incus
systemctl start incus
incus admin init
incus --version
```

At this point incus was foobarred and had set up a default lxdbr0 and was not the way we like things. So we....

Set up the bridge.

```sh
cat > /etc/network/interfaces<<EOD
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug enp11s0
iface enp11s0 inet dhcp
auto br0
iface br0 inet static
     address 192.168.129.189
     network 192.168.128.0
     netmask 255.255.128.0
     broadcast 192.168.255.255
     gateway 192.168.128.1
     mtu 9000
     bridge_ports enp12s0
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
EOD
systemctl restart networking
```

reinstall incus

```sh
apt purge incus
apt install incus
incus admin init
incus profile edit default
incus profile show default
incus init ubuntu/focal -c limits.cpu=4 -c limits.memory=8GiB -d root,size=20GiB --vm gru
incus init images:ubuntu/focal -c limits.cpu=4 -c limits.memory=8GiB -d root,size=20GiB --vm gru
incus profile show default
incus profile edit default
incus init images:ubuntu/focal -c limits.cpu=4 -c limits.memory=8GiB -d root,size=20GiB --vm gru
incus start gru
incus init images:ubuntu/focal -c limits.cpu=4 -c limits.memory=8GiB -d root,size=20GiB --vm minion1
incus start minion1
ip link set incusbr0 down
ip link delete incusbr0
nano /etc/resolv.conf
```

Mount apfs volumes.

```sh
apt install apfs-dkms --fix-missing
```
