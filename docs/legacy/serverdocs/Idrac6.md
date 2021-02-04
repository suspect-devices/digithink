The Dell idrac is a very powerful tool allowing remote administration of a server down to bare bones os installation.  The console feature of this tool is based on a Java app which is downloaded from the idrac and which then sets up a vnc style remote console. As the hardware ages this code becomes less and less secure and is often broken but updates to the local os (OS X being ours) and to java. 

When purchasing a dell with idrac capabilities ALWAYS opt for the "Enterprise" edition. 
* The enterprise edition uses a separate network connection allowing it to be placed on a secure lan.
* The enterprise edition allows remote console 

## securing the idrac
* Since the idrac allows complete control of the system it should never be allowed directly on the network. 
* The idrac is initially configured with a "root" user who's password is "calvin" 
* Change it ASAP
* Create local administrators. 
* Once local accounts are tested strip the root user of all privileges.
 [[Image(wiki:Idrac6:users.png)]]
* The idrac needs several ports opened to be controlled.
  * https
  * ssh
  * vnc (5900)

## remote console fun
The latest version of java disables the graphical remote console. The console makes you jump through all of the hoops to run launches and fails to connect. The solution is to disable the disabling of ssl3.
	
	bash-3.2# find / -name java.security -print
	/Applications/Arduino.app/Contents/PlugIns/JavaAppletPlugin.plugin/Contents/Home/lib/security/java.security
	/Applications/microchip/mplabx/v3.15/sys/java/jre1.7.0_79.jre/Contents/Home/lib/security/java.security
	/Applications/microchip/mplabx/v3.15/sys/java/jre1.8.0_60.jre/Contents/Home/lib/security/java.security
	/Applications/Xcode.app/Contents/Applications/Application Loader.app/Contents/itms/java/lib/security/java.security
	find: /dev/fd/3: Not a directory
	find: /dev/fd/4: Not a directory
	/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/lib/security/java.security
	/Users/don/Downloads/Energia.app/Contents/PlugIns/jdk1.8.0_91.jdk/Contents/Home/jre/lib/security/java.security
	bash-3.2# nano /Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/lib/security/java.security
	....
	.... change the commented out line to the one below it ....
	#jdk.tls.disabledAlgorithms=SSLv3, RC4, MD5withRSA, DH keySize < 1024, \
	jdk.tls.disabledAlgorithms, RC4, MD5withRSA, DH keySize < 1024, \
	    EC keySize < 224, DES40_CBC, RC4_40, 3DES_EDE_CBC
	....
	
== Enabling bios and console accèss via ssh.
...Unfortunately this requires a functioning console..
As well as access to the f2 key.

[[Image(wiki:Idrac6:fnkeys.png)]]
* Enter bios
[[Image(boot.png)]]
* Select Serial settings.
[[Image(BIOS.png)]]
* set console redirection to com2
[[Image(BIOSSerialSettings.png)]]
## Connecting to the console
* once you can ssh to the idrac set up the serial using racadm
	
	steve:~ don$ ssh -p222 feurig@198.202.31.242
	feurig@198.202.31.242's password: 
	/admin1-> racadm config -g cfgSerial -o cfgSerialBaudRate 115200
	Object value modified successfully
	/admin1-> racadm config -g cfgSerial -o cfgSerialCom2RedirEnable 1
	Object value modified successfully
	/admin1-> racadm config -g cfgSerial -o cfgSerialSshEnable 1
	Object value modified successfully
	/admin1-> racadm config -g cfgIpmiSol -o cfgIpmiSolEnable 1
	Object value modified successfully
	/admin1-> racadm config -g cfgIpmiSol -o cfgIpmiSolBaudRate 115200
	Object value modified successfully
	
* then you can connect to the console
	
	/admin1-> console com2
	
	Connected to Serial Device 2. To end type: ^\
	
## fixing grub
* you need set the console to ttyS1 by adding a console=ttyS1,115200n8 to the end of the kernel line
	
	root@bs2020:~# nano /boot/grub/menu.list
	...
	kernel          /boot/vmlinuz-4.4.0-96-generic root=UUID=8cafbdf6-441e-4f76-b89c-017fc22253f9 ro console=hvc0 console=ttyS1,115200n8
	
* add the changes to /etc/default/grub so that it will survive updates to the kernel.
	
	root@bs2020:~# nano /etc/default/grub
	...
	GRUB_TERMINAL='serial console'
	GRUB_CMDLINE_LINUX="console=hvc0 console=ttyS1,115200n8"
	GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=1 --word=8 --parity=no --stop=1"
	root@bs2020:~# update-grub
	
* reboot the server and attach to the console.
[[Image(post0.png)]]

[[Image(post1.png)]]
## as of Ubuntu 16.04 systemd actually figures it out from there
Once the console is set systemd creates a getty process for it. Otherwise you can chase the web around for the pre-upstart (i.e. /etc/inittab), upstart (/etc/init/xxxx), and early systemd questions/solutions. Hope they don't screw it up in 18.04
* Victory!!!
[[Image(login.png)]]
## Afterthoughts / Todo
* look at ipmi
   http://www.alleft.com/sysadmin/ipmi-sol-inexpensive-remote-console/
## linkdump
* http://media.community.dell.com/en/dtc/attach/idrac6_security_v1.pdf
* https://gist.github.com/xbb/4fd651c2493ad9284dbcb827dc8886d6
* https://www.dell.com/community/Systems-Management-General/iDRAC6-Virtual-Console-Connection-Failed/td-p/5144021/page/3
* http://support.hkti.net/support/solutions/articles/3000003121--for-dell-user-how-to-open-dell-idrac-virtual-console
* https://www.slac.stanford.edu/grp/cd/soft/unix/EnableSerialConsoleAccessViaSSH.htm
* https://serverfault.com/questions/269382/garbled-using-from-dell-drac-for-serial-console-redirection
* https://www.serverhome.nl/media/specsheets/Dell/DRAC/iDRAC6-user-guide.pdf
* http://jonamiki.com/2014/10/18/sol-serial-over-lan-connection-from-linux-to-dell-idrac-or-bmc/
* https://www.hiroom2.com/2016/06/06/ubuntu-16-04-grub2-and-linux-with-serial-console/
* http://0pointer.de/blog/projects/serial-console.html
* https://lnxgeek.wordpress.com/2018/02/16/serial-console-howto-ubuntu-16-04/
* http://lukeluo.blogspot.com/2015/04/dell-r710-idrac6-setup-with-ssh-console.html