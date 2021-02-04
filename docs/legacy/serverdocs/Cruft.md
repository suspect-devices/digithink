#Updating Hosts Notes 

### Updating hosts manually
The process for updating hosts is handled via apt-get in 3 steps. [#2 (2)]
1. update == check repos
2. dist-upgade == apply updates
3. autoremove == clean up

	
	root@bs2020:~# apt-get update&&apt-get dist-upgrade&& apt-get autoremove
	

### Updating debian hosts using Ansible (via lxd connection)
From kb2018 we can use the apt module to update out hosts and containers however this is apt specific
	
	ansible pets -m apt -a "force_apt_get=yes upgrade=yes update_cache=yes autoremove=yes"
	
 
### Updating containers using an os agnostic script
#### update.sh
The ansible module is nice but specific to the operating system. To extend this to other distributions we can use the following script. 
	
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
	          zypper dist-upgrade
	        fi
	        echo ======================#### done==========================
	    
Deploying the script using either basic shell commands or shell/awk is fairly straight forward. 
	
	root@kb2018:~# lxc list -c n --format csv|awk '{print "lxc file push /usr/local/bin/update.sh " $1 "/usr/local/bin/"}' |bash
	
Since the hosts are on a private lan they are configured to trust each other. This means that the above deployment can be pushed to the other server as well. 
	
	root@kb2018:~# lxc list bs2020: -c n --format csv|awk '{print "lxc file push /usr/local/bin/update.sh bs2020:" $1 "/usr/local/bin/"}' |bash
	
Running the script using is equally simple. 
	
	root@kb2018:~# for h in `lxc list bs2020: -c n --format csv ` ;do lxc exec bs2020:$h update.sh; done
	root@kb2018:~# for h in `lxc list local: -c n --format csv ` ;do lxc exec local:$h update.sh; done
	
Ansible improves on this simplicity using the file and raw modules.
	
	.... fill in file deployment example ....
	root@kb2018:/etc/ansible# ansible pets  -m copy -a 'src=/etc/ansible/files/update.sh dest=/usr/local/bin/ owner=root group=root mode=0774'
	root@kb2018:~# ansible pets -m raw -a "update.sh"
	
Currently only current ubuntu (18.04) is downloaded for creating hosts. Any other hosts will require manual configuration or use of a custom profile.
### for example (more info at TaskCreatingNewContainers) 
	
	root@bs2020:~# lxc image list kb2018:
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	|   ALIAS    | FINGERPRINT  | PUBLIC |                 DESCRIPTION                 |  ARCH  |   SIZE   |          UPLOAD DATE          |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	| ubuntu-lts | ae465acff89b | no     | ubuntu 18.04 LTS amd64 (release) (20180613) | x86_64 | 173.14MB | Jun 16, 2018 at 10:07pm (UTC) |
	+------------+--------------+--------+---------------------------------------------+--------+----------+-------------------------------+
	root@bs2020:~# lxc init kb2020:ubuntu-lts test18 -p susdev19 
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
	
## linkdump
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
.... review / decruft ..
[=#fn1 1] ) The original purpose of this server was to evaluate openstack.

Openstack requires relinquishing complete control of the host server to an overtly complicated pile of layers which once installed cannot be uninstalled without completely re-inststalling the entire operating system. This is not that unusual (my first installation of puppet was equally badly behaved and destructive ) but it does not instill confidence in software with cart blanch access to everything.

See: [wiki:GoodByeOpenstack]

Our search for a way to deploy such an insecure POS led us to look deeply into the lightweight container system provided by lxc. We attempted to create an isolated server for openstack/devstack that can be uninstalled and which will not shit all over everything. (Attempting to containerize devstack was as disastrous as trying to uninstall it)
 
In the process we discovered a wy to create a public facing server for dns/email/and other services which is isolated from other containers and can not access the host directly.

By extending this new set of tools we are also able to to create user space containers for experimentation which are in themselves isolated from everything else.

[=#fn2 2] ) Ubuntu can be  configured to auto update however in my experience this leads to a false sense of security and a lack of awareness of what is broken/changing. Also, when autoupdates fail they do not recover gracefully, will not apply the next set of updates, and it's a major pain in the ass to fix them. For this reason I tend to use apticron to notify us when updates are available and manually update them. 

For BS2020 and naomi, I also tend to look at what is being done instead of adding the -y parameter to apt-get.

[=#fn3 3] ) There are some side effects to this method for instance moving to a new server can apply the other servers default profile to it. I have also noticed that moving from a snapshot to a new container starts the new container.  