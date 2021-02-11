<!-- LedeRemoteSyslog, Version: 2, Modified: 2018/12/21, Author: feurig -->
# LEDE Remote Syslog

Sending router system logs to remote server using rsyslogEither 18.04 Server or the LXC snap has rsyslog installed. So getting syslog information from the admin firewall is pretty simple. Its possible that we may need to provide a server other than kb2018 to make this ideal however I wanted to make sure that the syslogs stayed on the admin lan.

## Sending logs to remote server
Modify the log configuration entries to point to the remote syslog and selecting a port and protocol is all that is needed.
	
	feurig@knight:~$ cat /etc/config/system 
	
	config system
		option hostname 'knight'
		option timezone 'PDT'
		option ttylogin '0'
		option log_size '64'
		option urandom_seed '0'
		option log_ip '192.168.31.159'
		option log_port '514'
		option log_proto 'udp'
	
	config timeserver 'ntp'
		option enabled '1'
		option enable_server '0'
		list server '0.lede.pool.ntp.org'
		list server '1.lede.pool.ntp.org'
		list server '2.lede.pool.ntp.org'
		list server '3.lede.pool.ntp.org'
	
Afterwords commit the configuration and restart the log daemon. 
	
	root@knight:/home/feurig# uci commit 
	root@knight:/home/feurig# /etc/init.d/log enable
	root@knight:/home/feurig# /etc/init.d/log restart
	
## Configuring rsyslogd on the remote server


Once you swim through the bagillian conflicting howtoo's for the multiple versions of rsyslogd you add the following lines to /etc/rsyslog.conf and restart it.

	
	root@kb2018:/var/log# nano /etc/rsyslog.conf 
	....
	# provides UDP syslog reception
	module(load="imudp")
	input(type="imudp" port="514")
	
	##Try exameple template for remote logs.
	$template RemoteLogs,"/var/log/%HOSTNAME%/%PROGRAMNAME%.log"
*.* ?RemoteLogs
	....
	root@kb2018:/var/log# service rsyslog restart
	
	

And test it.
	
	root@knight:/home/feurig# logger testlog meh
	
	
	root@kb2018:/var/log# tail /var/log/knight/
	dropbear.log  logread.log   root.log      sudo.log      
	root@kb2018:/var/log# tail /var/log/knight/dropbear.log 
	2018-12-21T18:50:54-08:00 knight dropbear[2465]: Exit (feurig): Keepalive timeout
	2018-12-21T19:44:31-08:00 knight dropbear[2524]: Child connection from 193.193.70.69:59547
	2018-12-21T19:44:31-08:00 knight dropbear[2524]: Exit before auth: Exited normally
	2018-12-21T20:02:11-08:00 knight dropbear[2541]: Child connection from 111.43.34.166:2323
	2018-12-21T20:02:12-08:00 knight dropbear[2541]: Exit before auth: Exited normally
	2018-12-21T21:22:01-08:00 knight dropbear[2598]: Child connection from 35.159.6.209:37640
	2018-12-21T21:22:13-08:00 knight dropbear[2598]: Login attempt for nonexistent user from 35.159.6.209:37640
	2018-12-21T21:22:14-08:00 knight dropbear[2598]: Exit before auth: Disconnect received
	2018-12-21T21:54:15-08:00 knight dropbear[2623]: Child connection from 97.115.132.190:59586
	2018-12-21T21:54:17-08:00 knight dropbear[2623]: Pubkey auth succeeded for 'feurig' with key sha1!! 2a:26:75:a7:ec:fe:92:f4:b5:64:2e:26:26:dd:12:e5:d5:68:4f:67 from 97.115.132.190:59586
	root@kb2018:/var/log# tail /var/log/knight/sudo.log 
	2018-12-21T18:35:42-08:00 knight sudo:   feurig : TTY=pts/0 ; PWD=/home/feurig ; USER=root ; COMMAND=/bin/ash
	2018-12-21T22:13:35-08:00 knight sudo:   feurig : TTY=pts/0 ; PWD=/home/feurig ; USER=root ; COMMAND=/sbin/uci commit
	root@kb2018:/var/log# tail /var/log/knight/root.log 
	2018-12-21T17:37:28-08:00 knight root: testLog “Blah1”
	2018-12-21T18:35:54-08:00 knight root: testlog meh
	root@kb2018:/var/log# 
	
	
### Link Dump
* https://forum.archive.openwrt.org/viewtopic.php?id=11912
* https://kuther.net/howtos/howto-log-firewall-openwrt-remote-rsyslog
* https://feeding.cloud.geek.nz/posts/debugging-openwrt-routers-by-shipping/
* https://www.rsyslog.com/storing-messages-from-a-remote-system-into-a-specific-file/
