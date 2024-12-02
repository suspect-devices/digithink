# Guthrie rebuild 

Guthrie is Utah's partner in home service.
It is also the last ubuntu server and since it does my girlfriends backup its probably the most important.

### Install incus and convert the lxd containers to incus. 

```
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
```

### establishing remotes and trust between nodes

#### Guthrie to Utah

##### Generate trust token

```sh
root@utah:~# incus config trust add guthrie
Client guthrie certificate add token:
eyJjbGllbnRfbmFtZSI6Imd1dGhyaWUiLCJmaW5nZXJwcmludCI6IjgwMDVmNDliNTdkMTUyMDZlNjI4MDE3M2YzNTljZjI1NjVhNDU2OWQ5MzkxMjExZWRhNDllNWMxNDFkNWU0MTIiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4wLjIwOjg0NDMiLCIxOTIuMTY4LjEyOS4xMDA6ODQ0MyJdLCJzZWNyZXQiOiI1ZWQzZmJjMjAzMjljMDZiOThiYzc1YzIxZmVmNmU2ZDFhZjM1Zjg0N2NmOTUxNWRjNDJlMjFkYmM2NzllODY1IiwiZXhwaXJlc19hdCI6IjAwMDEtMDEtMDFUMDA6MDA6MDBaIn0=
```

##### Use it to add remote

```sh
root@guthrie:~# incus remote add utah
Generating a client certificate. This may take a minute...
Certificate fingerprint: 8005f49b57d15206e6280173f359cf2565a4569d9391211eda49e5c141d5e412
ok (y/n/[fingerprint])? y
Trust token for utah: <paste token from above>
Client certificate now trusted by server: utah
root@guthrie:~# incus list utah:
+-------------+---------+------------------------------+------+-----------+-----------+
|    NAME     |  STATE  |             IPV4             | IPV6 |   TYPE    | SNAPSHOTS |
+-------------+---------+------------------------------+------+-----------+-----------+
| bunnyfoofoo | RUNNING | 192.168.128.152 (eth0)       |      | CONTAINER | 0         |
+-------------+---------+------------------------------+------+-----------+-----------+
| haley       | RUNNING | 192.168.129.198 (eth0)       |      | CONTAINER | 0         |
|             |         | 172.18.0.1 (br-a4e161520842) |      |           |           |
|             |         | 172.17.0.1 (docker0)         |      |           |           |
+-------------+---------+------------------------------+------+-----------+-----------+

```

#### Utah to Guthrie

##### Generate trust certificate

```sh
root@guthrie:~# incus config trust add utah
Client utah certificate add token:
eyJjbGllbnRfbmFtZSI6InV0YWgiLCJmaW5nZXJwcmludCI6ImJmZTkxMmFkODgzNmE3NDU3NDIwNTA2ZmM4ZTEzMzY5NTM0MDc3ZmU2NDcxODQzMDkzNjMxMTdjYTU4MDFhZDQiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4xMjkuMTgyOjg0NDMiXSwic2VjcmV0IjoiNTQ0NDg5MjlkMGNmNTA4M2ViNzc5ODFkMjc4OGNiNWMwYzNmMzI5NjhkNjE1ZTNjYWFjN2MxZjVmMTJlZDg2YiIsImV4cGlyZXNfYXQiOiIwMDAxLTAxLTAxVDAwOjAwOjAwWiJ9
```

##### Use it to add remote

```sh
root@utah:~# incus remote add guthrie
Certificate fingerprint: bfe912ad8836a7457420506fc8e13369534077fe647184309363117ca5801ad4
ok (y/n/[fingerprint])? yes
Trust token for guthrie: <Paste token from above>
Client certificate now trusted by server: guthrie
root@utah:~# incus list guthrie:
+-----------+---------+------------------------------+------+-----------------+-----------+
|   NAME    |  STATE  |             IPV4             | IPV6 |      TYPE       | SNAPSHOTS |
+-----------+---------+------------------------------+------+-----------------+-----------+
| annie     | RUNNING | 192.168.129.110 (enp5s0)     |      | VIRTUAL-MACHINE | 0         |
+-----------+---------+------------------------------+------+-----------------+-----------+
| dick      | RUNNING | 192.168.129.183 (enp5s0)     |      | VIRTUAL-MACHINE | 1         |
+-----------+---------+------------------------------+------+-----------------+-----------+
| gail      | RUNNING | 192.168.129.192 (eth0)       |      | CONTAINER       | 3         |
|           |         | 172.18.0.1 (br-a4e161520842) |      |                 |           |
|           |         | 172.17.0.1 (docker0)         |      |                 |           |
+-----------+---------+------------------------------+------+-----------------+-----------+
| jobs      | RUNNING | 192.168.129.187 (eth0)       |      | CONTAINER       | 0         |
+-----------+---------+------------------------------+------+-----------------+-----------+
| katherine | RUNNING | 192.168.129.188 (eth0)       |      | CONTAINER       | 0         |
+-----------+---------+------------------------------+------+-----------------+-----------+
| luigi     | RUNNING | 192.168.129.250 (eth0)       |      | CONTAINER       | 0         |
+-----------+---------+------------------------------+------+-----------------+-----------+
```

### Temporarily transfer containers to Utah

luigi should be started since unlike the other containers it isnt providing a service tied to guthries storage.

```sh
root@utah:~# incus stop guthrie:luigi\
 && incus move guthrie:luigi luigi\
 && incus start luigi
```

Stop remaining containers and move them.

```sh
root@utah:~# incus stop guthrie:annie
root@utah:~# incus move guthrie:annie annie
root@utah:~# incus stop guthrie:dick
root@utah:~# incus move guthrie:dick dick
... continue for all containers on guthrie...
```


## Install debian on guthrie.

### Prep
#### free up the target disk (currently mirroring the ubuntu zfsroot)

```
parted /dev/nvme0n1 print
zpool status -L
zfs status local
zpool status local
zpool detach local nvme-TEAM_TM8FP6002T_TPBF2306190020902551-part5
zpool status -L rpool
zpool status rpool
zpool detach nvme-TEAM_TM8FP6002T_TPBF2306190020902551-part4
zpool detach rpool zpool status bpool -L
zpool detach bpool zpool detach bpool 1f1027f1-c44d-7f42-a71b-8bdff56b3a51
```
get rid of any zfs stuff. 
The debian installer (for bookworm anyways)tends to freak out and not want to install on anything with zfs on it.

```sh
wipefs -fa /dev/nvme0n1
```

save some stuff for later

```sh
df -k
parted /dev/nvme0n1 print
mkdir /tank/oldguthrie/
cp /etc/netatalk/afp.conf /tank/oldguthrie/
cp -rpv /etc/ssh /tank/oldguthrie/
mkdir /tank/oldguthrie/root
cp -rpv .bash_history .bashrc .config .local .profile .selected_editor .ssh zplan go /tank/oldguthrie/root/
```

### Install stuff you will want installed.


```sh
apt install openssh-server
apt install ca-certificates
apt install curl
apt install gpg
apt install sudo
apt install parted
apt install htop
apt install bridge-utils
```

start the sshd and go upstairs to finish this.

```sh
systemctl enable sshd
systemctl start sshd
```

get rid of the graphical runtime before the system goes to sleep.

```sh
systemctl set-default multi-user.target
reboot

```
set up sudo
```
visudo
.... add feurig ....
```

### Install zfs from trixie

```sh
apt -t bookworm-backports install zfs-dkms zfs-zed zfsutils-linux
modprobe zfs
```

Import the data pools.

```sh
zpool import
zpool import -f archive
zpool import -f home
zpool import -f tank
zpool import -f filebox
```

### Set up networking as it was before

Forgot a few things mount the old ubuntu root

```sh
mkdir /tmp/mnt
zpool import
zpool import -f rpool orpool
zfs set mountpoint=/tmp/mnt orpool/ROOT/ubuntu_lrmg80
zfs mount orpool/ROOT/ubuntu_lrmg80 
cp /tmp/mnt/etc/netplan/00-merlot.yaml /tank/oldguthrie/
```

Set /etc/network/interfaces

```sh
cat /etc/network/interfaces|sed
ip a|sed 's/^/# /'
ip a|sed 's/^/# /'>/etc/network/interfaces
nano /etc/network/interfaces
auto lo
iface lo inet loopback

allow-hotplug enp9s0
auto enp9s0
#iface enp10s0 inet dhcp
iface enp9s0 inet manual

auto br0
iface br0 inet static
     address 192.168.129.182
     network 192.168.128.0
     netmask 255.255.128.0
     broadcast 192.168.255.255
     gateway 192.168.128.1
     mtu 9000
     bridge_ports enp10s0
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
^X
reboot
```

### Install incus from zabbly repo.

```sh
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
```

Clear all of the zfs data from ubuntu disk otherwise incus will bitch about the old local pool

```sh
ls -ls /dev/disk/by-id|grep nvme1n1
zpool export orpool
wipefs -af /dev/disk/by-id/nvme-T-CREATE_TM8FPE002T_112108250100368
```
Initialize incus 
- create new local pool (with above device)
- use existing bridge (br0)

```sh

incus admin init
systemctl enable incus
systemctl start incus

```
Add utah to /etc/hosts and generate trust key 

```sh
nano /etc/hosts
incus config trust add utah
```

on utah remove old remote, generate trust key, and re add guthrie as a remote

```sh
incus remote remove guthrie
incus config trust add guthrie
incus remote add guthrie
incus list guthrie:
```

Add utah as a remote.

```sh
incus remote add utah
incus list utah:
```

### Install netatalk 4 from netatalk.io

```sh
wget https://github.com/Netatalk/netatalk/releases/download/netatalk-4-0-0/netatalk_4.0.0.ds-1_amd64.deb
apt install ./netatalk_4.0.0.ds-1_amd64.deb
cp /tank/oldguthrie/afp.conf /etc/netatalk/afp.conf.new
nano /etc/netatalk/afp.conf
systemctl enable netatalk
systemctl start netatalk
systemctl status netatalk
apt install avahi-daemon
apt enable avahi-daemon
systemctl enable avahi-daemon
systemctl restart avahi-daemon
systemctl status avahi-daemon
systemctl restart netatalk
```

### Wrapup

- test backups on girlfriends system
- test containers