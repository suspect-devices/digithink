The process of replacing mirrored zfs disks is fairly simple. The changes are done by zpool attach and detach.
	
	zpool detach <pool> <disk-id>
	zpool attach <pool> <disk-id-to-mirror> <disk-id-mirrored-to>
	
The heavy lifting is done by zfs itself.

## process
### PREP
* use the [pdf article link](http://trac.suspectdevices.com/trac/wiki/ZFSDiskReplacement?format=pdfarticle) to print this before going down 
* If possible pre wipe and check the disks on a separate linux machine _(note: /dev/sdf is an placeholder for the disk mounted on that system)_
	
   ```
	root@homebox:~# wipefs -af --backup /dev/sdf
	/dev/sdf: 8 bytes were erased at offset 0x00000200 (gpt): 45 46 49 20 50 41 52 54
	/dev/sdf: 8 bytes were erased at offset 0x222ee64e00 (gpt): 45 46 49 20 50 41 52 54
	/dev/sdf: 2 bytes were erased at offset 0x000001fe (PMBR): 55 aa
	/dev/sdc: calling ioctl to re-read partition table: Success
	root@homebox:~# fdisk /dev/sdf
	....
	Command (m for help): g
	
	Created a new GPT disklabel (GUID: EBC5A0C9-E871-544F-A8EA-E31FCA655F9C).
	
	Command (m for help): w
	The partition table has been altered.
	Calling ioctl() to re-read partition table.
	Syncing disks.
	
	root@homebox:~# badblocks /dev/sdf
	....
	
```	

* insure that you can ssh into the box
### On site
The following assumes you have escalated to root privileges (sudo bash), in this case we are replacing /dev/sdc and /dev/sdd in the pool named 'level'

* check for the correct disk.
   The following should cause the disk to light up\
 _(<CTRL> C when you have identified the disk. Careful with the if/of here)_.
	
   ```
	root@bs2020:~# dd if=/dev/sdc of=/dev/null
```	
* find the disk in the pool.

   ```	
	root@bs2020:~# zpool status
	  pool: devel
	 state: ONLINE
	  scan: resilvered 9.95G in 0h4m with 0 errors on Sat Nov 10 22:00:41 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		devel                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000c50054fee503  ONLINE       0     0     0
		    scsi-35000c5005501b45b  ONLINE       0     0     0
	
	errors: No known data errors
	
	...
	root@bs2020:~# ls -ls /dev/disk/by-id/|grep scsi|grep -v "\-part"
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:22 scsi-350000395a8336d34 -> ../../sde
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:22 scsi-35000c50054fee503 -> ../../sdd
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:56 scsi-35000c5005501b45b -> ../../sdc
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:22 scsi-35000cca00b33a264 -> ../../sdf
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:22 scsi-3600508e00000000069cf3977618f1408 -> ../../sdg
	root@bs2020:~# 
```
  _We notice above that the disk we are looking for is scsi-35000c5005501b45b_

* detach the disk from the pool.
  
  ```	
	root@bs2020:~# zpool detach devel scsi-35000c5005501b45b 
	root@bs2020:~# zpool status
	  pool: devel
	 state: ONLINE
	  scan: resilvered 9.95G in 0h4m with 0 errors on Sat Nov 10 22:00:41 2018
	config:
	
		NAME                      STATE     READ WRITE CKSUM
		devel                     ONLINE       0     0     0
		  scsi-35000c50054fee503  ONLINE       0     0     0
	
	errors: No known data errors
	
	  pool: infra
	...
	root@bs2020:~#
```	

* even if expanding the disk size insure that auto expand is off.
	
  ```
	root@bs2020:~# zpool set autoexpand=off devel
```	

* Swap out the old disk with the new one. 

* find the new disk's id.  

   ```
	root@bs2020:~# partprobe
	root@bs2020:~# ls -ls /dev/disk/by-id/|grep sdc
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:56 scsi-xxxxxxxxxxxxxxx -> ../../sdc
	...   
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:56 xxx-xxxxxxxxxxxxxxx -> ../../sdc
```	

* _If the drive id does not change reboot the server_

* attach the new disk to the zfs pool  _(scsi-xxxxxxxxxxxxxxxx is the new id from the above step)_
	
  ```
	root@bs2020:~# zpool attach devel scsi-35000c50054fee503 scsi-xxxxxxxxxxxxxx
```	

* wait for pool to resliver
	
  ```
  	root@bs2020:~# zpool status
	  pool: devel
	 state: ONLINE
	status: One or more devices is currently being resilvered.  The pool will
		continue to function, possibly in a degraded state.
	action: Wait for the resilver to complete.
	  scan: resilver in progress since Sat Nov 10 21:56:04 2018
		8.54G scanned out of 9.95G at 35.5M/s, 0h0m to go
		8.54G resilvered, 85.85% done
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		devel                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000c50054fee503  ONLINE       0     0     0
		    scsi-35000c5005501b45b  ONLINE       0     0     0  (resilvering)
	
	errors: No known data errors
	
	  pool: infra
	...
	
	root@bs2020:~# zpool status
	.... repeat until finished reslivering .... 
	root@bs2020:~# zpool status
	  pool: devel
	 state: ONLINE
	  scan: scrub repaired 0B in 0h4m with 0 errors on Sat Nov 10 21:58:04 2018
	config:
	
		NAME                        STATE     READ WRITE CKSUM
		devel                       ONLINE       0     0     0
		  mirror-0                  ONLINE       0     0     0
		    scsi-35000cca00b33a264  ONLINE       0     0     0
		    scsi-350000395a8336d34  ONLINE       0     0     0
	
	errors: No known data errors
	...
```
	
* if expanding disk check for new size and if not expand it
	
* zfs list and check for larger disk pool 

* repeat process for disk in bay below (we already know its old id from above).

  ```
  	
	root@bs2020:~# dd if=/dev/sdd of=/dev/null
	root@bs2020:~# zpool detach devel scsi-35000c50054fee503  
	... swap disks ...
	root@bs2020:~# partprobe
	root@bs2020:~# ls -ls /dev/disk/by-id/|grep sdd
	0 lrwxrwxrwx 1 root root  9 Nov 10 21:56 scsi-yyyyyyyyyyyyyyyy-> ../../sdd
	... reboot if necessary ...
	root@bs2020:~# wipefs -a /dev/sdd
	...
	root@bs2020:~# fdisk /dev/sdd
	...
	root@bs2020:~# zpool attach devel scsi-xxxxxxxxxxxxxx scsi-yyyyyyyyyyyyyyy
	... wait for resliver...
```
	
* use the process below to grow disks to new size
	
  ```
  	# zpool set autoexpand=on devel
	# zpool online -e devel scsi-xxxxxxxxxxxxxxxxxxxx
	# zpool online -e devel scsi-yyyyyyyyyyyyyyyyyyy
	# zpool set autoexpand=off devel  
```	

### references

* https://tomasz.korwel.net/2014/01/03/growing-zfs-pool/
* https://jsosic.wordpress.com/2013/01/01/expanding-zfs-zpool-raid/
* https://serverfault.com/questions/5336/how-do-i-make-linux-recognize-a-new-sata-dev-sda-drive-i-hot-swapped-in-without