# incus install on kh2024

Currently just the bones.
You are here fleshing them in.

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
... split off a 300G partition for infra pool ...
ls -lsa /dev/disk/by-id/|grep sdb
... save this for infra partition device ...
```

Install and initialize incus

```sh
apt -t bookworm-backports install incus incus-tools
incus admin init
```

Pull down the images you know you are going to use.

```sh
incus image list images: bookworm
incus image copy images:debian/12/cloud local:
incus image list images: trixie
incus image copy images:debian/trixie/cloud local:
incus alias add bookworm 4ed6d8b34c84
incus alias add trixie b0104c654d3d
incus image alias create bookworm 4ed6d8b34c84
incus image alias create trixie b0104c654d3d
incus image list

```

Set up a profile.

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
