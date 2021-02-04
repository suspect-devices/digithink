#BS2020 LXC to LXD Notes 
When I set up BS2020 a year ago I was new to LXC and LXD (both of which are used at present because I wanted separate disk pools and network for infrastructure and development(/deployment). I believe that once we move from 16.04 to 18.04 we should be able to remove LXC from the equation. Regardless the initial pools were set up using lxd init as described in [wiki:BS2020InstallNotes the install notes for BS2020]. 
	
	root@bs2020:~# lxd init
	Name of the storage backend to use (dir or zfs) [default=zfs]: 
	Create a new ZFS pool (yes/no) [default=yes]? yes
	Name of the new ZFS pool [default=lxd]: lxd4infra
	Would you like to use an existing block device (yes/no) [default=no]? yes
	Path to the existing block device: /dev/sde1
	Would you like LXD to be available over the network (yes/no) [default=no]? 
	Do you want to configure the LXD bridge (yes/no) [default=yes]? no
	
	
	root@bs2020:~# lxd init
	... create new zfs pool and use all of /dev/sdd1 do not configure bridge ...
	root@bs2020:~# dpkg-reconfigure -p medium lxd
	... no yes br1 ... use existing bridge...
	root@bs2020:~#
	
When we moved disks from the original server to the new one the OS renumerated the disks so that the boot disk is at /dev/sdc1 (bay 2?) and our archive disk is in the last bay (bay 5). The remaining disks make up two zfs pools. In hindsight I would have preferred to initialize the original disks as entire disks as apposed to the first slice.

	
	root@bs2020:~# df -k
	...
	/dev/sdc1                                                                        41921808 2140004  37629256   6% /
	...
	/dev/sdf1                                                                       480589544 1524692 454629192   1% /archive
	...
	root@bs2020:~# 
	
	root@bs2020:~# zpool status
	  pool: lxd4dev
	 state: ONLINE
	  scan: scrub repaired 0 in 0h6m with 0 errors on Sun May 13 00:30:55 2018
	config:
	
		NAME        STATE     READ WRITE CKSUM
		lxd4dev     ONLINE       0     0     0
		  sdd1      ONLINE       0     0     0
		  sdb       ONLINE       0     0     0
		  sde       ONLINE       0     0     0
	
	errors: No known data errors
	
	  pool: lxd4infra
	 state: ONLINE
	  scan: scrub repaired 0 in 0h2m with 0 errors on Sun May 13 00:26:10 2018
	config:
	
		NAME        STATE     READ WRITE CKSUM
		lxd4infra   ONLINE       0     0     0
		  sda1      ONLINE       0     0     0
	
	errors: No known data errors
	
Disks sdb and sde were added to the dev/deployment pool as follows.
	
	zpool  add -f lxd4dev /dev/sde
	zpool  add -f lxd4dev /dev/sdb
	
As the disks were previously used they should have been wiped first.
	
	wipefs -a /dev/sdf
	
## New Disks New Errors
Since adding the two new disks I keep getting io errors on one of them. They do not seem to be causing any data errors however.
	
	ZFS has detected an io error:
	
	   eid: 106
	 class: io
	  host: bs2020
	  time: 2018-05-31 13:45:36-0700
	 vtype: disk
	 vpath: /dev/sdb1
	 vguid: 0x04009EB732FC8852
	 cksum: 0
	  read: 0
	 write: 0
	  pool: lxd4dev
	
## Backing up containers using zfs

### Link dump
* http://trac.suspectdevices.com/trac/wiki/FunWithLinuxDisks
* https://www.thegeekdiary.com/zfs-tutorials-creating-zfs-snapshot-and-clones/