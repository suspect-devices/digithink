<!-- OperationsGuide, Version: 28, Modified: 2020/12/02, Author: feurig -->
# Server Modernization
## Overview 

![](images/ContainerShip.jpg)

### Phase I

Phase one of the server modernization shifted away from multipurposed servers and kvms to lxc/lxd based containers.

* Moving all legacy system functions onto separate linux containers isolated from each other.
* Use mirrored disk systems to insure that disk corruption does not lead to data corruption.
* Start giving a shit about the systems, code, and sites on them.
* Own your code/data. (If your free code hosting system is shutdown or taken over by Microsoft is it really free)

### Server Modernization Phase II

Phase two extends on this by integrate Ansible into system maintenance tasks.

* Integrate Ansible into system maintenance tasks
* Reevaluate Centos and other RPM based containers built using playbooks vs profiles/scripts/cloud-init _while maintaining current security model_
* Develop off site backup strategy.
* Clean up the cruft (If it doesn't bring you joy DTMFA)

### SMP III _Make Shit Happen / Own Your Shit_

* Work on secure and efficient traffic in and out of home lans (Privoxy,DNS based ad blocking,squid etc) 
* Continue to refine server operation/maintanance.
* ~~Build Gitlab and other alternatives to trac/git and evaluate workflows.~~
* Deploy off site backup strategy.
* Build out content. 
* Start new projects.
* Distribute data and backups over the network to home servers.
* [Document home server/network setup](edge-server-configuration/)

### SMP IV 
* Reduce colo footprint.
  * remove the dell.
* Dump Canonical
  * debian
  * incus
* Adapt Freebsd based firewall/router
  * wireguard
  * dnsmasq
  * pf

### Goals.

* Security
* Flexibility
* Simplification

### Isolation

* network
* performance
* disk

## Hardware

Starting in 2025 the environment contains a freebsd bassed router (Knight) and an enterprise class server 

* ~~kh2024 , a Dell PowerEdge R610 [[br]]and~~
* tk2018 a HP ProLiant DL380 (g7) .

## Network

The network is divided into 3 segments 

* 192.168.31.0/24 a private administrative lan
* 10.0.0.0/24 wireguard lan
* 198.202.31.129/25 A public facing lan.

The hosts themselves do not have any public facing interfaces and are only accessible though the admin lan. The containers which handle all public facing work do so via an anonymous bridge configuration, allowing them to access the internet directly without allowing external access to the servers.

### kh2024 network config (temporary)

|   |   |   |   |  kh2024 ports|
|---|---|---|---|-----------------|
|port| Interface| IP Address/mask |  linux device| purpose|
| 4 |  br0  |  0.0.0.0/0 | eno4 |Public Interface for dev/deploymant servers|
| 3 | N/A | N/A | eno3 | unused |
| 1 |  br1  | 192.168.31.158/24 | eno1 |internal / admin lan|
| idrac |   |  192.168.31.121/24 | |remote console|

As Drawn|As Deployed.
---|---
![](images/IMG_1402.jpg) | ![](images/r610Network.jpg)

/etc/network/interfaces
```
# https://ip4calculator.com
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

iface eno1 inet manual
iface eno2 inet manual
iface eno3 inet manual
iface eno4 inet manual


auto br0
iface br0 inet manual
     bridge_ports eno4
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay

auto br1
iface br1 inet static
     address 192.168.31.158
     network 192.168.31.0
     netmask 255.255.255.0
     broadcast 192.168.31.255
     bridge_ports eno1
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
```

### TK2022 Network Config

|   |   |   |   |    tk2022 ports|
|---|---|---|---|-----------------|
|port| Interface|IP Address/mask |  linux device| purpose |
| 4 |  br0  | 0.0.0.0/32    | enp4s0f1 | public interface for containers|
| 3 |  N/A  | ?.?.?.?/?? | N/A | unused |  
| 1 |  br1  | 192.168.31.159/24 | enp4s0f1 |internal / admin lan |
| ilo |   |  192.168.31.119/24 | |remote console|

As Drawn|As Deployed.
---|---
![](images/IMG_1401.jpg) | ![](images/DL380Network.jpg)

#### As implimented in /etc/network/interfaces

```
#--------------------------------------------------------/etc/network/interfaces
# 2: enp3s0f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br0 state UP group default qlen 1000
# 3: enp3s0f1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br1 state UP group default qlen 1000
# 4: enp4s0f0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
# 5: enp4s0f1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9000 qdisc mq master br3 state UP group default qlen 1000
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

iface enp3s0f0 inet manual
iface enp3s0f1 inet manual
iface enp4s0f0 inet manual
iface enp4s0f1 inet manual

auto br0
iface br0 inet manual
     bridge_ports enp3s0f0
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay


auto br1
iface br1 inet static
     address 192.168.31.159
     network 192.168.31.0
     netmask 255.255.255.0
     broadcast 192.168.31.255
     bridge_ports enp4s0f1
     bridge_stp off       # disable Spanning Tree Protocol
        bridge_waitport 0    # no delay before a port becomes available
        bridge_fd 0          # no forwarding delay
EOD
```

See: ​[https://bitbucket.org/suspectdevicesadmin/ansible/src/master/hosts](https://bitbucket.org/suspectdevicesadmin/ansible/src/master/hosts) which is built referencing [a google doc with proposed allocations](https://docs.google.com/spreadsheets/d/1KRkqdYvgRtV4vu6AGzdLWJVGTIsV2o2iSSJBEFMZJAw/edit#gid=0)

## Server OS, Filesystems and Disk layout
The servers are both running a standard install Ubuntu Server LTS, along with the Canonical supported LXD "snap". Outside of zfs not much is added to the stock installation. This is intentional. Since the real work is done by the containers the host os is considered disposable and can be rebuilt without effecting production.

### Disk Layout
The system disks on both servers use hardware raid 1+0 mirroring. The containers are able to take advantage of zfs mirroring and caching. 

|   |   |   |   |   |    bs2020 disks|
|---|---|---|---|---|-----------------|
|disk|device/pool | bay |  type|mount point(s)|purpose/notes| 
.... YOU ARE HERE FLESHING THIS IN ......

On kb2018 the second pair of disks are Solid State. The first partition on each is a mirrored pair for the infrastructure zfs pool. The remaining partitions are for zfs caching.

|   |   |   |   |   |   kb2018 disks|
|---|---|---|---|---|-----------------|
| disk| device/pool | bay |  type| mount point(s)| purpose/notes| 
... YOU ARE HERE ...


### Hardware raid on the DL380

The raid controller on the Dell allows a mixing of hardware raid and direct hot swappable connections. The HP 420i does only hardware raid or direct connections (HBA) but not both. Since we use the hardware raid the remaining disks need to be configured using the ssacli or the raid controllers bios.
See: DudeWhereAreMyDisks

## Containers

Work previously done by standalone servers is now done though incus managed containers. [#fn1 (1)]
An up to date list of containers is maintained at  https://bitbucket.org/suspectdevicesadmin/ansible/src/master/hosts''

## Ansible

Ansible is used to make most tasks reasonable including.
* creating containers
* updating containers
* updating admin passwords and ssh keys.
* accessing 

# Tasks: Accessing Hosts
### bs2020/kb2020 ssh access
The host machines for the containers can be accessed through the admin lan. This is done via wirguard on either [sitka](norouter/using-a-tank-for-crowd-control/) or [virgil](norouter/wireguard-and-tinyproxy/)
 
 
_note: as of a few updates ago you have to tell apples ssh client to use ssh-dss as below_

YOU ARE HERE updating this. 
```sh
steve:~ don$ ssh -p22 -oHostKeyAlgorithms=+ssh-dss feurig@bs2020.suspectdevices.com
User:feurig logged-in to kb2018.suspectdevices.com(192.168.31.119 / FE80::9E8E:99FF:FE0C:BAD8)
iLO 3 Advanced for BladeSystem 1.88 at  Jul 13 2016
Server Name: kb2018
Server Power: On

</>hpiLO-> vsp

Virtual Serial Port Active: COM2

Starting virtual serial port.
Press 'ESC (' to return to the CLI Session.

Ubuntu 18.04.1 LTS kb2018 ttyS1

kb2018 login: <ESC> (
</>hpiLO-> exit
steve:~ don$ ssh -p 222 feurig@vpn.suspectdevices.com
...
/admin1-> console com2
Connected to Serial Device 2. To end type: ^\

Ubuntu 18.04.1 LTS bs2020 ttyS1

bs2020 login: <CTL> \
/admin1-> exit
CLP Session terminated
Connection to vpn.suspectdevices.com closed.
steve:~ don$ 


_ if the serial port is still in use do the following _

Virtual Serial Port is currently in use by another session.
</>hpiLO-> stop /system1/oemhp_vsp1
```	
### bs2020/kb2018 graphical console access


tk2022 allows console access using the on board described on the [ilo 3 notes page](NotesOnILO3) This a requires access to the admin lan.

### ssh access to containers

The susdev profile adds ssh keys and sudo passwords for admin users allowing direct ssh access to the container.
	
```sh
steve:~ don$ ssh feurig@ian.suspectdevices.com
...
feurig@ian:~$ 
```	

The containers can be accessed directly from the incus host as root
	
```sh
root@bs2020:~# incus exec harvey bash
root@harvey:~# apt-get update&&apt-get -y dist-upgrade&& apt-get -y autoremove
```	

## Updating dns

Dns is provided by bind , The zone files have been consolidated into a single directory under /etc/bind/zones  on naomi (dns.suspectdevices.com).
YOU ARE HERE (update and add zone/config file checks)
```sh
root@naomi:/etc/bind/zones# nano suspectdevices.hosts
...
@               IN      SOA  dns1.digithink.com. don.digithink.com (
                2018080300 10800 3600 3600000 86400 )
;               ^^ update ^^
; .... make some changes ....
morgan          IN      A       198.202.31.224
git             IN      CNAME   morgan
...
root@naomi:/etc/bind/zones# service bind9 reload
root@naomi:/etc/bind/zones# tail /var/log/messages
...
Sep  3 08:10:04 naomi named[178]: zone suspectdevices.com/IN: loaded serial 2018080300
Sep  3 08:10:04 naomi named[178]: zone suspectdevices.com/IN: sending notifies (serial 2018080300)
Sep  3 08:10:04 naomi named[178]: client 198.202.31.132#56120 (suspectdevices.com): transfer of 'suspectdevices.com/IN': AXFR-style IXFR started (serial 2018080300)
Sep  3 08:10:04 naomi named[178]: client 198.202.31.132#56120 (suspectdevices.com): transfer of 'suspectdevices.com/IN': AXFR-style IXFR ended
Sep  3 08:10:04 naomi named[178]: client 198.202.31.132#47381: received notify for zone 'suspectdevices.com'
```	
	
## Updating Hosts / Containers

When updates are available Apticron sends us an email. We prefer this to autoupdating our hosts as it helps us maintain awareness of what issues are being addressed and does not stop working when there are issues. All hosts in /etc/asnsible/hosts on kb2018 shoul be updated using the following add hoc command. 

UPDATE WITH CURRENT bash.
	
```sh
root@kb2018:~# ansible pets -m raw -a "update.sh"
```	
https://bitbucket.org/suspectdevicesadmin/ansible/src/master/files/update.sh

## Creating containers
	
	ansible-playbook playbooks/create-lxd-containers.yml 
	
https://bitbucket.org/suspectdevicesadmin/ansible/src/master/roles/create_lxd_containers/tasks/main.yml
.....YOU ARE HERE.....
_documenting the ansible script to create containers_.

## Backing Up Containers

YOU ARE HERE REWORKING THIS

#  links.... (tbd)
