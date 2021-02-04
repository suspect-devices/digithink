This does not work. As far as I can tell you can only install devstack on raw hardware and let it install all of its ever moving dependencies. I was able to do this where pike was 6 months ago but not uninstall and reinstall is using the same version. 

I don't believe it can trust anything this moving to be sane let alone secure.

FUCK THIS.

### Best attempt at lxc in a container

Now we want to see about the devstack container. It should have its own network interface (eno3) and disk /dev/sdf.
* use lxd init to create zfs filesystem for devstack
  At some point we should figure out how to configure both zfs and the appropriate bridge configuration without these two steps.
	
	root@bs2020:~# lxd init
	...
	root@bs2020:~# zfs list
	NAME                          USED  AVAIL  REFER  MOUNTPOINT
	lxd4devstack                  243M   132G    19K  none
	lxd4infra                     200M   132G    19K  none
	lxd4infra/naomi               200M   132G   200M  /var/lib/lxc/naomi/rootfs
	root@bs2020:~# 
	
	https://docs.openstack.org/devstack/latest/guides/lxc.html
	

* setup br1 use dpkg-reconfigure to point the network at br1 

```	
	root@bs2020:~# nano /etc/network/interfaces
	... add the following ...
	auto br1
	iface br1 inet static
	    address 0.0.0.0
	    dns-nameservers 198.202.31.132 198.202.31.141 8.8.8.8
	    bridge_ports eno3
	
	iface eno3 inet manual
	root@bs2020:~# ifdown br1 && ifup br1
	root@bs2020:~# ip a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
	...
	12: br1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
	    link/ether d4:be:d9:ec:ee:d2 brd ff:ff:ff:ff:ff:ff
	    inet6 fe80::d6be:d9ff:feec:eed2/64 scope link 
	       valid_lft forever preferred_lft forever
```	
* set up lxc config file 

```	
	root@bs2020:~# nano /etc/lxc/devstack.conf 
	# from https://docs.openstack.org/devstack/latest/guides/lxc.html
	# Permit access to /dev/loop*
	lxc.cgroup.devices.allow = b 7:* rwm
	
	# Setup access to /dev/net/tun and /dev/kvm
	lxc.mount.entry = /dev/net/tun dev/net/tun none bind,create=file 0 0
	lxc.mount.entry = /dev/kvm dev/kvm none bind,create=file 0 0
	
	# Networking
	lxc.network.type = veth
	lxc.network.flags = up
	lxc.network.link = br1
	lxc.network.hwaddr = 00:16:3d:xx:xx:xx
	
	lxc.network.ipv4 = 198.202.31.160/25
	lxc.network.ipv4.gateway = 198.202.31.129
	
	lxc.start.auto = 1
	lxc.start.delay = 7
	lxc.start.order = 150
```
	
* create the image

```	
	root@bs2020:~# lxc-create -n theswedishchef  -t ubuntu -f /etc/lxc/devstack.conf -B zfs \        
	                                  --zfsroot=lxd4devstack \
	                              -- --packages=bsdmainutils,git,nano,ebtables,openvswitch-common
```	
* add local admin users, setup network and  lockdown ubuntu user.

```	
	root@bs2020:~# passwd -l ubuntu -R /var/lib/lxc/theswedishchef/rootfs
	passwd: password expiry information changed.
	root@bs2020:~# cd /var/lib/lxc/theswedishchef/rootfs/
	root@bs2020:~# cat ~feurig/passed.add>>etc/passwd
	root@bs2020:~# cat ~feurig/shadow.add>>etc/shadow
	root@bs2020:~# tar -xzvf ~feurig fnj.tgz
	drwxr-xr-x root/root         0 2017-09-27 17:58 home/
	... home directories for admins mostly for the following file ...
	-rw-rw-r-- joe/joe         402 2017-09-25 23:51 home/joe/.ssh/authorized_keys
	root@bs2020:~# cd 
	root@bs2020:~# usermod -R /var/lib/lxc/theswedishchef/rootfs -G sudo,root joe
	root@bs2020:~# usermod -R /var/lib/lxc/theswedishchef/rootfs -G sudo,root feurig
	root@bs2020:~# groupadd -R /var/lib/lxc/theswedishchef/rootfs -g 1001 feurig
	root@bs2020:~# groupadd -R /var/lib/lxc/theswedishchef/rootfs -g 1002 feurig
	root@bs2020:~# groupadd -R /var/lib/lxc/theswedishchef/rootfs -g 1002 joe
	root@bs2020:~#  cat <<eod >>/var/lib/lxc/theswedishchef/rootfs/etc/resolvconf/resolv.conf.d/base 
	dns-nameserver 198.202.31.132 8.8.8.8
	nameserver 198.202.31.132 8.8.8.8
	eod
	root@bs2020:~#  cat <<eod2 >>/var/lib/lxc/theswedishchef/rootfs/etc/network/interfaces
	iface eth0 inet static
	    address 198.202.31.160/25
	    gateway 198.202.31.129
	    dns-nameservers 198.202.31.132 198.202.31.141 8.8.8.8
	    dns-search suspectdevices.com digithink.com
	eod2
```	  
* check for ebtables module

```	
	root@bs2020:~# lsmod |grep ebt
	ebtable_broute         16384  0
	ebtable_nat            16384  0
	ebtable_filter         16384  0
	ebtables               36864  3 ebtable_broute,ebtable_nat,ebtable_filter
	x_tables               36864  9 xt_CHECKSUM,ip_tables,xt_tcpudp,ipt_MASQUERADE,xt_conntrack,iptable_filter,ebtables,ipt_REJECT,iptable_mangle
	bridge                126976  1 ebtable_broute
```
	 
* run up instance and install devstack

```	
	root@bs2020:~# lxc-start -n theswedishchef
	root@bs2020:~# lxc-attach -n theswedishchef
	root@theswedishchef:~# apt-get install --reinstall ca-certificates
	root@theswedishchef:/# useradd -s /bin/bash -d /opt/stack -m stack
	root@theswedishchef:/#  echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
	stack ALL=(ALL) NOPASSWD: ALL
	root@theswedishchef:/# su - stack
	stack@theswedishchef:~$ git clone https://git.openstack.org/openstack-dev/devstack
	Cloning into 'devstack'...
	... done.
	stack@theswedishchef:~$  cd devstack/
	stack@theswedishchef:~/devstack$ nano local.conf
	[[local|localrc]]
	ADMIN_PASSWORD=B0rkB0rkB0rk
	DATABASE_PASSWORD=$ADMIN_PASSWORD
	RABBIT_PASSWORD=$ADMIN_PASSWORD
	SERVICE_PASSWORD=$ADMIN_PASSWORD
	PUBLIC_INTERFACE=eth0
	HOST_IP=127.0.0.1
	FLOATING_RANGE=198.202.31.160/28
	PUBLIC_NETWORK_GATEWAY=198.202.31.129
	Q_FLOATING_ALLOCATION_POOL=start=198.202.31.161,end=192.202.31.173
	#IPV4_ADDRS_SAFE_TO_USE=172.31.1.0/24
	 stack@theswedishchef:~/devstack$ ./stack.sh
	... don't even look at it just walk away ....
	
```	

## Approaches Attempted

* https://stgraber.org/2016/10/26/lxd-2-0-lxd-and-openstack-1112/
  (lxd fights with yet another fucking automated deployment system (snapd) this is lxd not lxc....
  Bottom line snapd and therefore juju wont run in a container on LTS until at least 18.04 
* All three "stable" releases. Most of them had issues with different kernel dependencies.
### wasted time
* http://blog.decbug.com/openstack_in_lxc/
* https://bayton.org/docs/linux/lxd/lxd-zfs-and-bridged-networking-on-ubuntu-16-04-lts/
* https://www.simpleprecision.com/ubuntu-16-04-lxd-networking-simple-bridge
* http://networkstatic.net/installing-openstack-ml2-neutron-plugin-devstack-fedora/
* https://blog.scottlowe.org/2012/08/17/installing-kvm-and-open-vswitch-on-ubuntu/
* https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#prerequisites
* https://fedoraproject.org/wiki/OpenStack_devstack
* https://docs.openstack.org/devstack/latest/guides/single-machine.html
* https://serenity-networks.com/how-to-install-openstack-ocata-on-a-single-server-using-devstack/
* https://linuxcontainers.org/lxd/getting-started-openstack/
* https://jujucharms.com/u/openstack-charmers-next/openstack-lxd/
* https://stgraber.org/2016/10/26/lxd-2-0-lxd-and-openstack-1112/
* https://insights.ubuntu.com/2016/08/15/lunch-learn-with-openstack-containers/
* https://help.nextcloud.com/t/install-fails-on-snap-core-2466-mount-unknown-filesystem-squashfs/19251
* https://yourcodeway.com/how-to-install-nextcloud-on-ubuntu-16-04
* https://askubuntu.com/questions/925391/unknown-filesystem-squashfs-when-trying-to-mount-snap-packages
* https://bugs.launchpad.net/snappy/+bug/1628289
  dbclinton (dbclin) wrote on 2017-07-26:	#36
  Just to update my previous comment: poking around Stéphane Graber's blog a bit suggests to me that I really shouldn't expect success with this using less than 16.10.
* https://askubuntu.com/questions/869792/unit-snap-core-716-mount-has-failed-on-ubuntu-16-04-lts-rootfs-armhf
* 

  