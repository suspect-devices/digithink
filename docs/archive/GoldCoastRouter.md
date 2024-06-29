<!-- GoldCoastRouter, Version: 6, Modified: 2021/04/15, Author: feurig -->
#Gold Coast

 Gold Coast (goldcoast.lan) is the house router for portland. The configuration and this doc are at https://bitbucket.org/houselan/config/src/master/


## LEDE 19.07 on the Ubiquity ER-lite3

The Ubiquity EdgeRouter Lite is my new favorite OpenWrt device. It is fast and inexpensive ($150 new) and the os is on a USB Stick. 
[[Image(https://prd-www-cdn.ubnt.com/media/images/product-features/ER-lite-features-UNMS.jpg)]]

### Pros
* 3 independent Gigabit network ports.
* Serial Console
* Cheap and still supported.
* Stock Edge-os would work for most tasks.
* OS on a USB-stick easiest backup and install EVER.
* 512 K of memory.

### Cons (some assembly required)
* Because the stock usb stick and (unused) flash is only 4K LEDE considers it a 4K and are threatening to stop producing stock images after 19.07. 
* Third party usb sticks take longer to start up than the on board bootloader (U-boot) expects. So a pause and usb reset need to be configured.

## How do I get set up?
### Building 19.07 for the device
Getting the source. See LEDE documentation for dependencies.
	
	feurig@vasily:~$ git clone https://git.openwrt.org/openwrt/openwrt.git
	

Building for the target
	
	feurig@vasily:~$ cd openwrt/
	feurig@vasily:~/openwrt$ make clean
	feurig@vasily:~/openwrt$ git pull
	feurig@vasily:~/openwrt$ ./scripts/feeds update -a
	feurig@vasily:~/openwrt$ ./scripts/feeds install -a
	feurig@vasily:~/openwrt$ make menuconfig
	feurig@vasily:~/openwrt$ make -j8 download world
	feurig@vasily:~/openwrt$ mv bin/targets/octeon/generic/openwrt-octeon-ubnt_edgerouter-lite-ext4-sysupgrade.tar.gz ~/firmware/
	feurig@vasily:~/openwrt$ ./scripts/diffconfig.sh > ../firmware/openwrt-octeon-ubnt_edgerouter-lite-ext4-sysupgrade.diffconfig
	

### Deploying the image

Download the image from vasily 
	
	feurig@colbert:~ $ scp feurig@wrt.suspectdevices.com:firmware/openwrt-octeon-ubnt_edgerouter-lite-ext4-sysupgrade.tar.gz .
	

Format the stick with 2 partitions (142M dos and the lemaining linux)
	
	root@colbert:~ # fdisk -l
	... On our machine, this is our disk ...
	Disk /dev/sda: 7.6 GiB, 8166703104 bytes, 15950592 sectors
	...
	root@colbert:~ # fdisk /dev/sda
	... Partition disk here ...
	root@colbert:~ # fdisk -l
	...
	Disk /dev/sda: 7.6 GiB, 8166703104 bytes, 15950592 sectors
	Disk model: USB 2.0 FD      
	...
	Device     Boot  Start     End Sectors  Size Id Type
	/dev/sda1         2048  292863  290816  142M  c W95 FAT32 (LBA)
	/dev/sda2       292864 3710975 3418112  1.6G 83 Linux
	...
	root@colbert:/home/feurig# mkfs.vfat /dev/sda1
	root@colbert:/home/feurig# mkfs.ext4 /dev/sda2
	

Copy firmware to usb stick
	
	root@colbert:~ # mkdir scratch
	root@colbert:~ # cd scratch/
	root@colbert:~ # tar -xf ../openwrt-octeon-ubnt_edgerouter-lite-ext4-sysupgrade.tar.gz 
	root@colbert:~ # mkdir root oroot kernel
	root@colbert:~ # mount /dev/sda1 kernel/
	root@colbert:~ # mount /dev/sda2 root/
	root@colbert:~ # mount sysupgrade-erlite/root oroot -o loop
	root@colbert:~ # cp sysupgrade-erlite/kernel kernel/vmlinux.64
	root@colbert:~ # md5sum sysupgrade-erlite/kernel | cut -d' ' -f 1 > kernel/vmlinux.64.md5
	root@colbert:~ # rsync -aHAX oroot/* root/
	root@colbert:~ # umount kernel root oroot
	root@colbert:~ # sync
	

### Fixing the bootloader for standard USB Sticks.

If the usb stick used takes longer than the stock one to initialize the boot will fail.
	
	don$ screen /dev/tty.usbserial 115200
	...
	U-Boot 1.1.1 (UBNT Build ID: 4670715-gbd7e2d7) (Build time: May 27 2014 - 11:16:22)
	.
	BIST check passed.
	UBNT_E100 r1:2, r2:18, f:4/71, serial #: 802AA84CE978
	MPR 13-00318-18
	Core clock: 500 MHz, DDR clock: 266 MHz (532 Mhz data rate)
	DRAM:  512 MB
	Clearing DRAM....... done
	Flash:  4 MB
	Net:   octeth0, octeth1, octeth2
	.
	USB:   (port 0) scanning bus for devices... 
	      USB device not responding, giving up (status=0)
	1 USB Devices found
	       scanning bus for storage devices...
	No device found. Not initialized?                                                                                                                  0 
	

Getting the stock boot command
	
	Octeon ubnt_e100# printenv               
	bootdelay=0
	baudrate=115200
	download_baudrate=115200
	nuke_env=protect off $(env_addr) +$(env_size);erase $(env_addr) +$(env_size)
	autoload=n
	ethact=octeth0
	bootcmd=fatload usb 0 $loadaddr vmlinux.64;bootoctlinux $loadaddr coremask=0x3 root=/dev/sda2 rootdelay=15 rw rootsqimg=squashfs.img rootsqwdir=w mtd
	...
	
Copy the bootcmd from the existing environment and add a delay and usb reset
	
	Octeon ubnt_e100# setenv bootcmd 'sleep 10;usb reset;fatload usb 0 $loadaddr vmlinux.64;bootoctlinux $loadaddr coremask=0x3 root=/dev/sda2 rootdelay=15 rw rootsqimg=squashfs.img rootsqwdir=w mtd'
	Octeon ubnt_e100# saveenv
	Octeon ubnt_e100# reset
	
## Basic LEDE Configuration

* network
* dnsmasq
* firewall
* /etc/ethers

## References

### Primary

*  [OpenWrt Hardware Page](https://openwrt.org/toh/ubiquiti/edgerouter.lite)
*  [https://web.rory.co.nz/2018/02/edgerouter-lite-3-failing-to-boot/]( https://web.rory.co.nz/2018/02/edgerouter-lite-3-failing-to-boot/)

### Link Pile

* https://community.ui.com/questions/EdgeMax-rescue-kit-now-you-can-reinstall-EdgeOS-from-scratch/58d474b4-604d-48c9-871d-ff44fd9240f3#M12098
* https://www.kc8apf.net/2018/01/ubiquiti-edgerouter-lite-usb-surgery/
* https://github.com/sowbug/mkeosimg
* http://blog.darrenscott.com/2016/09/03/recovering-an-unresponsive-ubiquiti-edgerouter-lite-router/
* https://community.ui.com/questions/New-U-Boot-image-for-better-USB-drive-compatibility/c59436cc-dfca-4fab-a923-ba5cdc688a6f?page=2
