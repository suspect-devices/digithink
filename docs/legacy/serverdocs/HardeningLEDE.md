#Hardening LEDE
	
	BusyBox v1.30.1 () built-in shell (ash)
	
	  _______                     ________        __
	 |       |.-----.-----.-----.|  |  |  |.----.|  |_
	 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
	 |_______||   __|_____|__|__||________||__|  |____|
	          |__| W I R E L E S S   F R E E D O M
	 -----------------------------------------------------
	 OpenWrt 19.07.3, r11063-85e04e9f46
	 ----------------------------------------------------
	
### Add packages
In our build sudo, nano, and syslog-ng are included as well as the utilities to work with passwords and groups (shadow-useradd shadow-groupadd shadow-usermod) if your build does not you will need to install them. 
	
	root@OpenWrt:~# opkg update
	root@OpenWrt:~# opkg install shadow-useradd shadow-groupadd shadow-usermod
	root@OpenWrt:~# opkg install sudo nano syslog-ng
	
### Add Sudo Users
	
	root@OpenWrt:~# useradd -c "Joseph Wayne Dumoulin" -m joe -s /bin/ash
	root@OpenWrt:~# useradd -c "D Delmar Davis" -m feurig -s /bin/ash
	root@OpenWrt:~# groupadd --system sudo
	root@OpenWrt:~# usermod -a -G sudo joe
	root@OpenWrt:~# usermod -a -G sudo feurig
	root@OpenWrt:~# visudo
	...
	## Uncomment to allow members of group sudo to execute any command                   
	%sudo   ALL=(ALL) ALL                                                                
	...
	root@OpenWrt:~# passwd feurig
	root@OpenWrt:~# passwd joe
	
For each user add their authorized ssh keys.
	
	sudo -u feurig ash
	cd
	mkdir .ssh
	nano .ssh/authorized_keys
	... add keys ...
	
### Disable Root Login
Once you are able to log into the router using your ssh keys you should disable root access. The following is recommended but didnt work. _ALWAYS test that you are unable to login as root._
	
	root@OpenWrt:~# uci set dropbear.@dropbear[0].PasswordAuth="off"
	root@OpenWrt:~# uci set dropbear.@dropbear[0].RootPasswordAuth="off"
	root@OpenWrt:~# uci commit dropbear
	root@OpenWrt:~# reboot
	don@annie:~$ ssh root@192.168.128.215
	
	BusyBox v1.30.1 () built-in shell (ash)
	
	  _______                     ________        __
	 |       |.-----.-----.-----.|  |  |  |.----.|  |_
	 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
	 |_______||   __|_____|__|__||________||__|  |____|
	          |__| W I R E L E S S   F R E E D O M
	 -----------------------------------------------------
	 OpenWrt 19.07.3, r11063-85e04e9f46
	 -----------------------------------------------------
	root@OpenWrt:~#
	

Thats worse than ubuntu:ubuntu _Fuck that! Lock the root account and remove dropbears authorized keys._
	
	root@OpenWrt:~# passwd -l root
	root@OpenWrt:~# rm /etc/dropbear/authorized_keys 
	root@OpenWrt:~# ^D
	don@annie:~$ ssh root@192.168.128.215
	root@192.168.128.215: Permission denied (publickey).
	
Now the admin users need to log in using their personal ssh keys and escalate privileges using their password.
	
	don@annie:~$ ssh feurig@192.168.128.215
	  _______                     ________        __
	 |       |.-----.-----.-----.|  |  |  |.----.|  |_
	 |   -   ||  _  |  -__|     ||  |  |  ||   _||   _|
	 |_______||   __|_____|__|__||________||__|  |____|
	          |__| W I R E L E S S   F R E E D O M
	 -----------------------------------------------------
	 OpenWrt 19.07.3, r11063-85e04e9f46
	 -----------------------------------------------------
	feurig@OpenWrt:~$ sudo bash
	Password: 
	
#### preserving users home directories
In order to maintain the sudo users during upgrades you need to add /home and /etc/sudoers to the /etc/sysupgrade.conf file. The passwd, shadow, group and other files should already be saved by sysupgrade but the home directory is needed for the users .ssh/authorized_keys. 

### References
* https://openwrt.org/docs/guide-user/security/secure.access