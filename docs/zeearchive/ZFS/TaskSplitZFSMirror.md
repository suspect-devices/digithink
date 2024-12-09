<!-- TaskSplitZFSMirror, Version: 12, Modified: 2019/04/06, Author: feurig -->
#Task: Split ZF Mirror
We need to reduce the size of the zfs pool on the two 600G disks on bs2020 and use the space for backups. To do this we need to split the mirror and use the freed disk to create a new partition. Move that into place and then move the old data onto the smaller partition before finally repartitioning the remaining disk and mirror both new partitions.

Move running containers to kb2018

Get existing disk info.
	
```sh
root@bs2020:~# zpool status -L devel
	pool: devel
	state: ONLINE
	scan: resilvered 132G in 2h2m with 0 errors on Thu Apr  4 00:31:41 2019
config:

	NAME        STATE     READ WRITE CKSUM
	devel       ONLINE       0     0     0
		mirror-0  ONLINE       0     0     0
		sdc      ONLINE       0     0     0
		sdd      ONLINE       0     0     0

errors: No known data errors
root@bs2020:~# zpool status  devel
	pool: devel
	state: ONLINE
	scan: resilvered 132G in 2h2m with 0 errors on Thu Apr  4 00:41:41 2019
config:

	NAME                              STATE     READ WRITE CKSUM
	devel                             ONLINE       0     0     0
		mirror-0                        ONLINE       0     0     0
		scsi-350000c0f022fd4c8        ONLINE       0     0     0
		scsi-35000c50047d0926f        ONLINE       0     0     0

```
errors: No known data errors
	
	
Split devel mirror. 
```sh
root@bs2020:~# zpool split -R /newdevel devel newdevel 
root@bs2020:~# zpool status
	pool: devel
	state: ONLINE
	scan: scrub repaired 0B in 0h38m with 0 errors on Sun Mar 10 01:02:05 2019
config:

	NAME                      STATE     READ WRITE CKSUM
	devel                     ONLINE       0     0     0
		scsi-35000c50047d0926f  ONLINE       0     0     0

errors: No known data errors

	pool: infra
	state: ONLINE
	scan: scrub repaired 0B in 0h1m with 0 errors on Sun Mar 10 00:25:17 2019
config:

	NAME                        STATE     READ WRITE CKSUM
	infra                       ONLINE       0     0     0
		mirror-0                  ONLINE       0     0     0
		scsi-35000cca00b33a264  ONLINE       0     0     0
		scsi-350000395a8336d34  ONLINE       0     0     0

errors: No known data errors

	pool: newdevel
	state: ONLINE
	scan: scrub repaired 0B in 0h38m with 0 errors on Sun Mar 10 01:02:05 2019
config:

	NAME                      STATE     READ WRITE CKSUM
	newdevel                  ONLINE       0     0     0
		scsi-350000c0f022fd4c8  ONLINE       0     0     0
```	
	
Wipe and partition newly freed disk
	
```sh
root@bs2020:~# zpool destroy newdevel 
root@bs2020:~# parted /dev/sdc
GNU Parted 3.2
Using /dev/sdc
(parted) mklabel gpt                                                      
Warning: The existing disk label on /dev/sdc will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? yes                                                               
(parted) mkpart                                                           
Partition name?  []? images
File system type?  [ext2]? zfs                                            
Start? 0%                                                                 
End? 50%                                                                  
(parted) mkpart                                                           
Partition name?  []? devel                                                
File system type?  [ext2]? zfs                                            
Start? 50%                                                                
End? 100%                                                                 
(parted) print                                                            
Model: WD WD6001BKHG (scsi)
Disk /dev/sdc: 600GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End    Size   File system  Name    Flags
	1      1049kB  300GB  300GB  zfs          images
	2      300GB   600GB  300GB  zfs          devel

(parted) quit                                                             
```	
	
Build new zfs partition for /var/lib/lxd/images and move the old data
	
```sh
root@bs2020:~# systemctl stop lxd 
root@bs2020:~# zpool create lxd-images scsi-350000c0f022fd4c8-part1 -m/var/lib/lxd/images
root@bs2020:~# df -k
Filesystem     1K-blocks     Used Available Use% Mounted on
udev            49458232        0  49458232   0% /dev
tmpfs            9897784     1488   9896296   1% /run
/dev/sdg2      138930656 63784172  68019548  49% /
tmpfs           49488916        0  49488916   0% /dev/shm
tmpfs               5120        0      5120   0% /run/lock
tmpfs           49488916        0  49488916   0% /sys/fs/cgroup
/dev/loop0         53376    53376         0 100% /snap/lxd/10234
/dev/loop1         91392    91392         0 100% /snap/core/6673
/dev/loop2         55168    55168         0 100% /snap/lxd/10343
/dev/loop3         93312    93312         0 100% /snap/core/6531
/dev/loop4         53376    53376         0 100% /snap/lxd/10289
/dev/loop5         93184    93184         0 100% /snap/core/6405
/dev/sdg1         523248     6164    517084   2% /boot/efi
/dev/sda1      480589544 47764176 408389708  11% /archive
tmpfs            9897780        0   9897780   0% /run/user/1000
lxd-images     282394496        0 282394496   0% /var/lib/lxd/images
root@bs2020:~# mv /var/lib/lxd/images.tmp/* /var/lib/lxd/images/
df -k
root@bs2020:~# df -k
Filesystem     1K-blocks     Used Available Use% Mounted on
udev            49458232        0  49458232   0% /dev
tmpfs            9897784     1496   9896288   1% /run
/dev/sdg2      138930656 15992764 115810956  13% /
tmpfs           49488916        0  49488916   0% /dev/shm
tmpfs               5120        0      5120   0% /run/lock
tmpfs           49488916        0  49488916   0% /sys/fs/cgroup
/dev/loop0         53376    53376         0 100% /snap/lxd/10234
/dev/loop1         91392    91392         0 100% /snap/core/6673
/dev/loop2         55168    55168         0 100% /snap/lxd/10343
/dev/loop3         93312    93312         0 100% /snap/core/6531
/dev/loop4         53376    53376         0 100% /snap/lxd/10289
/dev/loop5         93184    93184         0 100% /snap/core/6405
/dev/sdg1         523248     6164    517084   2% /boot/efi
/dev/sda1      480589544 47764176 408389708  11% /archive
tmpfs            9897780        0   9897780   0% /run/user/1000
lxd-images     282392832 47751552 234641280  17% /var/lib/lxd/images
root@bs2020:~# systemctl start lxd
```	
Build new devel pool on second  partition and move data to smaller partition..
	
```sh
root@bs2020:~# zpool create devels scsi-350000c0f022fd4c8-part2
root@bs2020:~#  zfs snapshot -r devel@fullbackup
root@bs2020:~# zfs send -R devel@fullbackup | pv | zfs receive -vFdu devels
....
```	
Offline old devel pool replace with new
	
```sh
root@bs2020:~# systemctl stop lxd
root@bs2020:~# zpool export devels
root@bs2020:~# zpool destroy devel
root@bs2020:~# zpool import devels devel
root@bs2020:~# zpool status
	pool: devel
	state: ONLINE
	scan: none requested
config:

	NAME                            STATE     READ WRITE CKSUM
	devel                           ONLINE       0     0     0
		scsi-350000c0f022fd4c8-part2  ONLINE       0     0     0

errors: No known data errors
...
root@bs2020:~# systemctl start lxd
```	
Repartition remaining disk.
	
```sh
root@bs2020:~# parted /dev/sdd
GNU Parted 3.2
Using /dev/sdd
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print                                                            
Model: SEAGATE ST9600205SS (scsi)
Disk /dev/sdd: 600GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End    Size    File system  Name                  Flags
	1      1049kB  600GB  600GB   zfs          zfs-f77cf42a401f4fa0
	9      600GB   600GB  8389kB

(parted) mklabel                                                          
New disk label type? gpt                                                  
Warning: The existing disk label on /dev/sdd will be destroyed and all data on this disk will be lost. Do you want to continue?
Yes/No? yes                                                               
(parted) mkpart                                                           
Partition name?  []? images                                               
File system type?  [ext2]? zfs                                            
Start? 0%                                                                 
End? 50%                                                                  
(parted) mkpart                                                          
Partition name?  []? devel                                                
File system type?  [ext2]? zfs                                            
Start? 50%                                                                
End? 100%                                                                 
(parted) print                                                            
Model: SEAGATE ST9600205SS (scsi)
Disk /dev/sdd: 600GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End    Size   File system  Name    Flags
	1      1049kB  300GB  300GB  zfs          images
	2      300GB   600GB  300GB  zfs          devel

(parted) quit                                                             
Information: You may need to update /etc/fstab.
```	
Add new partitions as mirrors
	
```sh
root@bs2020:~# zpool attach lxd-images scsi-350000c0f022fd4c8-part1 scsi-35000c50047d0926f-part1
root@bs2020:~# zpool attach devel scsi-350000c0f022fd4c8-part2 scsi-35000c50047d0926f-part2
root@bs2020:~# zpool status
	pool: devel
	state: ONLINE
status: One or more devices is currently being resilvered.  The pool will
	continue to function, possibly in a degraded state.
action: Wait for the resilver to complete.
	scan: resilver in progress since Fri Apr  5 22:39:37 2019
	50.0M scanned out of 132G at 2.94M/s, 12h42m to go
	48.6M resilvered, 0.04% done
config:

	NAME                              STATE     READ WRITE CKSUM
	devel                             ONLINE       0     0     0
		mirror-0                        ONLINE       0     0     0
		scsi-350000c0f022fd4c8-part2  ONLINE       0     0     0
		scsi-35000c50047d0926f-part2  ONLINE       0     0     0  (resilvering)

errors: No known data errors

	pool: infra
	state: ONLINE
	scan: scrub repaired 0B in 0h1m with 0 errors on Sun Mar 10 00:25:17 2019
config:

	NAME                        STATE     READ WRITE CKSUM
	infra                       ONLINE       0     0     0
		mirror-0                  ONLINE       0     0     0
		scsi-35000cca00b33a264  ONLINE       0     0     0
		scsi-350000395a8336d34  ONLINE       0     0     0

errors: No known data errors

	pool: lxd-images
	state: ONLINE
status: One or more devices is currently being resilvered.  The pool will
	continue to function, possibly in a degraded state.
action: Wait for the resilver to complete.
	scan: resilver in progress since Fri Apr  5 22:39:09 2019
	3.70G scanned out of 45.6G at 84.2M/s, 0h8m to go
	3.70G resilvered, 8.11% done
config:

	NAME                              STATE     READ WRITE CKSUM
	lxd-images                        ONLINE       0     0     0
		mirror-0                        ONLINE       0     0     0
		scsi-350000c0f022fd4c8-part1  ONLINE       0     0     0
		scsi-35000c50047d0926f-part1  ONLINE       0     0     0  (resilvering)

errors: No known data errors
root@bs2020:~# 
```
Move containers back to bs2020

Continue work on backup scripts.
	
	
## References
https://github.com/lxc/lxd/issues/4984