# HOLY FUCKING AWESOME!!!!
Watch while I add a fresh disk as a mirror, resliver the pool and remove and repartition the original disk while the container using the pool is still running!!!
... make this into a structured document ...

	
```sh 
root@bs2020:~# zpool status
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
	scan: scrub repaired 0 in 0h2m with 0 errors on Sun Aug 12 00:27:02 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		sda1      ONLINE       0     0     0

errors: No known data errors
root@bs2020:~# zpool add -n lxd4infra mirror sdb
invalid vdev specification: mirror requires at least 2 devices
root@bs2020:~# zpool add -n lxd4infra mirror sda1 sdb
invalid vdev specification
use '-f' to override the following errors:
/dev/sda1 is part of active pool 'lxd4infra'
/dev/sdb does not contain an EFI label but it may contain partition
information in the MBR.
root@bs2020:~# mklabel GPT /dev/sdb
bash: mklabel: command not found
root@bs2020:~# parted /dev/sdb
bash: parted: command not found
root@bs2020:~# gparted /dev/sdb
bash: gparted: command not found
root@bs2020:~# zpool add -nf lxd4infra mirror sda1 sdb
invalid vdev specification
the following errors must be manually repaired:
/dev/sda1 is part of active pool 'lxd4infra'
root@bs2020:~# zpool add -nf lxd4infra mirror sdb sda1
invalid vdev specification
the following errors must be manually repaired:
/dev/sda1 is part of active pool 'lxd4infra'
root@bs2020:~# zpool add -nf lxd4infra mirror sdb
invalid vdev specification: mirror requires at least 2 devices
root@bs2020:~# zpool add -nf lxd4infra sda1 mirror sdb
invalid vdev specification: mirror requires at least 2 devices
root@bs2020:~# zpool attach  -n  sda1 sdb
invalid option 'n'
usage:
	attach [-f] [-o property=value] <pool> <device> <new-device>
root@bs2020:~# zpool attach   sda1 sdb
missing <new_device> specification
usage:
	attach [-f] [-o property=value] <pool> <device> <new-device>
root@bs2020:~# zpool attach lxd4infra   sda1 sdb
invalid vdev specification
use '-f' to override the following errors:
/dev/sdb does not contain an EFI label but it may contain partition
information in the MBR.
root@bs2020:~# gparted
bash: gparted: command not found
root@bs2020:~# parted
bash: parted: command not found
root@bs2020:~# apt-get install parted
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following additional packages will be installed:
	libparted2
Suggested packages:
	libparted-dev libparted-i18n parted-doc
The following NEW packages will be installed:
	libparted2 parted
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Need to get 158 kB of archives.
After this operation, 520 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
Get:1 http://us.archive.ubuntu.com/ubuntu xenial-updates/main amd64 libparted2 amd64 3.2-15ubuntu0.1 [115 kB]
Get:2 http://us.archive.ubuntu.com/ubuntu xenial-updates/main amd64 parted amd64 3.2-15ubuntu0.1 [42.4 kB]
Fetched 158 kB in 0s (277 kB/s)  
Selecting previously unselected package libparted2:amd64.
(Reading database ... 32152 files and directories currently installed.)
Preparing to unpack .../libparted2_3.2-15ubuntu0.1_amd64.deb ...
Unpacking libparted2:amd64 (3.2-15ubuntu0.1) ...
Selecting previously unselected package parted.
Preparing to unpack .../parted_3.2-15ubuntu0.1_amd64.deb ...
Unpacking parted (3.2-15ubuntu0.1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up libparted2:amd64 (3.2-15ubuntu0.1) ...
Setting up parted (3.2-15ubuntu0.1) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
root@bs2020:~# parted /dev/sdb
GNU Parted 3.2
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) mklabel GPT                                                      
(parted) w
	align-check TYPE N                        check partition N for TYPE(min|opt) alignment
	help [COMMAND]                           print general help, or help on COMMAND
	mklabel,mktable LABEL-TYPE               create a new disklabel (partition table)
	mkpart PART-TYPE [FS-TYPE] START END     make a partition
	name NUMBER NAME                         name partition NUMBER as NAME
	print [devices|free|list,all|NUMBER]     display the partition table, available devices, free space, all found partitions, or a particular
		partition
	quit                                     exit program
	rescue START END                         rescue a lost partition near START and END
	resizepart NUMBER END                    resize partition NUMBER
	rm NUMBER                                delete partition NUMBER
	select DEVICE                            choose the device to edit
	disk_set FLAG STATE                      change the FLAG on selected device
	disk_toggle [FLAG]                       toggle the state of FLAG on selected device
	set NUMBER FLAG STATE                    change the FLAG on partition NUMBER
	toggle [NUMBER [FLAG]]                   toggle the state of FLAG on partition NUMBER
	unit UNIT                                set the default unit to UNIT
	version                                  display the version number and copyright information of GNU Parted
(parted) q                                                                
Information: You may need to update /etc/fstab.

root@bs2020:~# zpool attach lxd4infra   sda1 sdb
root@bs2020:~# zpool status
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
status: One or more devices is currently being resilvered.  The pool will
	continue to function, possibly in a degraded state.
action: Wait for the resilver to complete.
	scan: resilver in progress since Tue Sep  4 09:05:14 2018
	182M scanned out of 5.38G at 10.7M/s, 0h8m to go
	181M resilvered, 3.30% done
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		mirror-0  ONLINE       0     0     0
		sda1    ONLINE       0     0     0
		sdb     ONLINE       0     0     0  (resilvering)

errors: No known data errors
root@bs2020:~# packet_write_wait: Connection to 198.202.31.242: Broken pipe
steve:~ don$ ssh feurig@bs2020.suspectdevices.com
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-96-generic x86_64)

	* Documentation:  https://help.ubuntu.com
	* Management:     https://landscape.canonical.com
	* Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

New release '18.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Tue Sep  4 08:26:28 2018 from 75.164.203.77
feurig@bs2020:~$ sudo bash
[sudo] password for feurig: 
root@bs2020:~# packet_write_wait: Connection to 198.202.31.242: Broken pipe
steve:~ don$ ssh feurig@bs2020.suspectdevices.com
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-96-generic x86_64)

	* Documentation:  https://help.ubuntu.com
	* Management:     https://landscape.canonical.com
	* Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

New release '18.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Wed Sep  5 16:10:53 2018 from 75.164.203.77
feurig@bs2020:~$ sudo bash
[sudo] password for feurig: 
root@bs2020:~# packet_write_wait: Connection to 198.202.31.242: Broken pipe
steve:~ don$ 
steve:~ don$ ssh feurig@bs2020.suspectdevices.com
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-96-generic x86_64)

	* Documentation:  https://help.ubuntu.com
	* Management:     https://landscape.canonical.com
	* Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

New release '18.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Wed Sep  5 18:56:14 2018 from 75.164.203.77
feurig@bs2020:~$ sudo bash
[sudo] password for feurig: 
root@bs2020:~# zpool status
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
	scan: resilvered 5.38G in 0h6m with 0 errors on Tue Sep  4 09:11:31 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		mirror-0  ONLINE       0     0     0
		sda1    ONLINE       0     0     0
		sdb     ONLINE       0     0     0

errors: No known data errors
root@bs2020:~# zpool detach -n lxd4infra sda1 
invalid option 'n'
usage:
	detach <pool> <device>
root@bs2020:~# zpool detach  lxd4infra sda1 
root@bs2020:~# zpool status
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
	scan: resilvered 5.38G in 0h6m with 0 errors on Tue Sep  4 09:11:31 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		sdb       ONLINE       0     0     0

errors: No known data errors
root@bs2020:~# gparted /dev/sda
bash: gparted: command not found
root@bs2020:~# parted /dev/sda
GNU Parted 3.2
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) mklabel GPT                                                      
Warning: The existing disk label on /dev/sda will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? y                                                                 
(parted) q                                                                
Information: You may need to update /etc/fstab.

root@bs2020:~# zpool status                                            
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
	scan: resilvered 5.38G in 0h6m with 0 errors on Tue Sep  4 09:11:31 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		sdb       ONLINE       0     0     0

errors: No known data errors
root@bs2020:~# zpool attach lxd4infra   sdb sda
root@bs2020:~# zpool status
	pool: lxd4dev
	state: ONLINE
	scan: scrub repaired 0 in 0h8m with 0 errors on Sun Aug 12 00:32:48 2018
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4dev     ONLINE       0     0     0
		sdd1      ONLINE       0     0     0
		sdf       ONLINE       0     0     0
		sde       ONLINE       0     0     0

errors: No known data errors

	pool: lxd4infra
	state: ONLINE
status: One or more devices is currently being resilvered.  The pool will
	continue to function, possibly in a degraded state.
action: Wait for the resilver to complete.
	scan: resilver in progress since Thu Sep  6 09:24:09 2018
	69.8M scanned out of 5.42G at 5.37M/s, 0h17m to go
	67.9M resilvered, 1.26% done
config:

	NAME        STATE     READ WRITE CKSUM
	lxd4infra   ONLINE       0     0     0
		mirror-0  ONLINE       0     0     0
		sdb     ONLINE       0     0     0
		sda     ONLINE       0     0     0  (resilvering)

errors: No known data errors
root@bs2020:~# 
```