#Imagebuilder notes
## Building firmware using imagebuilder
In the same page as the binary releases for openwrt/LEDE is the image builder for that architecture for instance at the bottom https://downloads.lede-project.org/releases/17.01.4/targets/ar71xx/generic/ there is a link https://downloads.lede-project.org/releases/17.01.4/targets/ar71xx/generic/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64.tar.xz. which we untar into /home/openwrt/xx.xx.xx/  on the sandbox.suspectdevices.com container (where xx.xx.xx is the release number. Then we can build the image as follows.
	
	root@sandbox:~# cd /home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64
	root@sandbox:/home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64# make
	Available Commands:
		help:	This help text
		info:	Show a list of available target profiles
		clean:	Remove images and temporary build files
		image:	Build an image (see below for more information).
	
	Building images:
		By default 'make image' will create an image with the default
		target profile and package set. You can use the following parameters
		to change that:
	
		make image PROFILE="<profilename>" # override the default target profile
		make image PACKAGES="<pkg1> [<pkg2> [<pkg3> ...]]" # include extra packages
		make image FILES="<path>" # include extra files from <path>
		make image BIN_DIR="<path>" # alternative output directory for the images
		make image EXTRA_IMAGE_NAME="<string>" # Add this to the output image filename (sanitized)
	root@sandbox:/home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64# make info
	Current Target: "ar71xx (Generic)"
	Default Packages: base-files libc libgcc busybox dropbear mtd uci opkg netifd fstools uclient-fetch logd kmod-gpio-button-hotplug swconfig kmod-ath9k wpad-mini uboot-envtools dnsmasq iptables ip6tables ppp ppp-mod-pppoe firewall odhcpd odhcp6c
	Available Profiles:
	
	Default:
	    Default Profile (all drivers)
	    Packages: kmod-usb-core kmod-usb-ohci kmod-usb2 kmod-usb-ledtrig-usbport
	ALFAAP120C:
	...
	wndr3700:
	    NETGEAR WNDR3700
	    Packages: kmod-usb-core kmod-usb-ohci kmod-usb2 kmod-usb-ledtrig-usbport kmod-leds-wndr3700-usb
	wndr3700v2:
	    NETGEAR WNDR3700 v2
	    Packages: kmod-usb-core kmod-usb-ohci kmod-usb2 kmod-usb-ledtrig-usbport kmod-leds-wndr3700-usb
	wndr3800:
	...
	root@sandbox:/home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64# make PROFILE="wndr3700v2" PACKAGES="nano" image
	make[1]: Entering directory '/home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64'
	...
	
The resulting firmware will be placed in the bin directory. You can use the factrory images to "update" the routers factory firmware to lede. Once you have it installed you can install the next version or future builds using sysupgrade.
	
	don@bob2:~/LEDE$ scp feurig@sandbox:/home/openwrt/17.01.4/lede-imagebuilder-17.01.4-ar71xx-generic.Linux-x86_64/bin/targets/ar71xx/generic/lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin .
	lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin                        100% 3328KB   1.1MB/s   00:03    
	don@bob2:~/LEDE$ scp -P 2222 lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin  root@198.202.31.241:/tmp/
	lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin                        100% 3328KB  92.4KB/s   00:36    
	don@bob2:~/LEDE$ ssh -p2222 root@198.202.31.241
	
	
	BusyBox v1.23.2 (2015-07-25 15:09:46 CEST) built-in shell (ash)
	
	  _______                     ________        __
	 |       |.-----.-----.-----.|  |  |  |.----.|  |_
	 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
	 |_______||   __|_____|__|__||________||__|  |____|
	          |__| W I R E L E S S   F R E E D O M
	 -----------------------------------------------------
	 CHAOS CALMER (15.05, r46767)
	 -----------------------------------------------------
	  * 1 1/2 oz Gin            Shake with a glassful
	  * 1/4 oz Triple Sec       of broken ice and pour
	  * 3/4 oz Lime Juice       unstrained into a goblet.
	  * 1 1/2 oz Orange Juice
	  * 1 tsp. Grenadine Syrup
	 -----------------------------------------------------
	root@vpn:~# cd /tmp/
	root@vpn:/tmp# sys
	sysctl      sysupgrade
	root@vpn:/tmp# sysupgrade -v 
	.jail/
	.uci/
	TZ
	dhcp.leases
	dnsmasq.d/
	etc/
	hosts/
	lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin
	lib/
	lock/
	log/
	overlay/
	racoon/
	resolv.conf
	resolv.conf.auto
	run/
	state/
	sysinfo/
	root@vpn:/tmp# sysupgrade -v lede-17.01.4-ar71xx-generic-wndr3700v2-squashfs-sysupgrade.bin 
	Saving config files...
	etc/config/dhcp
	etc/config/dropbear
	etc/config/firewall
	etc/config/luci
	etc/config/network
	etc/config/rpcd
	etc/config/system
	etc/config/ubootenv
	etc/config/ucitrack
	etc/config/uhttpd
	etc/config/wireless
	etc/dnsmasq.conf
	etc/dropbear/authorized_keys
	etc/dropbear/dropbear_dss_host_key
	etc/dropbear/dropbear_rsa_host_key
	etc/firewall.user
	etc/fw_env.config
	etc/group
	etc/hosts
	etc/inittab
	etc/iproute2/rt_tables
	etc/ipsec.conf
	etc/ipsec.secrets
	etc/ipsec.user
	etc/openldap/ldap.conf
	etc/opkg.conf
	etc/passwd
	etc/ppp/chap-secrets
	etc/ppp/filter
	etc/ppp/options
	etc/ppp/options.xl2tpd
	etc/profile
	etc/protocols
	etc/racoon.conf
	etc/racoon/psk.txt
	etc/rc.local
	etc/services
	etc/shadow
	etc/shells
	etc/ssl/openssl.cnf
	etc/strongswan.conf
	etc/sysctl.conf
	etc/sysupgrade.conf
	etc/xl2tpd/xl2tp-secrets
	etc/xl2tpd/xl2tpd.conf
	killall: watchdog: no process killed
	Sending TERM to remaining processes ... odhcpd racoon uhttpd xl2tpd starter charon ntpd odhcp6c dnsmasq ubusd askfirst logd rpcd netifd 
	Sending KILL to remaining processes ... askfirst 
	Switching to ramdisk...
	Performing system upgrade...
	Unlocking firmware ...
	
	Writing from <stdin> to firmware ...  [w]
	[w]
	   
	Appending jffs2 data from /tmp/sysupgrade.tgz to firmware...TRX header not found
	Error fixing up TRX header
	    
	Upgrade completed
	Rebooting system...
	
### References
* https://openwrt.org/docs/guide-user/additional-software/imagebuilder
* http://blog.suspectdevices.com/blahg/electronics/making-due-with-what-you-have/
