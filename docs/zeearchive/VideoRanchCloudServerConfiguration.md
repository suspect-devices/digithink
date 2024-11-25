<!-- VideoRanchCloudServerConfiguration, Version: 1, Modified: 2018/12/02, Author: trac -->
### Videoranch Cloud Server Configuration.
The purpose of this document is provide information on how gihon.orgs cloud server is currently configured and basic guidelines for maintaining it.

|# Date|# Author|# Email|# Comments|
|------|--------|-------|----------|
|28MAY16|Donald Delmar Davis|don@suspectdevices.com|Initial document|
### Background
We were asked to  convert a 15 year old internet server running freebsd to the cloud. We started by setting up a staging server running Ubuntu 14.04 and migrating the users data and log files from the old server. This provided a backup of the original data and a place where we could work without having to pay for disk or bandwidth before deploying the final product. After a long process of porting all of the users and web sites that the server had served over the decades we began identifying which services, users, and domains were needed on the server. Given a much smaller set of users and web sites that were actually needed, we deployed an AWS image based on the AMI provided by the commercial entity which maintains Ubuntu. The active users users and web content have been installed on this server and the remainder has been archived to an external disk.

## The Base Image

We chose to deploy an image provided by Canonical  specifically for AWS "ubuntu-trusty-14.04-amd64-server-20150325 (ami-5189a661)"
http://cloud-images.ubuntu.com/releases/trusty/release-20150325/

### Adjustments to the image
The ubuntu user which provides a back door through which AWS allows users that it has authenticated to have root access to the instance. Unfortunately the ubuntu UID(1000) was already taken (jess) so it was moved to 999 and files owned by it were migrated as well.

	
	chown --from=1000:1000 999:999 /. -Rv
	

Also the mail spool was somewhere new (/var/spool/mail) so I linked the new location back to /var/mail

### Additions to the image

a lamp stack was added to the image using the "tasksel" package which bundles most services into supported configurations and deploys them along with all of their dependencies. (Note that the Ubuntu Cloud Image was already installed)
	
	# tasksel
	Package configuration                                                                                                        
	                                                                                                                             
	               ┌─────────────┤ Software selection ├───────────   ───────┐               
	               │ You can choose to install one or more of the following predefined collections of software.  │               
	               │                                                                                                                                                      │               
	               │ Choose software to install:                                             
	               │                                                                                       
	               │    [*] Basic Ubuntu server                                                        
	               │    [*] OpenSSH server                                                            
	               │    [ ] DNS server                                                            
	               │    [*] LAMP server                                                                 
	               │    [*] Mail server                                                                 
	               │    [*] PostgreSQL database                                                 
	               │    [ ] Print server                                                                    
	               │    [ ] Samba file server                                                        
	               │    [ ] Tomcat Java server                                                   
	               │    [*] Ubuntu Cloud Image (instance)                                 
	               │    [ ] Virtual Machine host                                                     
	       ...                                                                        
	               │                                           <Ok>                                              │               
	               │                                                                                             │               
	               └─────────────────────────────────────┘               
	                                                                                                                             
	                                                                                                                             
	

### users and superusers

The following users were added to the system. 

	
	jess:x:1000:1000:Jessica Kent:/home/jess:/bin/csh
	gepr:x:1053:1053:Glen E Ropella:/home/gepr:/bin/bash
	don:x:1054:1054:Donald Delmar Davis:/home/don:/bin/bash
	vic:x:1002:1002:Victoria Kennedy:/home/vic:/bin/bash
	nez:x:1003:1003:Michael Nesmith:/home/nez:/bin/bash
	vranch:x:1004:1004:Videoranch User:/home/vranch:/bin/bash
	foreman:x:1005:1005:Videoranch Foreman:/home/foreman:/bin/tcsh
	navajoslim:x:1007:1007:Navajo Slim:/home/navajoslim:/bin/bash
	gihon:x:1017:1017:Gihon Foundation:/home/gihon:/bin/bash
	vk:x:1021:1021:Victoria Kennedy:/home/vk:/bin/bash
	vrresume:x:1024:1024:videoranch resume:/home/vrresume:/bin/bash
	vak:x:1027:1027:victoria kennedy:/home/vak:/bin/tcsh
	nezrays:x:1031:1031:nezrays:/usr/home/vranch/nezrays/www:/bin/sh
	vr3d:x:1035:1035:VR3D:/home/vr3d:/bin/sh
	staging:x:1041:1041:staging:/home/staging:/bin/bash
	nesmith:x:1042:1042:nesmith:/home/nesmith:/bin/bash
	director:x:1045:1045:Jessica Kent:/home/director:/bin/bash
	petetest:x:1048:1048:petetest:/home/petetest:/bin/bash
	mn:x:1022:1022:Michael Nesmith:/home/mn:/bin/bash
	
This had to be done manually as some of the origional passwords were so old that their encryption methods were no longer supported. In cases where the users were less than a few years old the users passwords transferred to the new system seamlessly. In other cases the passwords will have to be reset by someone with root access.   
	
	ubuntu@cloud # passwd vranch
	

Their mail spools (/var/mail/<usr>), and home directories were copied over as well.

sudo privileges were enabled for members of the sudo group.
	
	ubuntu@cloud # vigr
	...
	sudo:x:27:ubuntu,jess,foreman,don,gepr
	...
	

## Apache Configuration

In addition to the home directories of the remaining users the /home/vranch directory tree and /home/gihon were copied to the new server. The server configurations were ported to be as close to the originals as possible. (exceptions noted below)


The default server is set to www.gihon.com and is configured based on the original virtual-host. The php information and much about the apache server can be queried directly at http://videoranch.com/test.php
	
	#ServerName www.gihon.com
	<VirtualHost *:80>
	    ServerName www.gihon.com
	    ServerAlias gihon.com www.gihon.org gihon.org cloud.gihon.com
	    ServerAdmin info@digitaloffspring.com
	    DocumentRoot /home/gihon/www
	    <Directory '/home/gihon'>
	        AllowOverride All
	    </Directory>
	    ScriptAlias /cgi-bin/ /home/gihon/cgi-bin
	    CustomLog /home/gihon/logs/gihon-access_log common
	    ErrorLog /home/gihon/logs/gihon-error_log
	</VirtualHost>
	

* Note that the log files are left in user space (off of /home) this allows clients to pull and view the log files in the same way that they update the content of their web site (ftp etc)
* Some configuration directives are no longer supported and are commented out.
* Extremely dangerous statements such as AllowOverides for the root directory were modified.

All other servers are named virtualhosts. The first of which is www.videoranch.com defined in 
/etc/apache2/sites-enabled/www.videoranch.com.conf 
	
	<VirtualHost *:80>
	        ServerName www.videoranch.com
	        ServerAlias videoranch.com www.videoranch.com
	#       Header append p3p 'CP=\"OTI DSP COR CUR UNI\" polyref=\"/w3c/p3policy.xml\"'
	        ServerAdmin info@digitaloffspring.com
	        DocumentRoot /home/vranch/videoranch/www
	        ScriptAlias /cgi-bin/ /home/vranch/videoranch3d/cgi-bin/
	        ErrorLog /home/vranch/logs/www.videoranch.com-error_log
	        CustomLog /home/vranch/logs/www.videoranch.com-access_log common
	        <Directory /home/vranch/videoranch/www>
	                Options Indexes FollowSymLinks
	                AllowOverride All
	        </Directory>
	</VirtualHost>
	

## Pro-ftpd Configuration

We configured proftpd (which we vetted as a viable and secure ftp daemon) as closely as possible to the original configuration on the old server. Because AWS instances are in their own private network and access has to be explicitly allowed you must specify the PASV ports in /etc/proftpd/proftpd.conf. These ports must be opened up in the "Security Group" configuration as well. 
	
	# In some cases you have to specify passive ports range to by-pass
	# firewall limitations. Ephemeral ports can be used for that, but
	# feel free to use a more narrow range.
	PassivePorts                  49152 49153
	

Ftp in its native form is insecure and so we would prefer to have configured an SSL certificate and require TLS for all ftp requests. We were able to verify that SFTP (ftp provided by ssh).

## Network and "Security Group" configuration

The AWS instance is placed in a private network. This network provides the instance a private ip through dhcp. For this reason the main interface is configured as follows in /etc/networks/interfaces.d/eth0

	
	# The primary network interface
	auto eth0
	iface eth0 inet dhcp
	

This address is attached to the outside world via an "Elastic" ip (52.34.143.142). To connect the external traffic to the private address you have to create a "Security group" and define the rules which allow traffic in and out of the private network.

* INBOUND RULES * ||
|# protocol|# family|# port|# allow from|
|----------|--------|------|------------|
| HTTP | TCP | 80 | 0.0.0.0/0 |
| SSH | TCP | 22 | 0.0.0.0/0 |
| SMTP | TCP | 25 | 0.0.0.0/0 |
| Custom TCP Rule | TCP | 20 - 21 | 0.0.0.0/0 |
| IMAP | TCP | 143 | 0.0.0.0/0 |
| Custom TCP Rule | TCP | 49152 - 49153 | 0.0.0.0/0 |
| HTTPS | TCP | 443 | 0.0.0.0/0 |

Outbound rules allow all outgoing traffic.

## Unused Capabilities
### MySQL and PostgresSQL
While the M in LAMP is MySQL, Many developers prefer Postgres which is much more standards oriented and robust. Both databases are available and PHP is configured for them. At one point mysql was on the old server however neither gihon nor the model files served by videoranch.com seemed to use it. _ Note that if either database is used a mechanism to back up the data must also be implimented_

### Postfix and Dovecot
The standard SMTP (email) server for most current operating systems is Postfix. The Mail server task also includes Dovecot which provides both POP and IMAP servers for clients to download any mail still on the server. To use the pop server will require the addition of the ports for pop (110) to be added to the security group configuration. _These servers are not currently configured. _

## Log Rotation Configuration

On the previous server most log files were larger than the content being provided. Ubuntu provides a log rotation utility designed to compress and delete logs in a reasonable manner preventing them from consuming system resources over time. 
Since the apache logs on this system are in "user space" and not under /var/log/apache2 their location needed to be configured.


Here is the section added to /etc/logrotate.d/apache2 for the gihon.com

	
	/home/gihon/logs/*_log {
	        weekly
	        missingok
	        rotate 52
	        compress
	        delaycompress
	        notifempty
	        create 640 root adm
	        sharedscripts
	        postrotate
	                if /etc/init.d/apache2 status > /dev/null ; then \
	                    /etc/init.d/apache2 reload > /dev/null; \
	                fi;
	        endscript
	        prerotate
	                if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
	                        run-parts /etc/logrotate.d/httpd-prerotate; \
	                fi; \
	        endscript
	}
	

##  unattended upgrades (security only)

The system is configured to automatically install security upgrades as released by the operating system. _In the event that an error occurs mail is sent to the foreman account._

## Operations Guide

Given the state of the previous system the soundest approach is to automate as much of the systems upkeep as possible. Log rotation and unattended system upgrades along with other minor adjustments (turning on apt's auto-remove for instance) should enable us to think of the box more as an appliance.

### Backing up Server work with Live Snapshots

AWS allows a server to be backed up while running. These snapshots can be run up as separate servers (for development or to do a major release upgrade) Or they can be reattached to an existing instance (in the case of disaster or compromise).
Please make a snapshot of the server whenever significant work has been done to it.

### Backing up your data

Since the servers web content is in the user space. Log files, websites and other data served should be copied to a local server preferably one behind a firewall. *In particular Gihon should take care to keep updated copies of /home/gihon and /home/vranch* 


### Accessing the server

Privileged access can be granted through AWS to the Ubuntu user. For instructions on how to do this see http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html.  The server has been configured to allow ssh access directly. 

	
	$ ssh www.videoranch.com
	Welcome to Ubuntu 14.04.4 LTS (GNU/Linux 3.13.0-85-generic x86_64)
	
	 * Documentation:  https://help.ubuntu.com/
	
	  System information as of Mon Apr 11 18:12:10 UTC 2016
	
	  System load:  0.0                Processes:           139
	  Usage of /:   69.8% of 29.39GB   Users logged in:     1
	  Memory usage: 28%                IP address for eth0: 172.31.16.108
	  Swap usage:   0%
	
	  Graph this data and manage this system at:
	    https://landscape.canonical.com/
	
	  Get cloud support with Ubuntu Advantage Cloud Guest:
	    http://www.ubuntu.com/business/services/cloud
	
	0 packages can be updated.
	0 updates are security updates.
	
	
	You have new mail.
	Last login: Mon Apr 11 16:11:57 2016 from 71-34-91-188.ptld.qwest.net
	don@cloud:~$ 
	




### References


* why ubuntu? https://insights.ubuntu.com/2014/04/15/ubuntu-14-04-lts-the-cloud-platform-of-choice/
* https://www.digitalocean.com/community/tutorials/how-to-configure-logging-and-log-rotation-in-apache-on-an-ubuntu-vps
* https://help.ubuntu.com/lts/serverguide/automatic-updates.html
* https://anturis.com/linux-server-maintenance-checklist/