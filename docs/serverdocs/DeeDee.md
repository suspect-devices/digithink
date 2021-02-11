<!-- DeeDee, Version: 18, Modified: 2020/08/29, Author: feurig -->
## Basement Server Setup
''Hey Daddy O. I don't wanna go, down to the basement"

DeeDee, [wiki:Joey Joey], and [wiki:Annie Annie] are hp z400s intended to be used at the home lans. They provide the following services to the lan.
* Dns filtering via pihole
* Http/s caching via squid.
* Distributed file sharing / private cloud backup (mechanism tbd)
* LXD Container based services
* Zero Configuration Networking
* ZFS/Mirrored File Sharing.
* (planned : sso)
### Example Home Network Configuration
[[Image(wiki:Annie:Home Network Diagram.jpg, width=70%)]]
#### Initial PDX Network Configuration
Our portland location has internet through Century Link. Largely because they have proven them selves  historically trustable to not sell all of our personable data to the government.

Initially we set up our home servers on a single /24 network.
However our router did some things that made me uncomfortable. 
* The routers operating system is proprietary and can not be replaced (easily)
* The default settings were way insecure.
* Even though it was a private network the router refused to let it be larger than a class-c network. 
* The dns from the router provided some sketch redirection including outside resolution of .lan and .local addresses.
#### Improved PDX network configuration. 
Treating the initial network  with the same disdain and suspicion as the greater internet beyond we segmented the network into the original private c block, and a half b class network connected via  [wiki:GoldCoastRouter a router running openwrt 19.07].   
* Local addresses and name resolution are handled by the router.
* External DNS is tied to a filtering server hosted on the Home server (Pihole via an LXD Container)
* A caching server (squid) is also hosted on one of the servers.
* Services which are meant to interact with the outside world are connected to the upstream router treating its network as a DMZ.

### Basement Server Hardware.
Our current platform for the home server is the HP z400 workstation which is capable of file serving as well as LXD based containers. All servers should have at least 12G of memory and an sas raid controller, more info on upgrades etc can be found on my [wiki:NotesForHPZ400Workstation Z400 notes page], I also put an ssd and a second GB Nic into Joey for transferring data between the internet, our internet deployed containers, and our home servers. 

To stage DeeDee I used one of the 500GB hp disks for booting and one 600G SAS drive for infrastructure containers and data. These disks and the raid controller were sent to be installed once I have the rudimentary system in place. Once tested I recommend installing a second sas drive to mirror the data.

### OS Installation.
Much like the servers at the cool Ubuntu 18.04 was installed using the alternate installer, _(Tasksel: Samba, SSH and Basic ubuntu servers)_. In addition, zfsutils were installed: not much else.

### LXD Configuration
lxd was initialized using the scsi id of the SAS disk (in hopes that the disk will just show up when installed in new system)
	
	oot@DeeDee:~# zpool status
	  pool: infra
	 state: ONLINE
	  scan: none requested
	config:
	
		NAME                                      STATE     READ WRITE CKSUM
		infra                                     ONLINE       0     0     0
		  scsi-3600508b1001cd7e650c500a2e7a5a52d  ONLINE       0     0     0
	
	
Since we have an existing lxd server we allow connections to the daemon.
	
	root@DeeDee:~# lxc config set core.https_address [::]:8443
	root@DeeDee:~# lxc config set core.trust_password ~~something secure~~
	
We have a working pi-hole container. Copy it from Annie.
_Also the susdev19 profile contains users and some minor tweaks. _
	
	root@annie:~# lxc profile copy susdev19 deedee:
	root@annie:~# lxc snapshot deniro pihole27jul19
	root@annie:~# lxc move deniro/pihole27jul19 deedee:pihole
	
### squid container
To create the container we set up a profile for the disk and network and create it from a ubuntu-its image.
	
	root@DeeDee:~# lxc image copy ubuntu:18.04 local: --alias=ubuntu-lts
	root@DeeDee:~# lxc profile create infra
	Profile infra created
	root@DeeDee:~# lxc profile edit infra
	config: {}
	description: LXD profile for infrastructure
	devices:
	  eth0:
	    name: eth0
	    nictype: bridged
	    parent: br0
	    type: nic
	  root:
	    path: /
	    pool: infra
	    type: disk
	name: infra
	root@DeeDee:~# lxc init ubuntu-lts squid -p susdev19 -p infra
	Creating squid
	root@DeeDee:~# lxc start squid
	root@DeeDee:~# lxc exec squid bash
	root@squid:~# nano /etc/netplan/50-cloud-init.yaml 
	root@squid:~# reboot
	root@squid:~# root@DeeDee:~# 
	root@DeeDee:~# lxc list
	+--------+---------+----------------------+------+------------+-----------+
	|  NAME  |  STATE  |         IPV4         | IPV6 |    TYPE    | SNAPSHOTS |
	+--------+---------+----------------------+------+------------+-----------+
	| pihole | RUNNING | 192.168.0.254 (eth0) |      | PERSISTENT | 0         |
	+--------+---------+----------------------+------+------------+-----------+
	| squid  | RUNNING | 192.168.0.252 (eth0) |      | PERSISTENT | 0         |
	+--------+---------+----------------------+------+------------+-----------+
	
	
Then we can update the image and install squid.
	
	root@DeeDee:~# lxc exec squid bash
	root@squid:~# update.sh 
	--------------------- begin updating squid ----------------------
	...
	======================#### done==========================
	root@squid:~# apt-get install squid
	...
	Do you want to continue? [Y/n] 
	...
	root@squid:~# nano /etc/squid/squid.conf
	acl SSL_ports port 443
	acl Safe_ports port 80          # http
	acl Safe_ports port 21          # ftp
	acl Safe_ports port 443         # https
	acl Safe_ports port 70          # gopher
	acl Safe_ports port 210         # wais
	acl Safe_ports port 1025-65535  # unregistered ports
	acl Safe_ports port 280         # http-mgmt
	acl Safe_ports port 488         # gss-http
	acl Safe_ports port 591         # filemaker
	acl Safe_ports port 777         # multiling http
	acl CONNECT method CONNECT
	http_access deny !Safe_ports
	http_access deny CONNECT !SSL_ports
	http_access allow localhost manager
	http_access deny manager
	http_access allow localhost
	acl my_internal_net src 192.168.0.0/24
	http_access allow my_internal_net
	#http_port 3128 transparent
	http_port 3128
	coredump_dir /var/spool/squid
	refresh_pattern ^ftp:           1440    20%     10080
	refresh_pattern ^gopher:        1440    0%      1440
	refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
	refresh_pattern (Release|Packages(.gz)*)$      0       20%     2880
	refresh_pattern .               0       20%     4320
	
	

### Segmenting the network

I purchased an Asus RT-N56U a while back because it had plenty of memory making it ideal to run openwrt. Once I was able to get a stock 18.06 image on it I set up the new network.  The wan interface was set to get its address from the upstream router.
	
	root@mullein:/etc/config# nano network 
	...
	config interface 'lan'
		option type 'bridge'
		option ifname 'eth0.1'
		option proto 'static'
		option ipaddr '192.168.129.1'
		option netmask '255.255.128.0'
	
	config interface 'wan'
		option ifname 'eth0.2'
		option proto 'dhcp'
	...
	 
#### Adding a second bridge
By adding a second 1G network card to each of the basement servers we can redefine our network so that the containers face the DMZ while the local (file server/pihole/etc) interface is on the new home network.
	
	root@annie# nano /etc/netplan/50-cloud-init.yaml   
	network:
	  version: 2
	  renderer: networkd
	  ethernets:
	    ens6:
	        dhcp4: no
	        dhcp6: no
	    enp1s0:
	        dhcp4: no
	        dhcp6: no
	  bridges:
	    br1:
	        dhcp4: no
	        dhcp6: no
	        addresses:
	            - 192.168.129.69/17
	        gateway4: 192.168.129.1
	        nameservers:
	            addresses:
	                - 192.168.129.1
	                - 198.202.31.141
	        interfaces:
	            - enp1s0
	    br0:
	        dhcp4: no
	        dhcp6: no
	        interfaces:
	            - ens6
	root@annie # netplan apply
	
_.... todo: Document moving containers to br1 ...._
## References / Notes

#### Yaml from lxd init
	
	config: {}
	networks: []
	storage_pools:
	- config:
	    source: /dev/disk/by-id/scsi-3600508b1001cd7e650c500a2e7a5a52d
	  description: ""
	  name: infra
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
	      pool: infra
	      type: disk
	  name: default
	cluster: null
	
	