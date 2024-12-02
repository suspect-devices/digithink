<!-- NotesOnDL380RaidBios, Version: 1, Modified: 2018/12/10, Author: feurig -->
# Dl380 Raid Bios notes
Flesh this out with new 
## Configuring the disks using the raid controller bios

	
```sh
steve:~ don$ ssh kates-ilo.suspectdevices.com
User:feurig logged-in to kb2018.suspectdevices.com(192.168.31.119 / FE80::9E8E:99FF:FE0C:BAD8)
iLO 3 Advanced for BladeSystem 1.88 at  Jul 13 2016
Server Name: kb2018
Server Power: On

</>hpiLO-> vsp

Virtual Serial Port Active: COM2

Starting virtual serial port.
Press 'ESC (' to return to the CLI Session.

root@kb2018:~# fdisk -l|grep Disk\ \/
Disk /dev/loop0: 86.9 MiB, 91099136 bytes, 177928 sectors
Disk /dev/loop1: 87.9 MiB, 92164096 bytes, 180008 sectors
Disk /dev/loop2: 63.4 MiB, 66486272 bytes, 129856 sectors
Disk /dev/sda: 136.7 GiB, 146778685440 bytes, 286677120 sectors

root@kb2018:~# reboot
[  OK  ] Stopped Stop ureadahead data collection 45s after completed          Stopping Session 98 of user feurig.
			Stopping Availability of block devices...
	...
	
[  OK  ] Reached target Shutdown.
[  OK  ] Reached target Final Step.
			Starting Reboot...
[292357.910620] reboot: Restarting system



After several seconds you will see a text based bios screen
[[Image(CaptiveRaidController:ILo3SSHConsoleBooting.png)]]
After the network controller is started the raid controller will give you a chance to configure it. 
_PRESS F8 NOW!! _ \\ 
[[Image(CaptiveRaidController:PressF8NOW.png)]]

If you miss it you will have to escape back to the ILO3 and power cycle the machine. _(This is ok because the disks are not active until the machine actually boots)_

Booting from Hard Drive C: 
<ESC> (
</>hpiLO-> power off hard

status=0
status_tag=COMMAND COMPLETED
Wed Sep 26 15:31:57 2018



Forcing server power off .......
Please wait 6 seconds for this operation to complete.



</>hpiLO-> power         

status=0
status_tag=COMMAND COMPLETED
Wed Sep 26 15:32:04 2018



power: server power is currently: Off


</>hpiLO-> power on 

status=0
status_tag=COMMAND COMPLETED
Wed Sep 26 15:32:21 2018



Server powering on .......



</>hpiLO-> vsp

Virtual Serial Port Active: COM2

Starting virtual serial port.
Press 'ESC (' to return to the CLI Session.

```
Once in the raid controller bios you will get a main menu.

 [[Image(CaptiveRaidController:ViewLogicalDrive.png)]]

If you select view logical drives will see that the first two disks are combined into a mirrored pair and that there are no other drives defined. 

So we select "Create Logical Drive". Which gives us the following screen. 
 
 [[Image(CaptiveRaidController:CreateLogicalDriveDefaults.png)]]

Notice that the defaults are to create a raid 1+0 array with the first two matching disks. Deselecting either disk (down arrow, spacebar) will cause the raid configuration to automatically drop to RAID 0

Press Enter when finished.  The next screen will ask you to verify the creation <F8>

Repeat this for each remaining disk. 

When you are finished you can view the logical drives.
 [[Image(CaptiveRaidController:RaidConfFinished.png)]]

The <ESC> key will walk you back out so you can continue to boot. 

## success
	
	root@kb2018:~# fdisk -l|grep Disk\ \/
	Disk /dev/loop0: 86.9 MiB, 91099136 bytes, 177928 sectors
	Disk /dev/loop1: 87.9 MiB, 92164096 bytes, 180008 sectors
	Disk /dev/loop2: 63.4 MiB, 66486272 bytes, 129856 sectors
	Disk /dev/sda: 136.7 GiB, 146778685440 bytes, 286677120 sectors
	Disk /dev/sdb: 223.6 GiB, 240021504000 bytes, 468792000 sectors
	Disk /dev/sdc: 223.6 GiB, 240021504000 bytes, 468792000 sectors
	Disk /dev/sdd: 279.4 GiB, 299966445568 bytes, 585871964 sectors
	Disk /dev/sde: 279.4 GiB, 299966445568 bytes, 585871964 sectors
	root@kb2018:~# 
	
### References
- https://www.n0tes.fr/2024/03/04/CLI-HPE-ssacli-and-hpssacli-tools/
- https://gist.github.com/ameiji/bfb738ec5edd6ab701b2095ed05e138e