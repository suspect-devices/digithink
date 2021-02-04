# Overview[[Image(OperationsGuide:ContainerShip.jpg)]]


* Goals.
* Security
* Flexibility
* Simplification
* Isolation
* network
* performance
* disk
## Systems
At present the environment  contains a vpn capable router (Knight) and two enterrise class servers 
* bs2020 , a Dell PowerEdge R610 [[br]]and 
* kb2018 a HP ProLiant DL380 (g7) .

## Network
The network is divided into 3 segments 
* 192.168.31.0/24 a private administrative lan
* tbd.tbd.tbd.tbd/? a private vpn for home offices
* 198.202.31.129/25 A public facing lan.

The hosts themselves do not have any public facing interfaces and are only accessible though the admin lan. The containers which handle all public facing work do so via an anonymous bridge configuration, allowing them to access the internet directly without allowing external access to the servers.

|   |   |   |   |   # bs2020 ports|
|---|---|---|---|-----------------|
|# port|# Interface|# IP Address/mask |  linux device| purpose |
| 1 |  eno1  |   192.168.31.158/24  | eno1 |internal / admin lan  |
| 2 |  ?  | ?.?.?.?/?? | eno2 | vpn for home/office networks  |  
| 3 |  br1  | 0.0.0.0/0 | eno3 |Public Interface for infrastructure servers|
| 4 |  br0  |  0.0.0.0/0 | eno4 |Public Interface for dev/deploymant servers|
| idrac |   |  192.168.31.121/24 | |remote console|
||||||[[Image(OperationsGuide:IMG_1402.jpg,80%)]]||||[[Image(OperationsGuide:r610Network.jpg,70%)]]


|   |   |   |   |   # kb2018 ports|
|---|---|---|---|-----------------|
|# port|# Interface|# IP Address/mask |  linux device| purpose |
| 4 |  enp4s0f1  |   192.168.31.159/24  | enp4s0f1 |internal / admin lan  |
| 3 |  enp4s0f0  | ?.?.?.?/?? | enp4s0f0 | vpn for home/office networks  |  
| 2 |  br1  | 0.0.0.0/32 | enp3s0f1 |Public Interface for infrastructure servers|
| 1 |  br0  |  0.0.0.0/32 | enp3s0f0 |Public Interface for dev/deploymant servers|
| ilo |   |  192.168.31.119/24 | |remote console|
|||||||[[Image(OperationsGuide:IMG_1401.jpg,70%)]]||||[[Image(OperationsGuide:DL380Network.jpg,70%)]]

See: [Google Dock with proposed allocations](https://docs.google.com/spreadsheets/d/1KRkqdYvgRtV4vu6AGzdLWJVGTIsV2o2iSSJBEFMZJAw/edit#gid=0)

### Server OS, Filesystems and Disk layout
The servers are both running a standard install Ubuntu Server 18.04.1 along with the Canonical supported LXD "snap". Outside of zfs not much was added to the stock installation. This is intentional. Since the real work is done by the containers the host os is considered disposable and can be rebuilt without effecting production.

#### Disk Layout
The system disks on both servers use hardware raid 1+0 mirroring. The containers are able to take advantage of zfs mirroring and caching. 
|   |   |   |   |   |   # bs2020 disks|
|---|---|---|---|---|-----------------|
|# disk|# device/pool | bay |  type|# mount point(s)|# purpose/notes| 
|   |   |   |   |   |   Host Machine Disks  |
|sdg|/dev/sdg|0|ext4|/|root filesytem (hardware raid)|
|sdg|/dev/sdg|1|ext4|/|mirror|
|sda1|/dev/sda1|external|ext4|/archive|backup staging|
|   |   |   |   |   |   development zfs pool  |
|sdc|devel|2|zfs|/var/lib/lxd/storage-pools/devel|dev/deployment (www,trac,usw)|
|sdd|devel|3|zfs| | mirror |
|   |   |   |   |   |   development zfs pool  |
|sdd|infra|4|zfs|/var/lib/lxd/storage-pools/infra|infrastructure (email,dns,usw)|
|sde|infra|5|zfs| | mirror |

On kb2018 the second pair of disks are Solid State. The first partition on each is a mirrored pair for the infrastructure zfs pool. The remaining partitions are for zfs caching.
|   |   |   |   |   |   # kb2018 disks|
|---|---|---|---|---|-----------------|
|# disk|# device/pool | bay |  type|# mount point(s)|# purpose/notes| 
|   |   |   |   |   |   Host Machine Disks  |
|sda|/dev/sda|0|ext4|/|root filesytem (hardware raid)|
|sda|/dev/sda|1|ext4|/|mirror|
|   |   |   |   |   |   infrastructure zfs pool  |
|sdb1|infra|2|zfs|/var/lib/lxd/storage-pools/infra|infrastructure (email,dns,usw)|
|sdc1|infra|3|zfs| | mirror |
|   |   |   |   |   |   development zfs pool  |
|sdd|devel|4|zfs|/var/lib/lxd/storage-pools/devel|dev/deployment (www,trac,usw)|
|sde|devel|5|zfs| | mirror |
|sdb2|devel|2|zfs| | zfs cache (proposed) |

## Containers
The majority of the work previously done by standalone servers is now done though LXD managed containers. [#fn1 (1)]
### LXD Containers (development/deployment)

|#  NAME |#  OS |#  IP|# zfs pool|# Purpose |# Notes|
|--------|------|-----|----------|----------|-------|
| kb2018/naomi   | Ubuntu 16.04 |198.202.31.225|infra| primary dns / email|   |
| kb2018/ernest   | Ubuntu 16.04 |198.202.31.225|devel| bresgal.com content|   |
| kb2018/oldtrac   | Ubuntu 16.04 |198.202.31.221|devel| trac/git |  |
| kb2018/ian   | Ubuntu 16.04  |198.202.31.222|devel|wordpress/blog.suspectdevices.com | |
| kb2018/kurt   | Ubuntu 16.04  |198.202.31.230|devel|lighthttp/static sites busholini,digithink,softtargets| |
| bs2020/phillip   | Ubuntu 18.10 |198.202.31.223|devel|Bleeding Edge |  |
| kb2018/morgan   | Ubuntu 18.04 |198.202.31.224|devel| |  |
| kb2018/sandbox  | Ubuntu 18.04 |198.202.31.191|devel|Development/OpenWRT Build|   |
| bs2020/teddy   | Ubuntu 16.04 |198.202.31.132|infra|Secondary DNS|  |

# Tasks: Accessing Hosts
### bs2020/kb2020 ssh access
The host machines for the containers can be accessed through the admin lan. Currently this is done through ssh redirection. Eventually it will require a vpn connection. Only ssh key access is allowed and root is not allowed to login. To escalate privileges requires sudo. 

 ||||# Current ssh port mappings to vpn.suspectdevices.com||
 
  port |destination 
  ---- |----
  22   | bs2020 ssh via admin lan 
  222  | bs2020 racadm / serial console via ssh 
  2222 | knight / vpn 
  22222 |kb2018 hpILO / serial console via ssh
  22223 |kb2018 ssh via admin lan

	
	steve:~ don$ ssh -p 22222 feurig@vpn.suspectdevices.com
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
	
### bs2020/kb2018 graphical console access
bs2020 allows complete control of the system via a Dell Idrac 6 controller. This also requires access to the admin lan. This is described on the [wiki:Idrac6 Idrac 6 page]
kb2020 allows similar using the on board described on the [wiki:ILO3Notes ILO 3 Notes page.]
### ssh access to containers
The susdev profile adds ssh keys and sudo passwords for admin users allowing direct ssh access to the container.
	
	steve:~ don$ ssh feurig@ian.suspectdevices.com
	...
	feurig@ian:~$ 
	
The containers can be accessed directly from the lxc/lxd host as root
	
	root@bs2020:~# lxc exec harvey bash
	root@harvey:~# apt-get update&&apt-get -y dist-upgrade&& apt-get -y autoremove
	

## Updating dns
Dns is provided by bind , The zone files have been consolidated into a single directory under /etc/bind/zones  on naomi (dns.suspectdevices.com).
	
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
	
	
## Updating hosts
The process for updating hosts is handled via apt-get in 3 steps. [#2 (2)]
1. update == check repos
2. dist-upgade == apply updates
3. dist-upgrade == clean up

	
	root@bs2020:~# apt-get update&&apt-get dist-upgrade&& apt-get autoremove
	
### updating containers
#### update.sh
 After revisiting the major players (ansible, puppet, etc) and not finding them to be simple or straightforward, I found a script or two that does more or less what was needed. After using this script for updates I arrived at a simple script (/usr/local/bin/update.sh) that could be pushed to the containers. This script should be tailored to the os (the current script is debian/ubuntu focused), and should probably be added by the local profile at container creation time.
	
	root@kb2018:~# cat /usr/local/bin/update.sh
	#!/bin/bash
	# update.sh for debian/ubuntu  (copyleft) don@suspecdevices.com
	echo --------------- begin updating `uname -n` ----------------
	apt-get update
	apt-get -y dist-upgrade
	apt-get -y autoremove
	echo ==================#### done====================
	root@kb2018:~# 
	
Deploying the script using either basic shell commands or shell/awk is fairly straight forward. 
	
	root@kb2018:~# lxc list -c n --format csv|awk '{print "lxc file push /usr/local/bin/update.sh " $1 "/usr/local/bin/"}' |bash
	
Since the hosts are on a private lan they are configured to trust each other. This means that the above deployment can be pushed to the other server as well. 
	
	root@kb2018:~# lxc list bs2020: -c n --format csv|awk '{print "lxc file push /usr/local/bin/update.sh bs2020:" $1 "/usr/local/bin/"}' |bash
	
Running the script is equally simple. 
	
	root@kb2018:~# for h in `lxc list bs2020: -c n --format csv ` ;do lxc exec bs2020:$h update.sh; done
	root@kb2018:~# for h in `lxc list local: -c n --format csv ` ;do lxc exec local:$h update.sh; done
	
## Creating containers
Currently only current ubuntu (18.04) is downloaded for creating hosts. Any other hosts will require manual configuration or use of a custom profile.
### hosts
	
	root@bs2020:~# lxc image list kb2018:
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	|   ALIAS    | FINGERPRINT  | PUBLIC |                 DESCRIPTION                 |  ARCH  |   SIZE   |          UPLOAD DATE          |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	| ubuntu-lts | ae465acff89b | no     | ubuntu 18.04 LTS amd64 (release) (20180613) | x86_64 | 173.14MB | Jun 16, 2018 at 10:07pm (UTC) |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	root@bs2020:~# lxc init kb2020:ubuntu-lts test18 -p susdev
	Creating test18
	root@bs2020:~# lxc start test18 
	root@bs2020:~# lxc exec test18 bash
	root@test18:~# nano /etc/netplan/50-cloud-init.yaml 
	network:
	  version: 2
	  ethernets:
	    eth0:
	      dhcp4: no
	      addresses: [198.202.31.216/25]
	      gateway4: 198.202.31.129
	      nameservers:
	        search: [suspectdevices.com fromhell.com vpn]
	        addresses: [198.202.31.141]
	root@test18:~# reboot
	root@test18:~# update.sh
	root@test18:~# root@bs2020:~# lxc list
	+----------+---------+--------------------------------+------+------------+-----------+
	|   NAME   |  STATE  |              IPV4              | IPV6 |    TYPE    | SNAPSHOTS |
	+----------+---------+--------------------------------+------+------------+-----------+
	....
	+----------+---------+--------------------------------+------+------------+-----------+
	| test18   | RUNNING | 198.202.31.216 (eth0)          |      | PERSISTENT | 0         |
	+----------+---------+--------------------------------+------+------------+-----------+
	root@bs2020:~# 
	
## Backing Up Containers
The simplest way to back up a host is to create a snapshot, and move or copy the snapshot to the other server. [#fn3 (3)]
	
	root@kb2018:~# lxc snapshot oldtrac 7oct2018
	root@kb2018:~# lxc move oldtrac/7oct2018 bs2020:oldtrac7oct2018
	root@kb2018:~# lxc stop bs2020:oldtrac7oct2018
	
At that point you can publish or send via zfs the containers data-pool. 
	
	root@bs2020:~# zfs send devel/containers/oldtrac7oct2018> /archive/zfsback/oldtrack.07oct18
	
	
####  links
* https://lxd.readthedocs.io/en/latest/backup/
* https://s3hh.wordpress.com/2016/05/08/using-lxd-snapshots/
* https://blog.ubuntu.com/2015/03/20/installing-lxd-and-the-command-line-tool
* https://www.virtualizationhowto.com/2018/09/installing-and-configuring-ubuntu-server-18-04-lts/
* http://blog.dustinkirkland.com/2018/02/rfc-new-ubuntu-1804-lts-server-installer.html
* https://blog.printk.io/2018/04/ubuntu-18-04-lts-bionic-beaver-server-installer-differences/
* https://github.com/lxc/lxd/issues/4526
* https://github.com/lxc/lxd/issues/4619
* https://docs.oracle.com/cd/E19253-01/819-5461/gbcya/index.html
* http://lxd.readthedocs.io/en/latest/backup/#container-backup-and-restore
* https://stgraber.org/2016/03/30/lxd-2-0-image-management-512/
* https://github.com/lxc/lxd/issues/2669
* https://github.com/lxc/lxd/issues/3730
* https://www.thegeekdiary.com/zfs-tutorials-creating-zfs-snapshot-and-clones/
* https://pthree.org/2012/12/19/zfs-administration-part-xii-snapshots-and-clones/
* https://serverfault.com/questions/74411/best-compression-for-zfs-send-recv
* http://everycity.co.uk/alasdair/2010/07/using-mbuffer-to-speed-up-slow-zfs-send-zfs-receive/
* http://www.polyomica.com/improving-transfer-speeds-for-zfs-sendreceive-in-a-local-network/
### Foot Notes
[=#fn1 1] ) The original purpose of this server was to evaluate openstack.

Openstack requires relinquishing complete control of the host server to an overtly complicated pile of layers which once installed cannot be uninstalled without completely re-inststalling the entire operating system. This is not that unusual (my first installation of puppet was equally badly behaved and destructive ) but it does not instill confidence in software with cart blanch access to everything.

See: [wiki:GoodByeOpenstack]

Our search for a way to deploy such an insecure POS led us to look deeply into the lightweight container system provided by lxc. We attempted to create an isolated server for openstack/devstack that can be uninstalled and which will not shit all over everything. (Attempting to containerize devstack was as disastrous as trying to uninstall it)
 
In the process we discovered a wy to create a public facing server for dns/email/and other services which is isolated from other containers and can not access the host directly.

By extending this new set of tools we are also able to to create user space containers for experimentation which are in themselves isolated from everything else.

[=#fn2 2] ) Ubuntu can be  configured to auto update however in my experience this leads to a false sense of security and a lack of awareness of what is broken/changing. Also, when autoupdates fail they do not recover gracefully, will not apply the next set of updates, and it's a major pain in the ass to fix them. For this reason I tend to use apticron to notify us when updates are available and manually update them. 

For BS2020 and naomi, I also tend to look at what is being done instead of adding the -y parameter to apt-get.

[=#fn3 3] ) There are some side effects to this method for instance moving to a new server can apply the other servers default profile to it. I have also noticed that moving from a snapshot to a new container starts the new container.  