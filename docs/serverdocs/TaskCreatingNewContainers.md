<!-- TaskCreatingNewContainers, Version: 17, Modified: 2020/05/16, Author: feurig -->
## Creating containers

LXD allows us to create lightweight virtual machines, and combined with filesystems such as ZFS, provides several mechanisms to easily configure, backup, replicate and update them. Adding ansible to the mix makes this process even more simple. 

To create a container in our current environment simply add the hostname, ip_address, and purpose to /etc/ansible/hosts and run the create-lxd-containers.yml

	
	root@kb2018:/etc/ansible# nano hosts
	...
	redshirt ip_address=198.202.31.200 purpose="Disposable Ubuntu"
	...
	root@kb2018:/etc/ansible# ansible-playbook /etc/ansible/playbooks/create-lxd-containers.yml
	 

The containers created have admin accounts and ssh keys installed. They have Isolated static ip addresses which can not reach the server directly. Getting onto the containers requires an ssh key and a password to escalate privileges. By default the containers are unprivileged which should minimize the security risks to the main server. They also have an os agnostic script to perform periodic updates.

### Mechanisms
LXD provides images and profiles which define the disk storage, network and other configuration used to create the container. The profiles include cloud config however only the ubuntu image implements it. Most things work well except some don't or some things change and the updates or the updated images require some tweaking _(resolved for instance because it wasn't broken and you had to work around what was already)_

## Container !Image/Profile notes

The fragments below are from my work to create other images that would work as well.  
### Ubuntu LTS (20.04)
My initial forays into the new  LTS release are [StartUsingTheFwords here]. 

### Previous Ubuntu LTS (18.04)

Ubuntu 18.04 is really well suited for LXD in that it comes stock with cloud init. This means that with a simple profile you can create a usable container pre seeded with admin accounts, static networking and an update script. 

### Creating a new ubuntu container using lxd

In our environment hosts do not tend to be temporary so they are not dynamically allocated. Containers are built at the static ip address at redshirt.suspectdevices.com and then reconfigured before being used.

	
	root@bs2020:~# lxc image list kb2018:
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	|   ALIAS    | FINGERPRINT  | PUBLIC |                 DESCRIPTION                 |  ARCH  |   SIZE   |          UPLOAD DATE          |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	| ubuntu-lts | ae465acff89b | no     | ubuntu 18.04 LTS amd64 (release) (20180613) | x86_64 | 173.14MB | Jun 16, 2018 at 10:07pm (UTC) |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	root@bs2020:~# lxc init kb2018:ubuntu-lts test18 -p susdev19 -p default
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
	root@test18:~# netplan apply
	root@test18:~# update.sh
	root@test18:~# reboot
	root@test18:~# root@bs2020:~# lxc list
	+----------+---------+--------------------------------+------+------------+-----------+
	|   NAME   |  STATE  |              IPV4              | IPV6 |    TYPE    | SNAPSHOTS |
	+----------+---------+--------------------------------+------+------------+-----------+
	....
	+----------+---------+--------------------------------+------+------------+-----------+
	| test18   | RUNNING | 198.202.31.216 (eth0)          |      | PERSISTENT | 0         |
	+----------+---------+--------------------------------+------+------------+-----------+
	root@bs2020:~# 
	
### lxd profile for suspectdevices
The profile for suspect devices is broken into three major parts. 
* Network configuration
* System, User and Security Configuration 
* Disk Pools and Network Devices
#### Overriding the profiles network configuration
.... do this by hand and discuss the ansible update in progress....
	
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
	        address: 198.202.31.141
	
### System, User and Security Configuration
(Network Configuration is Stubbed in)
 
	
	root@kb2018:~# lxc profile show susdev19
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
	        address: 198.202.31.141
	  user.user-data: |
	    #cloud-config
	    timezone: America/Vancouver
	    users:
	      - name: feurig
	        passwd: "$6$2Pf0ittl$nl....VdI/FyCXtu."
	        gecos: Donald Delmar Davis
	        ssh-authorized-keys:
	          - ssh-rsa AAAA....uj4SL don@annie
	          - ssh-rsa AAA..... FMNNn don@haifisch.local
	        groups: sudo,root,wheel
	        shell: /bin/bash
	      - name: joe
	        passwd: "$6$o14Dp3u...pD3vLrS1vX."
	        gecos: Joseph Wayne Dumoulin
	        ssh-authorized-keys:
	          - ssh-rsa AAAA...r6Y/ZePpr jdumoulin@nextit.com
	        groups: sudo,root,wheel
	        shell: /bin/bash
	    manage_resolv_conf: false
	    packages:
	    - python
	    package_update: true
	    package_upgrade: true
	    write_files:
	    - path: /etc/systemd/resolved.conf
	      permissions: '0644'
	      owner: root:root
	      content: |
	        # resolved because that wasnt broken either
	        [Resolve]
	        DNS= 198.202.31.141 198.202.31.132 8.8.4.4
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
	          apt-get -y autoremove
	        fi
	        if  [ -x "$(command -v yum)" ]; then
	          echo yum upgrade.
	          yum -y upgrade
	        fi
	        if  [ -x "$(command -v zypper)" ]; then
	          echo zypper dist-upgrade.
	          zypper -y dist-upgrade
	        fi
	        echo ======================#### done==========================
	    runcmd:
	    # fix stupid subtle things
	    # sudo needs to be able to resolve itself to authenticate users
	    # and the users are locked by default
	    # cloud cart blanch accounts are inexcusable
	    - sed -i "s/^127.0.0.1/#127.0.0.1/" /etc/hosts
	    - echo 127.0.0.1 `hostname` localhost >>/etc/hosts
	    - passwd joe -u
	    - passwd feurig -u
	    - userdel -f ubuntu
	    - userdel -f centos
	    - userdel -f opensuse
	    #- netplan apply
	    power_state:
	       mode: reboot
	       message: See You Soon...
	       condition: True
	description: Try to create a sane environment for cloud-init based operating systems
	devices: {}
	name: susdev19
	used_by:
	
## cloud - init and ubuntu but no where else.
When I ran up the lxc containers for operating systems that aren't ubuntu the magic profile doesn't work. And in fact cloud-init and the utilities that are native on Ubuntu are not installed on those images. (WTF??) So my first attempt (using the Debian 9 container was to add cloud-init cloud-utils and the other packages and then get export and reimport the container) which more or less failed miserably (because creating new containers from scratch isn't as simple as they say it is. :).

### debian 9 (Works!)
It turns out I didn't need to export or import the image. I just needed to copy the lxc templates from a working ubuntu image and then modify metadata.yaml on the image while its running and publish the result. (this method is buried in the discussion [| here](https://discuss.linuxcontainers.org/t/launching-lxd-images-using-templates/1099/16))
	
	... lxc create using images:debian/9 ....
	... lxc start image and add cloud init and cloud utils ...
	... copy templates and metadata data from working ubuntu ....
	... link /etc/network/interfaces.d/50... -> /etc/network/interfaces ...
	... delete /var/log/cloud cruft ...
	... shutdown and lxc publish ....
	root@bs2020:~# lxc publish kernigan --alias debian/9c
	root@bs2020:~# lxc init debian/9c redshirt -p susdev19
	

This works well. More better documentation to follow.

### Centos 7 (works)
	
	[root@keynes ~]# cd /etc/sysconfig/
	[root@keynes sysconfig]# cat network
	NETWORKING=yes
	HOSTNAME=LXC_NAME
	[root@keynes sysconfig]# cd network-scripts/
	[root@keynes network-scripts]# vi ifcfg-eth0 
	DEVICE=eth0
	BOOTPROTO=none
	ONBOOT=yes
	HOSTNAME=LXC_NAME
	NM_CONTROLLED=no
	TYPE=Ethernet
	PREFIX=25
	IPADDR=198.202.31.220
	MTU=
	GATEWAY=198.202.31.129
	[root@keynes network-scripts]# systemctl restart network
	[root@keynes network-scripts]# nano /etc/resolv.conf 
	bash: nano: command not found
	[root@keynes network-scripts]# vi /etc/resolv.conf 
	...
	nameserver 198.202.31.141
	search suspectdevices.com
	...
	[root@keynes network-scripts]# ping digithink.com
	PING digithink.com (198.202.31.230) 56(84) bytes of data.
	64 bytes from 198.202.31.230 (198.202.31.230): icmp_seq=1 ttl=64 time=0.441 ms
	...
	[root@keynes network-scripts]# cd
	[root@keynes ~]# yum update
	Failed to set locale, defaulting to C
	Loaded plugins: fastestmirror
	...
	updates                                                                                                                                                       | 3.4 kB  00:00:00     
	(1/4): extras/7/x86_64/primary_db                                                                                                                             | 156 kB  00:00:00     
	(2/4): updates/7/x86_64/primary_db                                                                                                                            | 1.3 MB  00:00:00     
	(3/4): base/7/x86_64/group_gz                                                                                                                                 | 166 kB  00:00:00     
	(4/4): base/7/x86_64/primary_db                                                                                                                               | 6.0 MB  00:00:01     
	No packages marked for update
	[root@keynes ~]# yum install -y nano less
	[root@keynes ~]# yum install -y cloud-init
	[root@keynes ~]# yum install -y cloud-utils
	[root@keynes ~]# yum install -y openssh-server
	[root@keynes ~]# yum install -y sudo
	[root@keynes ~]# cat >>/etc/sudoers.d/9_fix-centos-sudo  <<EOD
	%sudo ALL=(ALL) ALL
	centos  ALL = /usr/bin/su nobody
	EOD
	[root@keynes ~]# exit
	... modify metadata.yaml ...
	... copy templates ....
	root@bs2020:~# lxc image delete centos/7c
	root@bs2020:~# lxc publish keynes --alias centos/7c
	Container published with fingerprint: a27609a23021f4577dfea987176fa942635d349b2e3be0e046118db88af4c56a
	root@bs2020:~# 
	root@bs2020:~# lxc launch centos/7c redshirt -p susdev19
	Creating redshirt
	Starting redshirt
	
	
	
Check the work....
	
	haifisch:~ don$ ssh feurig@redshirt.suspectdevices.com
	The authenticity of host 'redshirt.suspectdevices.com (198.202.31.200)' can't be established.
	ECDSA key fingerprint is SHA256:ad0/DY7qDl9XKSl4lnjSq9jv63e18Nrr4IZjT0yu7Og.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added 'redshirt.suspectdevices.com,198.202.31.200' (ECDSA) to the list of known hosts.
	[feurig@redshirt ~]$ sudo bash
	
	We trust you have received the usual lecture from the local System
	Administrator. It usually boils down to these three things:
	
	    #1) Respect the privacy of others.
	    #2) Think before you type.
	    #3) With great power comes great responsibility.
	
	[sudo] password for feurig: 
	[root@redshirt feurig]# 
	
todo: look deeper into right way to sudo and cloud config. (ubuntu:ubuntu problem)

### Fedora 29 (not picking up local cloud-init)
	
	[root@kundara ~]# cat .bash_history 
	ip address add 198.202.31.200/25 dev eth0
	ip route add default via 198.202.31.129
	ping digithink.com
	dnf upgrade
	dnf upgrade cloud-init
	dnf install cloud-init
	dnf install -y cloud-utils
	dnf install -y nano less sudo
	dnf install -y openssh-server
	cat >>/etc/sudoers.d/9_fix-fedora-sudo  <<EOD
	%sudo ALL=(ALL) ALL
	fedora  ALL = /usr/bin/su nobody
	EOD
	dnf install -y network-scripts
	echo "NOZEROCONF=yes" >> /etc/sysconfig/network
	systemctl enable cloud-init
	chkconfig --levels 2345 sshd on
	chkconfig --levels 2345 network on
	journalctl --vacuum-time=`date +%s`
	shutdown -h now
	

### OpenSuse 15.0 (Close -- some oddities)
Image comes up with no network.
	
	ip address add 198.202.31.200/25 dev eth0
	ip route add default via 198.202.31.129
	cat >/etc/resolv.conf<<EOD
	nameserver 198.202.31.141
	nameserver 198.202.31.132
	nameserver 8.8.8.8
	search suspectdevices.com
	EOD
	
Install the packages needed to work here.
	
	zypper -y install nano sudo cloud-init
	zypper -y install openssh
	zypper -y dist-upgrade
	
	systemctl enable cloud-init
	
sshd install masks the service as disabled.
	
	systemctl unmask sshd
	systemctl enable sshd
	
Sudo comes out of the box pretty insecurely configured.
	
	cat> /etc/sudoers.d/9_fix_opensuse_sudo<<EOD
	Defaults !targetpw
	%sudo ALL=(ALL) ALL
	opensuse  ALL = /usr/bin/su nobody
	EOD
	

todo: (cloud init bugs)
* figure out why hashed passwords don't work. (or is it just my long complicated password).
* figure out why the default route isn't getting propagated.

### updating running containers
The update script created by the profile can be easily executed on all running containers on both hosts with the following 2 lines of bash. 
	
	root@kb2018:~# for h in `lxc list bs2020: -c n --format csv ` ;do echo $h ;lxc exec bs2020:$h update.sh; done
	root@kb2018:~# for h in `lxc list local: -c n --format csv ` ;do echo $h ;lxc exec local:$h update.sh; done
	