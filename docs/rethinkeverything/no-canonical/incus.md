# incus install on kh2024

Currently just the bones.
You are here fleshing them in.


This is on a system that has been installed as described in the debian link.

This requires that you modify the /etc/apt/sources.list to include the backports.

```sh
root@kh2024:~# cat /etc/apt/sources.list
#deb http://ftp.us.debian.org/debian bookworm main
deb http://deb.debian.org/debian bookworm main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-updates main non-free non-free-firmware contrib
deb http://deb.debian.org/debian-security/ bookworm-security main non-free non-free-firmware contrib
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
```

Set up the network

```sh
apt -t bookworm-backports install incus incus-tools
apt install bridge-utils
nano /etc/network/interfaces
.... 
# https://ip4calculator.com
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

iface eno2 inet manual
iface eno3 inet manual
iface eno4 inet manual

auto br0
iface br0 inet static
     address 198.202.31.158
     network 198.202.31.128
     netmask 255.255.255.128
     broadcast 198.202.31.255
     gateway 198.202.31.129
     bridge_ports eno4
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay

auto eno1
iface eno1 inet static
     address 192.168.31.158
     network 192.168.31.0
     netmask 255.255.255.0
     broadcast 192.168.31.255
     #gateway 192.168.31.2
...
systemctl restart networking
ip a
```

Set up a partition for containers.

```sh
fdisk -l |grep -v loop|grep Disk
df -k
fdisk -l /dev/sdc
fdisk -l /dev/sdd
fdisk -l /dev/sdb
parted /dev/sdb
(parted) rm 5
(parted) mkpart 600GB 900GB
(parted) mkpart 900GB 100%
(parted) print
Model: ATA TEAM T2532TB (scsi)
Disk /dev/sdb: 2048GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system     Name  Flags
 1      1049kB  200GB   200GB   ext4            /
 2      200GB   201GB   1000MB  fat32           2     boot, esp
 3      201GB   501GB   300GB   ext3            3
 4      501GB   600GB   99.0GB  linux-swap(v1)  4     swap
 5      600GB   900GB   300GB                   5
 6      900GB   2048GB  1148GB                  6

(parted) quit
ls -lsa /dev/disk/by-id/|grep sdb
...
0 lrwxrwxrwx 1 root root  10 Oct 31 09:30 ata-TEAM_T2532TB_TPBF2402200040201609-part5 -> ../../sdb5
...
```

Install and initialize incus.
- existing bridge is br0
- zfs pool is on /dev/disk/by-id/ata-TEAM_T2532TB_TPBF2402200040201609-part5

To install 6.0 install from bookworm-backports.
```sh
apt -t bookworm-backports install incus incus-tools
incus admin init
```

To install the latest you need to follow the directions at https://github.com/zabbly/incus

```sh
apt install curl
curl -fsSL https://pkgs.zabbly.com/key.asc -o /etc/apt/keyrings/zabbly.asc
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
apt install incus incus-tools
```

Pull down the images you know you are going to use.

```sh
incus image list images: bookworm
incus image copy images:debian/12/cloud local:
incus image list images: trixie
incus image copy images:debian/trixie/cloud local:
incus image alias create bookworm 4ed6d8b34c84
incus image alias create trixie b0104c654d3d
incus image list
```

Set up a profile. This should be edited for things that no longer matter.

```sh
incus profile create susdev24<<EOD
name: susdev24
description: Try to create a sane environment for cloud-init based operating systems
config:
  user.network-config: |
    version: 1
    config:
      - type: physical
        name: eth0
        subnets:
          - type: static
            ipv4: true
            address: 198.202.31.200
            netmask: 255.255.255.128
            gateway: 198.202.31.129
            control: auto
      - type: nameserver
        address:
          - 198.202.31.132
          - 8.8.8.8
  user.user-data: |
    #cloud-config
    timezone: America/Vancouver
    users:
      - name: feurig
        passwd: "REDACTED"
        gecos: Donald Delmar Davis
        ssh-authorized-keys:
          - REDACTED
        groups: sudo,root,wheel
        shell: /bin/bash
      - name: joe
        passwd: "REDACTED"
        gecos: Joseph Wayne Dumoulin
        ssh-authorized-keys:
          - REDACTED
        groups: sudo,root,wheel
        shell: /bin/bash
    manage_resolv_conf: true
    packages:
    - python3
    - python-is-python3
    - python2
    - nano
    - openssh-server
    - less
    package_update: true
    package_upgrade: true
    write_files:
    - path: /etc/resolv.conf.static
      permissions: '0644'
      owner: root:root
      content: |
        nameserver 198.202.31.141
        nameserver 8.8.4.4
        search suspectdevices.com fromhell.com vpn
    - path: /usr/local/bin/update.sh
      permissions: '0774'
      owner: root:root
      content: |
        #!/bin/bash
        # update.sh for debian/ubuntu/centos  (copyleft) don@suspecdevices.com
        echo --------------------- begin updating `uname -n` ----------------------
        if [ -x "$(command -v apt-get)" ]; then
          apt-get update
          apt-get -y dist-upgrade
    # and the users are locked by default
    # cloud cart blanch accounts are inexcusable
    - sed -i "s/^127.0.0.1/#127.0.0.1/" /etc/hosts
    - echo 127.0.0.1 `hostname` localhost >>/etc/hosts
    - passwd joe -u
    - passwd feurig -u
    - userdel -f ubuntu
    - userdel -f centos
    - userdel -f opensuse
    - mv /etc/resolv.conf /etc/resolv.conf.foobarred
    - ln -s /etc/resolv.conf.static /etc/resolv.conf
    - netplan apply
    - apt-get install -y openssh-server nano less
    - apt-get install -y python-is-python3
    - apt-get install -y python
    power_state:
       mode: reboot
       message: See You Soon...
       condition: True
EOD
```

Launch a container

```sh
incus launch local:bookworm teddy -p default -p susdev24
incus list
incus exec teddy bash

```

YOU ARE HERE ADDING A SECTION ON INCUS TO INCUS TRUST....
