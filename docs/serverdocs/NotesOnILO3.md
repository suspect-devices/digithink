<!-- NotesOnILO3, Version: 1, Modified: 2018/12/02, Author: trac -->
# ILO3 Notes
The ILO 3 card on the HP Prolient DL380 allows us complete remote control of the server for this reason the same security precautions which are used on the idrac6 need to be implemented.

### Securing the ILO3
The ilo3 is not directly accessible accept through the admin lan firewall. Eventually this will require vpn access however in the mean time it is accessed through port redirection. The ilo3s main access is through https. The port number for this is configurable along with the other ports used. (ssh + 2 ports for console redirection) 

[[Image(ILO3Notes:ilo3NetworkPorts.png)]]
Unless you are working in a MAAS environment the ipv6 should be disabled and the ipv4 address should be made static. This will require resetting the ILO3 itself.
[[Image(ILO3Notes:ILO3ResetILO.png)]]
#### Manage Admin Accounts
Create user and management accounts as soon as possible and demote or remove any existing accounts. 
[[Image(ILO3Notes:ilo3UserAdmin.png)]]
While there you should add your ssh keys for ssh connections. Note that only dsa keys are supported so you my need to create a separate public key.

	
	steve:~ don$ ssh-keygen -t dsa
	Generating public/private dsa key pair.
	...
	

### Java Console
The ILO 3 provides a java console similar to the one provided by the Dell idrac. It requires the remote  console port (17990) as well as the Virtual Medea Port (17988) to function properly. 
[[Image(ILO3Notes:HPBootSplash.png)]]
### Remote Media
Attaching an iso is straight  forward.
[[Image( ILO3Notes:ilo3RemovableMedia.png )]]
Using the Ubuntu 18.04 Live Server over a DSL connection is pokey and complains a lot but it does not fail.
[[Image(ILO3Notes:ilo3NetworkMountsAndLag.png)]]
### Enabling bios and console accèss via ssh.
Once you have administrative access to the ILO3 and you have an os install you can do everything vial ssh. Much like the idrac you need access to the f9 key.
[[Image(wiki:Idrac6:fnkeys.png)]]
* Enter bios
* Select Serial settings.
* set console redirection to com2
  _ you will have to do this in the advanced settings as well _
  [[Image(ILO3Notes:ILO Bios Virtual Serial Port.jpg)]]
## Connecting to the console
Once the bios is set up you can ssh to the console using your iso credentials and ssh key. 
	
	steve:~ don$ ssh -p22222 feurig@vpn.suspectdevices.com
	User:feurig logged-in to kb2018.suspectdevices.com(192.168.31.119 / FE80::9E8E:99FF:FE0C:BAD8)
	iLO 3 Advanced for BladeSystem 1.88 at  Jul 13 2016
	Server Name: kb2018
	Server Power: On
	
	</>hpiLO-> help
	
	status=0
	status_tag=COMMAND COMPLETED
	Sat Sep 22 20:20:42 2018
	...
	DMTF SMASH CLP Commands:
	...
	HP CLI Commands:
	
	POWER    : Control server power.
	UID      : Control Unit-ID light.
	NMI      : Generate an NMI.
	VM       : Virtual media commands.
	LANGUAGE : Command to set or get default language
	VSP      : Invoke virtual serial port.
	TEXTCONS : Invoke Remote Text Console.
	

Then you can connect to the console
	
	
	
	</>hpiLO-> vsp
	
	Virtual Serial Port Active: COM2
	
	Starting virtual serial port.
	Press 'ESC (' to return to the CLI Session.
	
	
	Ubuntu 18.04.1 LTS kb2018 ttyS1
	
	kb2018 login: 
	
If the session is preoccupied use the following (stop /system1/oemhp_vsp1)
	
	steve:~ don$ ssh -p 22222 feurig@vpn.suspectdevices.com
	User:feurig logged-in to kb2018.suspectdevices.com(192.168.31.119 / FE80::9E8E:99FF:FE0C:BAD8)
	iLO 3 Advanced for BladeSystem 1.88 at  Jul 13 2016
	Server Name: kb2018
	Server Power: On
	
	</>hpiLO-> vsp
	...
	Virtual Serial Port is currently in use by another session.
	</>hpiLO-> stop /system1/oemhp_vsp1
	...
	</>hpiLO-> </>hpiLO-> vsp
	
	Virtual Serial Port Active: COM2
	
	
## fixing grub (identical to the process for idrac 6)
You need set the console to ttyS1 by adding a console=ttyS1,115200n8 to the end of the kernel line
	
	root@bs2020:~# nano /boot/grub/menu.list
	...
	kernel          /boot/vmlinuz-4.4.0-96-generic root=UUID=8cafbdf6-441e-4f76-b89c-017fc22253f9 ro console=hvc0 console=ttyS1,115200n8
	
Add the changes to /etc/default/grub so that it will survive updates to the kernel.
	
	root@bs2020:~# nano /etc/default/grub
	...
	GRUB_TERMINAL='serial console'
	GRUB_CMDLINE_LINUX="console=hvc0 console=ttyS1,115200n8"
	GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=1 --word=8 --parity=no --stop=1"
	root@bs2020:~# update-grub
	
Reboot the server and attach to the console.
[[Image(ILO3Notes:ILo3SerialBootScreen.png)]]
[[Image(ILO3Notes:ILO3SerialConsoleBootFinish.png)]]

## virtual serial port in action
In order to make the dl380 expose the disks we added required jumping into the raid controllers bios during boot and configuring it. This is documented [[wiki:CaptiveRaidController|here]]
### HP Documents
* [ILO3 Users Guide (https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c02774507)](https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c02774507)
* [ILO3 Scripting Guide (https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c02774508)](https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c02774508)
* [ILO3 Serial Port Guide (https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c00263709)](https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-c00263709)
* [ILO3 Security Brief (https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-a00026171en_us)](https://support.hpe.com/hpsc/doc/public/display?sp4ts.oid=5294355&docLocale=en_US&docId=emr_na-a00026171en_us)
### Link Dump
* [using the VSP features of the ilo3 to configure the raid controller (http://trac.suspectdevices.com/trac/wiki/CaptiveRaidController)](http://trac.suspectdevices.com/trac/wiki/CaptiveRaidController)
* [Using IPMI to configure ILO card  (http://dev-random.net/configuring-hp-ilo-through-linux-automatically/)](http://dev-random.net/configuring-hp-ilo-through-linux-automatically/)
* https://sysadmin.compxtreme.ro/access-hps-ilo-remote-console-via-ssh/
* [bonus link on how to kill outstanding connections (https://stivesso.blogspot.com/2012/02/hp-ilolinux-output-to-vsp-for-linux.html)](https://stivesso.blogspot.com/2012/02/hp-ilolinux-output-to-vsp-for-linux.html)