# Replace Ubuntu with Debian on home server.

Utah (Phillips) is my secondary home file server. It is a cheeze grater style mac with 3 2t ssds on a pci card that are the boot disks and then mirrored 8T and 14T zfs disks. Like the other 2 home servers it is an appletalk server as well as providing lxc containers and running docker processes. 

*I attempted to repeat the process used at the colo on utah but since there is no ipmi interface on the old mac pro it was not possible*.

## Initial setup.
I started with a fresh install on one of the 3 nvme disks and then referenced/copied some things around from the old os boot disk and the first attempt to install debian trixie. I won't bother you with the details. I will however reuse /dev/nvme0n1.

```
fdisk -l|grep Disk
mkdir /mnt/ubuntu
mkdir /mnt/wtfdebian
mount /dev/sde2 /mnt/ubuntu/
mount /dev/nvme0n1p2 /mnt/wtfdebian/
```

## Convert from netplan back to /etc/network/interfaces

Somewhere along the last few ubuntu updates ubuntus netplan started becoming unusable. Sometimes the updates would overwrite the existing configuration without backing it up. When I tried to set up a fresh bridge configuration it refused. So stick a fork in it and turn it over we are done.

```
apt install bridge-utils
cat /mnt/ubuntu/etc/network/interfaces
cat /mnt/ubuntu/etc/netplan/
cat /mnt/ubuntu/etc/netplan/50-cloud-init.yaml
...
nano /etc/network/interfaces
...
#source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

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
^X
systemctl restart networking
```

## Install zfs and appletalk 

### Add repositories from testing(trixie) 

The zfs supported by bookworm will not import the filesystems created by ubuntu24.04 but the zfs packages backported from trixie will.

```
nano /etc/apt/sources.list
deb-src http://security.debian.org/debian-security bookworm-security main non-free-firmware
deb-src http://debian.osuosl.org/debian/ bookworm-updates main non-free-firmware
deb-src http://debian.osuosl.org/debian/ bookworm main non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main non-free-firmware
deb http://debian.osuosl.org/debian/ bookworm-updates main non-free-firmware
deb http://debian.osuosl.org/debian/ bookworm main non-free-firmware
deb http://deb.debian.org/debian-security/ bookworm-security main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-updates main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
^X
```
### Install Netatalk 4 debian provided by netatalk

There was no debian maintainer for a year or so which meant that debian dropped appletalk support on bookworm. This has been resolved and should be supported when trixie is released. In the mean time the fine folk at netatalk have provided a packaged version for both netatalk3 and netatalk4 for bookworm.

```
wget https://github.com/Netatalk/netatalk/releases/download/netatalk-4-0-0/netatalk_4.0.0.ds-1_amd64.deb
dpkg --install ./netatalk_4.0.0.ds-1_amd64.deb
apt --fix-broken install
dpkg --install ./netatalk_4.0.0.ds-1_amd64.deb
apt install avahi-daemon
systemctl enable avahi-daemon
systemctl start avahi-daemon
systemctl status avahi-daemon
systemctl enable netatalk
systemctl start netatalk
systemctl status netatalk
```
### Install zfs from bookworm-backports and import existing pools.

```
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
zpool import
zpool import -f tank
zpool import -f reddisk
nano /etc/netatalk/afp.conf
```

## Install and initialize incus

### Make some space 

Unlike lxd incus does most of its work under /var/lib/incus as apposed to in the storage pools. You need to make some room there. 

```
cat /etc/fstab
# / was on /dev/sdf2 during installation
UUID=1403cbd4-a187-4cd2-8d83-c7c036b3e589 /               ext4    errors=remount-ro 0       1
# /boot/efi was on /dev/sdf1 during installation
UUID=0E04-F115  /boot/efi       vfat    umask=0077      0       1
# /home was on /dev/sdf4 during installation
UUID=22bbd39c-e3b8-402a-bcc2-cd05a889cecb /var/lib/incus           ext4    defaults        0       2
# swap was on /dev/sdf3 during installation
UUID=4f2aa57f-219d-4355-815c-3a89a613a8cb none            swap    sw              0       0
```

### Install from bookworm-backports (trixie)

```
apt update
apt -t bookworm-backports install incus incus-tools qemu-system

root@utah:~# ls -ls /dev/disk/by-id|grep nvme0
0 lrwxrwxrwx 1 root root 13 Nov 17 16:31 nvme-eui.0000000001000000e4d25c757b395601 -> ../../nvme0n1
0 lrwxrwxrwx 1 root root 13 Nov 17 16:31 nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C -> ../../nvme0n1
0 lrwxrwxrwx 1 root root 13 Nov 17 16:31 nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C_1 -> ../../nvme0n1
root@utah:~# ls -ls /dev/disk/by-id/nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C
0 lrwxrwxrwx 1 root root 13 Nov 17 16:31 /dev/disk/by-id/nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C -> ../../nvme0n1
root@utah:~# incus admin init
Would you like to use clustering? (yes/no) [default=no]:
Do you want to configure a new storage pool? (yes/no) [default=yes]:
Name of the new storage pool [default=default]: local
Name of the storage backend to use (dir, zfs) [default=zfs]:
Create a new ZFS pool? (yes/no) [default=yes]:
Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]: yes
Path to the existing block device: /dev/disk/by-id/nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C
Would you like to create a new local network bridge? (yes/no) [default=yes]: no
Would you like to use an existing bridge or host interface? (yes/no) [default=no]: yes
Name of the existing bridge or host interface: br0
Would you like the server to be available over the network? (yes/no) [default=no]: yes
Address to bind to (not including port) [default=all]:
Port to bind to [default=8443]:
Would you like stale cached images to be updated automatically? (yes/no) [default=yes]:
Would you like a YAML "init" preseed to be printed? (yes/no) [default=no]: yes
config:
  core.https_address: '[::]:8443'
networks: []
storage_pools:
- config:
    source: /dev/disk/by-id/nvme-INTEL_SSDPEKNU020TZ_PHKA314002UT2P0C
  description: ""
  name: local
  driver: zfs
profiles:
- config: {}
  description: ""
  devices:
    eth0:
      name: eth0
      nictype: bridged
      parent: br0
      type: nic
    root:
      path: /
      pool: local
      type: disk
  name: default
projects: []
cluster: null

```