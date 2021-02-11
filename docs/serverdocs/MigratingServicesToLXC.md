<!-- MigratingServicesToLXC, Version: 1, Modified: 2018/12/02, Author: trac -->
#Migrating Services to LXD

Up until 31 Jan 2019 medea was still providing critical services to the network and to myself. None of these services are disentangled enough to move them quickly. Starting with the web/mail servers we first attempted to set up a container on Medea and Migrate that container to bs2020. Adding a bridge to a running server with 30 aliases wasn't exactly straightforward so the services are being built on containers on bs2020 and migrated, Starting with trac.

## osx-avr, suspectdevices.com, 3dangst, dns servers
### track server Apache, postgress, trac. (trac.suspecedevices.com/198.202.31.221)
This server could have been better documented but I needed it her to document everything else.
#### Install Notes
* Backed up old server according to https://trac.edgewall.org/wiki/TracBackup#RestoringaBackup
* installed everything from debian packages except for the wikiprint module which had to be manually installed. 
* Moved trac to /var/www/trac (default document root was /var/www/html may move it again.
*  path is hardcoded in cgi-bin/trac.wsgi
* The database file from hotcopy did not assign the database and tables to the trac_db_admin user. (manually fixed) 
* .egg-cache and plugins directories must be owned by www-data
*  replaced index.html with a redirect to /trac.
*  created dns entry for trac.suspectdevices.com
*  replaced apacheconfig on old server with Redirect
	
	Redirect permanent /project/todo http://trac.suspectdevices.com/trac
	
### Suspect devices wordpress blog
* create lxc container and install lamp server using tasksel.
	
	root@bs2020:~# lxc init local:ubuntults ian -p susdev
	Creating ian
	root@bs2020:~# lxc start ian
	root@bs2020:~# lxc exec ian bash
	... edit interfaces file and reboot or restart network services ...
	root@ian:~# apt-get install tasksel
	root@ian:~# tasksel
	... select lamp server ...
	... set password for mysql server ...
	

* Sort out the wordpress blog from the other legacy stuff.
	
	root@medea:/home/newcourse/suspectdevices/www# ls -ls
	total 9916
	   4 drwxr-xr-x  4 www-data www-data    4096 Nov 17  2015 art2013
	   4 drwxr-xr-x  6 www-data www-data    4096 Jan 13 09:42 blahg
	   4 drwxrwxr-x  2 www-data staff       4096 Oct 10  2011 blog
	5240 -rw-r--r--  1 www-data root     5365300 Jun 22  2012 cma.tgz
	   4 drwxr-xr-x  3 www-data www-data    4096 Aug 25  2012 CookingWithMapleBacon
	   4 drwxrwxr-x  2 www-data staff       4096 Jan 14  2012 css
	   4 drwxrwxr-x  2 www-data staff       4096 Mar  1  2012 data
	   4 drwxrwxr-x  2 www-data staff       4096 Feb 12  2013 demo
	   4 -rw-rw-r--  1 www-data staff        897 Nov 12  2011 dorkboard_gallery.html
	   8 -rw-rw-r--  1 www-data staff       4890 Jan 16  2012 dorkboard.html
	   4 drwxrwxrwx  2 www-data staff       4096 Jun 30  2013 drop
	   4 -rw-rw-r--  1 www-data staff       2970 Jun 22  2012 duce.html
	   0 -rw-rw-r--  1 www-data staff          0 Nov 12  2011 favicon.ico
	   4 drwxr-xr-x  2 www-data www-data    4096 Feb 11  2013 feedme
	   4 drwxrwxr-x  3 www-data staff       4096 Nov 12  2011 images
	   4 -rw-r--r--  1 www-data root          76 Jun 27  2012 index.php
	   4 drwxrwxr-x  3 www-data staff       4096 Nov 12  2011 js
	4432 -rw-r--r--  1 www-data root     4538093 Jun 22  2012 latest.tar.gz
	   4 drwxr-xr-x  2 www-data camo        4096 Jul 28  2012 library
	   4 -rw-rw-r--  1 www-data staff        819 Nov 12  2011 others.html
	   4 drwxr-xr-x 19 www-data don         4096 Nov  4  2014 PCFA
	   4 -rw-rw-r--  1 www-data staff        923 Oct 13  2011 pindex.php
	   4 drwxr-xr-x  2 www-data don         4096 Dec  9  2016 reference
	   4 drwxr-xr-x  2 www-data root        4096 Apr  8  2013 resumes
	   4 -rw-rw-r--  1 www-data staff       1371 Mar 13  2017 static.html
	   4 -rw-rw-r--  1 www-data staff       2599 Feb 26  2012 tad.html
	   4 drwxr-xr-x  3 www-data don         4096 Dec 19  2012 talks
	  28 -rw-rw-r--  1 www-data staff      27241 Jun 22  2011 temp_bg.png
	  68 -rw-rw-r--  1 www-data staff      68019 Jun 22  2011 temp_board.png
	  40 -rw-rw-r--  1 www-data staff      38110 Jun 22  2011 temp_logo.png
	   4 drwxr-xr-x  3 www-data www-data    4096 Jun 27  2012 TheBaco-matic5000-OSB
	   0 lrwxrwxrwx  1 www-data root           5 Feb 15  2013 wordpress -> blahg
	   4 -rw-rw-r--  1 www-data staff       3559 May 12  2012 workshops.html.old
	root@medea:/home/newcourse/suspectdevices/www# mkdir ../exodus
	root@medea:/home/newcourse/suspectdevices/www# cp -p *.html ../exodus
	root@medea:/home/newcourse/suspectdevices/www# cp -rpv talks/EpicMidiFail/ ../exodus
	...
	root@medea:/home/newcourse/suspectdevices/www# cp -rpv images ../exodus/
	...
	root@medea:/home/newcourse/suspectdevices/www# cp -rpv blahg ../exodus/
	...
	
	
* dump the database
	
	root@medea:/home/newcourse/suspectdevices/www# mysqldump -u www-data  -p  susdevweb> ../exodus/susdevweb.dump
	Enter password: 
	
* move and untar into /var/www/html
* restore database
	
	root@ian:/var/www# mysqladmin -p create susdevweb
	Enter password: 
	root@ian:/var/www/html/blahg# mysql -p susdevweb< exodus/susdevweb.dump
	Enter password: 
	root@ian:/var/www/html/blahg# mysql -p susdevweb
	Enter password: 
	...
	mysql> CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'somepassword';
	Query OK, 0 rows affected (0.00 sec)
	mysql> GRANT ALL PRIVILEGES ON * . * TO 'www-data'@'localhost';
	Query OK, 0 rows affected (0.00 sec)
	
	mysql> 
	
* adjust /etc/apache2/sites-enabled/000-default
	
	.... not really needed ....
	
* enable mod rewrite and .htaccess override.
	
	root@ian:~# nano /etc/apache2/apache2.conf 
	...
	<Directory /var/www/>
	        Options Indexes FollowSymLinks
	        AllowOverride All
	        Require all granted
	</Directory>
	...
	root@ian:~# cd /etc/apache2/mods-enabled/
	root@ian:/etc/apache2/mods-enabled# ln -s ../mods-available/rewrite.load .
	root@ian:/etc/apache2/mods-enabled# apachectl configtest
	Syntax OK
	root@ian:/etc/apache2/mods-enabled# apachectl restart
	
* route / to /blahg/ and check rewrite rules for wordpress site
	
	root@ian:~# nano /var/www/html/.htaccess 
	<IfModule mod_rewrite.c>
	RewriteEngine on
	RewriteRule   "^/$"  "/blahg/"  [R]
	</IfModule>
	
	root@ian:~# cat /var/www/html/blahg/.htaccess 
	<IfModule mod_rewrite.c>
	RewriteEngine On
	RewriteBase /blahg/
	RewriteRule ^index\.php$ - [L]
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule . /blahg/index.php [L]
	</IfModule>
	
	
## Static web server.
### busholini, Straight.fromhell.com, (with processing) osxavr.org

In order to mitigate the issues around CMS's such as wordpress, web sites whos primary purpose is to present photos and information that do not require dynamic content will be moved to a lighttpd server using named virtual hosts. Once this is tested it will be moved to 198.202.31.230 (formally www.suspectdevices.com) 

* create lts container and apt-get install lighttpd
* copy static content into directories under /var/www
* edit /etc/lighttpd/lighttpd.conf
	
	....
	# default server and configuration
	server.document-root        = "/var/www/busholini/www"
	server.upload-dirs          = ( "/var/cache/lighttpd/uploads" )
	server.errorlog             = "/var/log/lighttpd/error.log"
	server.pid-file             = "/var/run/lighttpd.pid"
	server.username             = "www-data"
	server.groupname            = "www-data"
	server.port                 = 80
	#
	# virtualhosts
	#
	
	$HTTP["host"] =~ "www.suspectdevices.com" {
	  url.redirect # ( "^/(.*)"> "http://blog.suspectdevices.com/$1" )
	}
	
	$HTTP["host"] =~ "(^|\.)digithink\.com$" {
	server.document-root = "/var/www/digithink/www"
	}
	$HTTP["host"] =~ "(^|\.)thesofttargets\.com$" {
	server.document-root = "/var/www/thesofttargets/www"
	}
	# disable php
	index-file.names            = ( "index.html", "index.lighttpd.html" )
	url.access-deny             = ( "~", ".inc", ".php" )
	
Note/todo: the redirects should be more specific
* ie /project/todo -> trac.suspectdevices.com
* ie /blahg/ -> blog.suspectdevices.com

## DNS/MAIL server (naomi)
### DNS
* consolidate active zone files and create single master.conf to be included by /etc/bind/named.conf.local
	
	//
	// Do any local configuration here
	//
	
	// Consider adding the 1918 zones here, if they are not used in your
	// organization
	include "/etc/bind/zones/master.conf";
	
	root@naomi:~# cat /etc/bind/zones/master.conf 
	zone "digithink.com" in {
	        type master;
	        file "/etc/bind/zones/digithink.hosts";
	};
	
	zone "fromhell.com" in {
	        type master;
	        file "/etc/bind/zones/fromhell.hosts";
	};
	
	zone "busholini.org" in {
	        type master;
	        file "/etc/bind/zones/busholini.hosts";
	};
	
	zone "3dangst.com" in {
	        type master;
	        file "/etc/bind/zones/3dangst.hosts";
	};
	
	zone "osx-avr.org" in {
	        type master;
	        file "/etc/bind/zones/osx-avr.hosts";
	};
	
	zone "suspectdevices.com" {
	        type master;
	        file "/etc/bind/zones/suspectdevices.hosts";
	};
	
	zone "thesofttargets.com" {
	        type master;
	        file "/etc/bind/zones/thesofttargets.hosts";
	};
	
	zone "bresgal.com" in {
	        type master;
	        file "/etc/bind/zones/bresgal.hosts";
	};
	
	zone "bresgal.org" in {
	        type master;
	        file "/etc/bind/zones/bresgal.hosts";
	};
	
	zone "bluegin.net" in {
	        type master;
	        file "/etc/bind/zones/bluegin.hosts";
	};
	
* check and restart bind
	
	root@naomi:~# named-checkconf /etc/bind/named.conf
	root@naomi:~# named-checkconf /etc/bind/named.conf
	root@naomi:~# service bind9 restart
	root@naomi:~# service bind9 status
	● bind9.service - BIND Domain Name Server
	   Loaded: loaded (/lib/systemd/system/bind9.service; enabled; vendor preset: enabled)
	  Drop-In: /run/systemd/generator/bind9.service.d
	           └─50-insserv.conf-$named.conf
	   Active: active (running) since Tue 2018-01-30 10:19:15 PST; 6s ago
	     Docs: man:named(8)
	  Process: 962 ExecStop=/usr/sbin/rndc stop (code=exited, status=0/SUCCESS)
	 Main PID: 965 (named)
	   CGroup: /system.slice/bind9.service
	           └─965 /usr/sbin/named -f -u bind
	
	Jan 30 10:19:15 naomi named[965]: zone bresgal.org/IN: sending notifies (serial 2009123000)
	Jan 30 10:19:15 naomi named[965]: zone suspectdevices.com/IN: sending notifies (serial 2018012902)
	Jan 30 10:19:15 naomi named[965]: zone 3dangst.com/IN: sending notifies (serial 2004072801)
	Jan 30 10:19:15 naomi named[965]: zone busholini.org/IN: sending notifies (serial 2018012201)
	Jan 30 10:19:15 naomi named[965]: zone osx-avr.org/IN: sending notifies (serial 2005032100)
	Jan 30 10:19:15 naomi named[965]: zone digithink.com/IN: sending notifies (serial 2018012200)
	Jan 30 10:19:15 naomi named[965]: zone fromhell.com/IN: sending notifies (serial 2004072000)
	Jan 30 10:19:15 naomi named[965]: zone bluegin.net/IN: sending notifies (serial 2004072500)
	Jan 30 10:19:15 naomi named[965]: zone thesofttargets.com/IN: sending notifies (serial 2018012200)
	Jan 30 10:19:15 naomi named[965]: zone bresgal.com/IN: sending notifies (serial 2009123000)
	
	
* install bind9 and email services via tasksel
* move dns1 ip from medea to naomi
* reboot servers.
### Mail
Based on the file dates of the Maildir's being updated by postfix on the old server..

* Look at existing server for active email users.

	
	root@medea:~# find / -name Maildir -a -newer www/postgres7JUL17.dump -print
	/var/www/Maildir
	/home/eldufe/Maildir
	/home/don/Maildir
	/home/fromhell/users/feurig/Maildir
	
We notice that only three users are reading email so we need to serve those users.

* So create users for feurig@fromhell.com, eldufe@busholini.org and don@suspectdevices.com since www is going to be exclusively spam.
	
	root@naomi:~# useradd -c "The Commander and Thief" -m eldufe
	root@naomi:~# useradd -c "D Delmar Davis" -m don
	
The rest of the documentation has been moved to a separate [wiki:UbuntuMailServerSetup mail server setup] document.

### Secondary DNS Server
* create server
* install dns using tasksel
* transfer and convert master configuration to slave.
	
	root@teddy:~# cd /etc/bind
	root@teddy:/etc/bind# mkdir zones
	root@teddy:/etc/bind# scp don@198.202.31.231:/etc/bind/zones/master.conf slave.conf
	The authenticity of host '198.202.31.231 (198.202.31.231)' can't be established.
	ECDSA key fingerprint is SHA256:WFKs+2xinTQKgPhIM6fjCy2FMpY4SbeYvM2lQZpifiI.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added '198.202.31.231' (ECDSA) to the list of known hosts.
	don@198.202.31.231's password: 
	master.conf                                                                            100%  983     1.0KB/s   00:00    
	root@teddy:/etc/bind# sed 's/master;/slave;\r\n\tmasters \{ 198.202.31.141; \};/' slave.conf >zones/slave.conf
	root@teddy:/etc/bind# nano named.conf.local 
	 
	// Do any local configuration here
	//
	
	// Consider adding the 1918 zones here, if they are not used in your
	// organization
	//include "/etc/bind/zones.rfc1918";
	include "/etc/bind/zones/slave.conf";
	
* deal with duplicate filename and slave configuration in bresgals....
	
	root@teddy:/etc/bind# named-checkconf 
	/etc/bind/zones/slave.conf:52: writeable file '/etc/bind/zones/bresgal.hosts': already in use: /etc/bind/zones/slave.conf:46
	root@teddy:/etc/bind# nano /etc/bind/zones/slave.conf
	....
	root@teddy:/etc/bind# service bind9 restart
	root@teddy:/etc/bind# service bind9 status
	● bind9.service - BIND Domain Name Server
	   Loaded: loaded (/lib/systemd/system/bind9.service; enabled; vendor preset: enabled)
	  Drop-In: /run/systemd/generator/bind9.service.d
	           └─50-insserv.conf-$named.conf
	   Active: active (running) since Wed 2018-01-31 22:17:00 PST; 5min ago
	     Docs: man:named(8)
	  Process: 5436 ExecStop=/usr/sbin/rndc stop (code=exited, status=1/FAILURE)
	 Main PID: 5450 (named)
	    Tasks: 27
	   Memory: 30.4M
	      CPU: 114ms
	   CGroup: /system.slice/bind9.service
	           └─5450 /usr/sbin/named -f -u bind
	
	Jan 31 22:17:01 teddy named[5450]: zone bluegin.net/IN: transferred serial 2004072500
	Jan 31 22:17:01 teddy named[5450]: transfer of 'bluegin.net/IN' from 198.202.31.141#53: Transfer status: success
	Jan 31 22:17:01 teddy named[5450]: transfer of 'bluegin.net/IN' from 198.202.31.141#53: Transfer completed: 1 messages,
	Jan 31 22:17:01 teddy named[5450]: zone bresgal.org/IN: transferred serial 2009123000
	Jan 31 22:17:01 teddy named[5450]: zone bluegin.net/IN: sending notifies (serial 2004072500)
	Jan 31 22:17:01 teddy named[5450]: transfer of 'bresgal.org/IN' from 198.202.31.141#53: Transfer status: success
	Jan 31 22:17:01 teddy named[5450]: transfer of 'bresgal.org/IN' from 198.202.31.141#53: Transfer completed: 1 messages,
	Jan 31 22:17:01 teddy named[5450]: zone bresgal.org/IN: sending notifies (serial 2009123000)
	Jan 31 22:17:01 teddy named[5450]: dumping master file: /etc/bind/zones/tmp-qGurg6XtTG: open: permission denied
	Jan 31 22:17:01 teddy named[5450]: dumping master file: /etc/bind/zones/tmp-jUyE6xKRDk: open: permission denied
	
* Move zone files to /var/lib/bind/ because apparmor won't let you write to /etc/bind/zones...
	
	root@teddy:~# sed -i 's/etc\/bind\/zones/var\/lib\/bind/' /etc/bind/zones/slave.conf 
	root@teddy:~# service bind9 restart
	root@teddy:~# tail /var/log/syslog
	Sep  8 13:48:56 teddy named[7118]: zone bresgal.com/IN: sending notifies (serial 2009123000)
	Sep  8 13:48:56 teddy named[7118]: transfer of 'bluegin.net/IN' from 198.202.31.141#53: connected using 198.202.31.132#45499
	Sep  8 13:48:56 teddy named[7118]: zone suspectdevices.com/IN: transferred serial 2018080300
	Sep  8 13:48:56 teddy named[7118]: transfer of 'suspectdevices.com/IN' from 198.202.31.141#53: Transfer status: success
	Sep  8 13:48:56 teddy named[7118]: transfer of 'suspectdevices.com/IN' from 198.202.31.141#53: Transfer completed: 1 messages, 32 records, 1228 bytes, 0.001 secs (1228000 bytes/sec)
	Sep  8 13:48:56 teddy named[7118]: zone suspectdevices.com/IN: sending notifies (serial 2018080300)
	Sep  8 13:48:56 teddy named[7118]: zone bluegin.net/IN: transferred serial 2004072500
	Sep  8 13:48:56 teddy named[7118]: transfer of 'bluegin.net/IN' from 198.202.31.141#53: Transfer status: success
	Sep  8 13:48:56 teddy named[7118]: transfer of 'bluegin.net/IN' from 198.202.31.141#53: Transfer completed: 1 messages, 18 records, 450 bytes, 0.001 secs (450000 bytes/sec)
	Sep  8 13:48:56 teddy named[7118]: zone bluegin.net/IN: sending notifies (serial 2004072500)
	root@teddy:~# ls /var/lib/bind/
	3dangst.hosts         bluegin.hosts   bresgal1.hosts   digithink.hosts  osx-avr.hosts         thesofttargets.hosts
	bind9-default.md5sum  bresgal0.hosts  busholini.hosts  fromhell.hosts   suspectdevices.hosts
	root@teddy:~# 
	

## Sidenote: 17.10/18.04 container
While we were running up new containers we started the process of looking at the changes coming down the road (next LTS candidate) [BleedingEdgeServer Phillip] is our current exploration into what the kids are up to.

* BleedingEdgeServer


## Linkdump
* https://stackoverflow.com/questions/33377916/migrating-lxc-to-lxd
* https://bobcares.com/blog/wordpress-hosting-using-lxd-lxc-server-virtualization-solution/3/
* https://wparena.com/how-to-move-a-wordpress-site-from-one-server-to-another/
* https://www.quora.com/How-do-you-export-a-WordPress-site-to-a-static-HTML-i-e-how-do-you-remove-all-WordPress-functionality-from-a-WordPress-theme-to-turn-it-into-a-plain-HTML-theme-and-are-there-any-%E2%80%98export-as-HTML%E2%80%99-type-features-available
* https://stackoverflow.com/questions/17468109/postfix-unable-to-find-etc-postfix-virtual-file
* https://wordpress.org/plugins/simply-static/
* https://wordpress.org/plugins/static-html-output-plugin/
* https://zargony.com/2008/02/04/migrating-from-apache-to-lighttpd-with-name-based-virtual-hosts-and-ssl/
* https://help.ubuntu.com/community/MailServer
* https://help.ubuntu.com/community/Dovecot
* https://help.ubuntu.com/community/Postfix
* https://help.ubuntu.com/lts/serverguide/postfix.html
* https://linoxide.com/ubuntu-how-to/setup-postfix-dovecot-mysql-ubuntu-1604/
* https://www.tecmint.com/setup-postfix-mail-server-in-ubuntu-debian/
* https://www.linuxbabe.com/mail-server/secure-email-server-ubuntu-16-04-postfix-dovecot
* https://skrilnetz.net/setup-your-own-mailserver/
* https://askubuntu.com/questions/54960/how-do-i-set-up-an-email-server#55027
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-on-ubuntu-16-04
* http://www.postfix.org/COMPATIBILITY_README.html
* https://unix.stackexchange.com/questions/145771/mail-filtering-with-procmail-in-a-postfix-dovecot-system-with-virtual-users 
* https://www.exratione.com/2016/05/a-mailserver-on-ubuntu-16-04-postfix-dovecot-mysql/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-16-04
* http://www.postfix.org/STANDARD_CONFIGURATION_README.html#null_client
* https://askubuntu.com/questions/967091/zpool-degrades-when-plugging-in-a-drive