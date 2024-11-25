# FIRST IMPRESSIONS: 

Creating LXD Container with Static IP (and Docker Profile)We want to create a docker capable LXD container using an existing bridge with a static ip and zfs. Then we want to install docker and test it. We will make a copy of this container once the admin users have been added so that we wont have to replicate these tasks. Our security model requires ssh keys to log in AND passwords to escalate privileges.

The first thing we learned is that LXC and LXD are pretty different beasts and that while lxc with lxc-templates is a straightforward way to create containers that act a lot like regular old hardware LXD brings on all of its we love the mother fucking cloud baggage. Major differences had to do with user mapping on the containers files created by root on the host were mapped to nobody on the container, making it really difficult to set up home directories etc. (for a workaround to this see https://stackoverflow.com/questions/33377916/migrating-lxc-to-lxd) The second was the way that the network is initialized with the assumption that LXD would be providing the bridge and the context. 

## First Attempt and zfs/bridge setup

* create zfs container and bridge as before

```sh	
root@bs2020:~# lxd init
... create new zfs pool and use all of /dev/sdd1 do not configure bridge ...
root@bs2020:~# dpkg-reconfigure -p medium lxd
... no yes br1 ... use existing bridge...
root@bs2020:~# lxc launch ubuntu:16.04 franklin -p default -p docker
root@bs2020:~# lxc stop franklin
root@bs2020:~# passwd -l ubuntu -R /var/lib/lxd/containers/franklin.zfs/rootfs
passwd: user 'ubuntu' does not exist
root@bs2020:~# cd /var/lib/lxd/containers/franklin.zfs/rootfs/
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# cat ~feurig/passwd.add>>etc/passwd
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# cat ~feurig/shadow.add>>etc/shadow
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# tar -xzvf ~feurig/fnj.tgz
home/feurig
...
home/joe/.ssh/authorized_keys
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# usermod -R /var/lib/lxd/containers/franklin.zfs/rootfs -G sudo,root joe
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# usermod -R /var/lib/lxd/containers/franklin.zfs/rootfs -G sudo,root feurig
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# groupadd -R /var/lib/lxd/containers/franklin.zfs/rootfs -g 1001 feurig
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# groupadd -R /var/lib/lxd/containers/franklin.zfs/rootfs -g 1002 joe
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# cat <<eod >>/var/lib/lxd/containers/franklin.zfs/rootfs/etc/resolvconf/resolv.conf.d/base 
> dns-nameserver 198.202.31.132 198.202.31.141 8.8.8.8
> nameserver 198.202.31.132 198.202.31.141 8.8.8.8
> eod
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# sed -i 's/^iface eth0/#iface eth0/' /var/lib/lxd/containers/franklin.zfs/rootfs/etc/network/interfaces
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# cat <<eod2 >>/var/lib/lxd/containers/franklin.zfs/rootfs/etc/network/interfaces
> iface eth0 inet static
>     address 198.202.31.201/25
>     gateway 198.202.31.129
>     dns-nameservers 198.202.31.132 198.202.31.141 8.8.8.8
>     dns-search suspectdevices.com digithink.com
> eod2
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# lxc start franklin
```	
* try to log in to instance over the network..... FAIL
* unlike lxc's ubuntu:16.04, lxd's ubuntu:16.04 has all of the cloud cruft . That and all of the modifications to the containers directory was rootsquashed (rendering it useless).
```sh	
root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# lxc exec franklin bash
root@franklin:~# nano /etc/network/interfaces
root@franklin:~# cat /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# Source interfaces
# Please check /etc/network/interfaces.d before changing this file
# as interfaces may have been defined in /etc/network/interfaces.d
# See LP: #1262951
source /etc/network/interfaces.d/*.cfg
iface eth0 inet static
	address 198.202.31.201/25
	gateway 198.202.31.129
	dns-nameservers 198.202.31.132 198.202.31.141 8.8.8.8
	dns-search suspectdevices.com digithink.com
	
* _first thought_: remove all of the cloud crap...

root@franklin:~# apt-get remove cloud*
...
The following packages will be REMOVED:
	cloud-guest-utils cloud-init cloud-initramfs-copymods cloud-initramfs-dyn-netconf
0 upgraded, 0 newly installed, 4 to remove and 0 not upgraded.
After this operation, 1682 kB disk space will be freed.
Do you want to continue? [Y/n] Y
...
root@franklin:~# nano /etc/network/interfaces
... add auto eth0
root@franklin:~# reboot
root@franklin:~# root@bs2020:/var/lib/lxd/containers/franklin.zfs/rootfs# lxc list
+----------+---------+-----------------------+------+------------+-----------+
|   NAME   |  STATE  |         IPV4          | IPV6 |    TYPE    | SNAPSHOTS |
+----------+---------+-----------------------+------+------------+-----------+
| franklin | RUNNING | 198.202.31.201 (eth0) |      | PERSISTENT | 0         |
+----------+---------+-----------------------+------+------------+-----------+
```
* _second thought_: Fuck that! Make it work!
## Second attempt
   (create LXD profile for suspect devices development).
```sh
root@bs2020:~# lxc stop franklin 
root@bs2020:~# lxc delete franklin
root@bs2020:~# lxc profile create susdev
root@bs2020:~# lxc profile edit susdev
... 
```	
	
* repeat until you have a working system that can be logged into remotely
* create docker container container
```sh	
root@bs2020:~# lxc profile show susdev
config:
	user.network_mode: link-local
	user.user-data: |
	#cloud-config
	timezone: America/Vancouver
	users:
		- name: feurig
		passwd: "... SUBSTITUTE REAL PASSWORD HASH HERE ...."
		gecos: Donald Delmar Davis
		ssh-authorized-keys:
			- ssh-rss ... SUBSTITUTE REAL KEY HERE ... don@viscious
		groups: sudo,root
		shell: /bin/bash
		- name: joe
		passwd: "... SUBSTITUTE REALPASSWORD HASH HERE ...."
		gecos: Joseph Wayne Dumoulin
		ssh-authorized-keys:
			- ssh-rss ...SUBSTITUTE REAL KEY HERE... jdumoulin@joeslaptop
		groups: sudo,root
		shell: /bin/bash
	manage_resolv_conf: true
	resolv_conf:
		nameservers: ['198.202.31.141', '198.202.31.132', '8.8.8.8']
		searchdomains:
		- suspectdevices.com
		- digithink.com
		domain: suspectdevices.com
		options:
		rotate: true
		timeout: 1
	write_files:
	# Set static IP address could not get this to work the "right" way
	- path: /etc/network/interfaces
		permissions: '0644'
		owner: root:root
		content: |
		auto lo
		iface lo inet loopback
		auto eth0
		# change this after first instantiation
		iface eth0 inet static
			address 198.202.31.200
			broadcast 198.202.31.255
			netmask 255.255.255.128
			gateway 198.202.31.129
			dns-nameservers 198.202.31.141 198.202.31.132 8.8.8.8
	runcmd:
	# sudo needs to be able to resolve itself to authenticate users
	# and the users are locked by default
	- sed -i "s/^127.0.0.1/#127.0.0.1/" /etc/hosts
	- echo 127.0.0.1 `hostname` localhost >>/etc/hosts
	- passwd joe -u
	- passwd feurig -u
description: Try to create a sane environment for cloud-init based operating systems
devices:
	eth0:
	name: eth0
	nictype: bridged
	parent: br1
	type: nic
name: susdev
root@bs2020:~#

root@bs2020:~# lxc list
+--------+---------+-----------------------+------+------------+-----------+
|  NAME  |  STATE  |         IPV4          | IPV6 |    TYPE    | SNAPSHOTS |
+--------+---------+-----------------------+------+------------+-----------+
| test13 | RUNNING | 198.202.31.200 (eth0) |      | PERSISTENT | 0         |
+--------+---------+-----------------------+------+------------+-----------+
root@bs2020:~# lxc init ubuntults16 franklin -p susdev -p docker
Creating franklin
root@bs2020:~# lxc start franklin
root@bs2020:~# lxc exec franklin bash
root@franklin:~# tail -2 /etc/shadow
feurig:<<HASHED PASSWORD>>:17453:0:99999:7:::
joe:<<HASHED PASSWORD>>:17453:0:99999:7:::
root@franklin:~# nano /etc/network/interfaces
root@franklin:~# cat /etc/network/interfaces
auto lo
iface lo inet loopback
auto eth0
# change this after first instantiation
iface eth0 inet static
	address 198.202.31.201
	broadcast 198.202.31.255
	netmask 255.255.255.128
	gateway 198.202.31.129
	dns-nameservers 198.202.31.141 198.202.31.132 8.8.8.8
root@franklin:~# cat /etc/hosts
#127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
127.0.0.1 franklin localhost
root@franklin:~# reboot
root@bs2020:~# lxc list
+----------+---------+-----------------------+------+------------+-----------+
|   NAME   |  STATE  |         IPV4          | IPV6 |    TYPE    | SNAPSHOTS |
+----------+---------+-----------------------+------+------------+-----------+
| franklin | RUNNING | 198.202.31.201 (eth0) |      | PERSISTENT | 0         |
+----------+---------+-----------------------+------+------------+-----------+
| test13   | RUNNING | 198.202.31.200 (eth0) |      | PERSISTENT | 0         |
+----------+---------+-----------------------+------+------------+-----------+
root@bs2020:~# 
```	
	
## References
* http://www.whiteboardcoder.com/2016/04/cloud-init-nocloud-with-url-for-meta.html
* https://stgraber.org/2016/03/11/lxd-2-0-blog-post-series-012/
* https://github.com/lxc/lxd/blob/master/doc/cloud-init.md
* http://www.mattjarvis.org.uk/post/lxd-openstack-cloudinit-pt1/
* https://sdgsystems.com/blog/understanding-and-using-lxc-and-lxd
* http://cloudinit.readthedocs.io/en/latest/topics/examples.html
* http://cloudinit.readthedocs.io/en/latest/topics/debugging.html