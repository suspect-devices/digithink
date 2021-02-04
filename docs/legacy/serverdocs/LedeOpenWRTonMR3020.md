# LEDE build (old)

Building new firmware
	
	root@sandbox:/home/openwrt/15.05.1/OpenWrt-ImageBuilder-15.05.1-ar71xx-generic.Linux-x86_64/bin/ar71xx# make info
	....
	root@sandbox:/home/openwrt/15.05.1/OpenWrt-ImageBuilder-15.05.1-ar71xx-generic.Linux-x86_64/bin/ar71xx# make image PROFILE=TLMR3020 PACKAGES="nano"
	...
	
getting firmware onto local system.
the stock firmware will not accept a firmware that is not the same name as a stock firmware.
	
	viscious:vpn don$ scp feurig@sandbox:/home/openwrt/15.05.1/OpenWrt-ImageBuilder-15.05.1-ar71xx-generic.Linux-x86_64/bin/ar71xx/openwrt-15.05.1-ar71xx-generic-tl-mr3020-v1-squashfs-factory.bin .
	viscious:vpn don$ mv openwrt-15.05.1-ar71xx-generic-tl-mr3020-v1-squashfs-factory.bin  mr3020nv1_en_3_17_2_up_boot(150921).bin
	
At this point you can telnet to the router and reset the root password (which will disable telnet and enable ssh)
### related
* [wiki:LEDE LEDE]
### References
* https://nicolas314.wordpress.com/2015/12/09/openwrt-on-mr3020/
* https://wolfgang.reutz.at/2012/04/12/openwrt-on-tp-link-mr3020-as-infopoint-with-local-webserver/
* https://blog.philippklaus.de/2012/03/openwrt-on-a-tp-link-tl-mr3020-router/
* https://openwrt.org/docs/guide-user/additional-software/imagebuilder
