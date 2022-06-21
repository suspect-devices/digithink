# Costello, an Ubuntu 22.04 lxd 5 home server.


```shell
# snap install lxd
# apt install htop  openssh-server install netatalk  zfsutils-linux
# apt remove --purge network-manager network-manager-gnome network-manager-pptp network-manager-pptp-gnome
```

```shell
# ip a >> /etc/netplan/01-network-manager-all.yaml
# nano /etc/netplan/01-network-manager-all.yaml
#------------------------------------- /etc/netplan/01-network-manager-all.yaml
#
# Dont Let NetworkManager manage *ANY* devices on this system
#
# enp3s0f0  68:fe:f7:09:3c:4c

...
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
        match:
          macaddress:  68:fe:f7:09:3c:4c
        mtu: 7000
        dhcp4: no
        dhcp6: no
        set-name: eth0
    wlp2s0:
        dhcp4: no
        dhcp6: no
  bridges:
    br0:
        dhcp4: no
        dhcp6: no
        mtu: 7000
        addresses:
            - 192.168.129.45/17
        gateway4: 192.168.129.1
        nameservers:
            addresses:
                - 192.168.129.1
                - 198.202.31.132
        interfaces:
            - eth0
# netplan apply
# reboot
```

```shell
fdisk -l
# fdisk -l
...
Disk /dev/nvme0n1: 1.82 TiB, 2000398934016 bytes, 3907029168 sectors
Disk model: CT2000P2SSD8
...
Device           Start        End    Sectors  Size Type
/dev/nvme0n1p1    2048    1050623    1048576  512M EFI System
/dev/nvme0n1p2 1050624 3907028991 3905978368  1.8T Linux filesystem
...
Disk /dev/sda: 12.73 TiB, 14000519643136 bytes, 27344764928 sectors
Disk model: M001G-2KJ103
...
Device           Start         End    Sectors  Size Type
/dev/sda1         2048  6442452991 6442450944    3T Linux filesystem
/dev/sda2   6442452992 12884903935 6442450944    3T Linux filesystem
/dev/sda3  12884903936 21474838527 8589934592    4T Linux filesystem
/dev/sda4  21474838528 27344764894 5869926367  2.7T Linux filesystem
...
Disk /dev/sdb: 1.86 TiB, 2048408248320 bytes, 4000797360 sectors
Disk model: JAJS600M2TB
...
Device      Start        End    Sectors  Size Type
/dev/sdb1      40     409639     409600  200M EFI System
/dev/sdb2  409640 4000797319 4000387680  1.9T Apple APFS
# ls -lsa /dev/disk/by-id/|grep sda
# zpool create tank wwn-0x5000c500dc29d6c5-part4
```

```shell
lxd init
# lxd init
Would you like to use LXD clustering? (yes/no) [default=no]: yes
What IP address or DNS name should be used to reach this node? [default=192.168.129.45]:
Are you joining an existing cluster? (yes/no) [default=no]:
What name should be used to identify this node in the cluster? [default=costello]:
Setup password authentication on the cluster? (yes/no) [default=no]: yes
Trust password for new clients:
Again:
Do you want to configure a new local storage pool? (yes/no) [default=yes]:
Name of the storage backend to use (btrfs, dir, lvm, zfs) [default=zfs]:
Create a new ZFS pool? (yes/no) [default=yes]:
Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]: yes
Path to the existing block device: /dev/disk/by-id/wwn-0x5000c500dc29d6c5-part1
Do you want to configure a new remote storage pool? (yes/no) [default=no]:
Would you like to connect to a MAAS server? (yes/no) [default=no]:
Would you like to configure LXD to use an existing bridge or host interface? (yes/no) [default=no]: yes
Name of the existing bridge or host interface: br0
Would you like stale cached images to be updated automatically? (yes/no) [default=yes]:
Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]: yes
config:
  core.https_address: 192.168.129.45:8443
  core.trust_password: ON.TACOCAT.NO
networks: []
storage_pools:
- config:
    source: /dev/disk/by-id/wwn-0x5000c500dc29d6c5-part1
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
cluster:
  server_name: costello
  enabled: true
  member_config: []
  cluster_address: ""
  cluster_certificate: ""
  server_address: ""
  cluster_password: ""
  cluster_certificate_path: ""
  cluster_token: ""

```

```shell
# nano /etc/netatalk/afp.conf
;--------------------------------------------- /etc/netatalk/afp.conf
; Netatalk 3.x configuration file
;

[Global]
; Global server settings

; pretty sure this one stays.
map acls = mode
; Not sure about the next two
aclinherit = passthrough
aclmode = passthrough

[tank]
path = /tank
ea=none
# service netatalk restart
```

```shell
# chown feurig /tank/
# su - feurig
```