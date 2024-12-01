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