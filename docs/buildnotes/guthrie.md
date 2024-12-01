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

#### Utah to Guthrie

```
root@utah:~# incus config trust add guthrie
Client guthrie certificate add token:
eyJjbGllbnRfbmFtZSI6Imd1dGhyaWUiLCJmaW5nZXJwcmludCI6IjgwMDVmNDliNTdkMTUyMDZlNjI4MDE3M2YzNTljZjI1NjVhNDU2OWQ5MzkxMjExZWRhNDllNWMxNDFkNWU0MTIiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4wLjIwOjg0NDMiLCIxOTIuMTY4LjEyOS4xMDA6ODQ0MyJdLCJzZWNyZXQiOiI1ZWQzZmJjMjAzMjljMDZiOThiYzc1YzIxZmVmNmU2ZDFhZjM1Zjg0N2NmOTUxNWRjNDJlMjFkYmM2NzllODY1IiwiZXhwaXJlc19hdCI6IjAwMDEtMDEtMDFUMDA6MDA6MDBaIn0=
root@utah:~# incus remote add guthrie
Certificate fingerprint: bfe912ad8836a7457420506fc8e13369534077fe647184309363117ca5801ad4
ok (y/n/[fingerprint])? yes
Trust token for guthrie: eyJjbGllbnRfbmFtZSI6InV0YWgiLCJmaW5nZXJwcmludCI6ImJmZTkxMmFkODgzNmE3NDU3NDIwNTA2ZmM4ZTEzMzY5NTM0MDc3ZmU2NDcxODQzMDkzNjMxMTdjYTU4MDFhZDQiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4xMjkuMTgyOjg0NDMiXSwic2VjcmV0IjoiNTQ0NDg5MjlkMGNmNTA4M2ViNzc5ODFkMjc4OGNiNWMwYzNmMzI5NjhkNjE1ZTNjYWFjN2MxZjVmMTJlZDg2YiIsImV4cGlyZXNfYXQiOiIwMDAxLTAxLTAxVDAwOjAwOjAwWiJ9
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

#### Guthrie to Utah

```
root@guthrie:~# incus remote add utah
Generating a client certificate. This may take a minute...
Certificate fingerprint: 8005f49b57d15206e6280173f359cf2565a4569d9391211eda49e5c141d5e412
ok (y/n/[fingerprint])? y
Trust token for utah: eyJjbGllbnRfbmFtZSI6Imd1dGhyaWUiLCJmaW5nZXJwcmludCI6IjgwMDVmNDliNTdkMTUyMDZlNjI4MDE3M2YzNTljZjI1NjVhNDU2OWQ5MzkxMjExZWRhNDllNWMxNDFkNWU0MTIiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4wLjIwOjg0NDMiLCIxOTIuMTY4LjEyOS4xMDA6ODQ0MyJdLCJzZWNyZXQiOiI1ZWQzZmJjMjAzMjljMDZiOThiYzc1YzIxZmVmNmU2ZDFhZjM1Zjg0N2NmOTUxNWRjNDJlMjFkYmM2NzllODY1IiwiZXhwaXJlc19hdCI6IjAwMDEtMDEtMDFUMDA6MDA6MDBaIn0=
Client certificate now trusted by server: utah
root@guthrie:~# incus config add trust utah
Error: unknown command "add" for "incus config"
root@guthrie:~# incus config trust add utah
Client utah certificate add token:
eyJjbGllbnRfbmFtZSI6InV0YWgiLCJmaW5nZXJwcmludCI6ImJmZTkxMmFkODgzNmE3NDU3NDIwNTA2ZmM4ZTEzMzY5NTM0MDc3ZmU2NDcxODQzMDkzNjMxMTdjYTU4MDFhZDQiLCJhZGRyZXNzZXMiOlsiMTkyLjE2OC4xMjkuMTgyOjg0NDMiXSwic2VjcmV0IjoiNTQ0NDg5MjlkMGNmNTA4M2ViNzc5ODFkMjc4OGNiNWMwYzNmMzI5NjhkNjE1ZTNjYWFjN2MxZjVmMTJlZDg2YiIsImV4cGlyZXNfYXQiOiIwMDAxLTAxLTAxVDAwOjAwOjAwWiJ9
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