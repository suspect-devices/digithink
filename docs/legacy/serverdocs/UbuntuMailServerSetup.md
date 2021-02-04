# Ubuntu LTS Email Server Setup
This document assumes that you have set up a debian 9 or ubuntu LTS server(/container) set up and that postfix/email has been set up using tasksel. 

## Dovecot (imap server) and Postfix (mail server)

configure dovecot to use self signed ssl cert created by postfix.
	
	root@naomi:/etc/postfix# cd ../dovecot/conf.d/
	root@naomi:/etc/dovecot/conf.d# nano 10-ssl.conf 
	##
	## SSL settings
	##
	
	# SSL/TLS support: yes, no, required. <doc/wiki/SSL.txt>
	ssl = yes
	
	# PEM encoded X.509 SSL/TLS certificate and private key. They're opened before
	# dropping root privileges, so keep the key file unreadable by anyone but
	# root. Included doc/mkcert.sh can be used to easily generate self-signed
	# certificate, just make sure to update the domains in dovecot-openssl.cnf
	ssl_cert = </etc/ssl/certs/ssl-cert-snakeoil.pem
	ssl_key = </etc/ssl/private/ssl-cert-snakeoil.key
	#ssl_cert = </etc/dovecot/dovecot.pem
	#ssl_key = </etc/dovecot/private/dovecot.pem
	
Also set mailbox format to Maildir or all of your legacy data will be hosed.
	
	
	root@naomi:/etc/dovecot/conf.d# nano 10-mail.conf
	  mail_location = maildir:~/Maildir
	...
	
Notice issues with sending mail using ssl/tls
	
	don@bob2:~$ openssl s_client -connect mail.suspectdevices.com:465 -starttls smtp
	connect: Connection refused
	connect:errno=111
	
Add ssl/tls to postfix for outgoing mail
	
	
	root@naomi:/etc/postfix# nano master.cf
	...
	# ==========================================================================
	# service type  private unpriv  chroot  wakeup  maxproc command + args
	#               (yes)   (yes)   (no)    (never) (100)
	# ==========================================================================
	smtp      inet  n       -       y       -       -       smtpd
	#smtp      inet  n       -       y       -       1       postscreen
	#smtpd     pass  -       -       y       -       -       smtpd
	#dnsblog   unix  -       -       y       -       0       dnsblog
	#tlsproxy  unix  -       -       y       -       0       tlsproxy
	submission inet n       -       y       -       -       smtpd
	  -o syslog_name=postfix/submission
	  -o smtpd_tls_security_level=encrypt
	  -o smtpd_sasl_auth_enable=yes
	#  -o smtpd_reject_unlisted_recipient=no
	#  -o smtpd_client_restrictions=$mua_client_restrictions
	#  -o smtpd_helo_restrictions=$mua_helo_restrictions
	#  -o smtpd_sender_restrictions=$mua_sender_restrictions
	#  -o smtpd_recipient_restrictions=
	  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
	  -o milter_macro_daemon_name=ORIGINATING
	root@naomi:/etc/postfix# service postfix check
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./sbin/lmtp
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./libpostfix-tls.so.1
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./libpostfix-global.so.1
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./libpostfix-master.so.1
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./libpostfix-dns.so.1
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/./libpostfix-util.so.1
	postfix/postfix-script: warning: group or other writable: /usr/lib/postfix/sbin/./lmtp
	root@naomi:/etc/postfix# service postfix reload
	
	
Link authentication to dovecot and enable auth server in dovecot.  '' apparently this can be avoided by installing a single package buried in ubuntu's documentation (g: Mail-Stack Delivery).
	
	root@naomi:/etc/postfix# nano /etc/dovecot/conf.d/10-master.conf 
	...
	  #Postfix smtp-auth
	  unix_listener /var/spool/postfix/private/auth {
	    mode = 0666
	  }
	
	  # Auth process is run as this user.
	  #user = $default_internal_user
	}
	
	service auth-worker {
	  # Auth worker process is run as root by default, so that it can access
	  # /etc/shadow. If this isn't necessary, the user should be changed to
	  # $default_internal_user.
	  user = root
	}
	...
	
	root@naomi:/etc/postfix# nano main.cf
	# TLS parameters
	smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
	smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
	smtpd_use_tls=yes
	smtpd_tls_auth_only = yes
	smtpd_sasl_type = dovecot
	smtpd_sasl_path = private/auth
	smtpd_sasl_auth_enable = yes
	smtpd_recipient_restrictions = permit_sasl_authenticated permit_mynetworks reject_unauth_destination
	
	
Follow up on above errors
  
   NOTE: the above errors are related to symlinks and not the files. Both debian and canonical aren't concerned about it and may or may not fix it at some point. https://bugs.launchpad.net/ubuntu/+source/postfix/+bug/1728723

eliminate pop3 as it isn't needed
	
	mv /usr/share/dovecot/protocols.d/pop3d.protocol /usr/share/dovecot/pop3d.protocol.disabled
	service dovecot reload
	netstat -ta
	
## SPF and openDKIM
Gmail currently requires that any email you send that isn't controlled by them use both SPF and DKIM. 
### What the hell is it?
According to linuxbabe https://www.linuxbabe.com/mail-server/setting-up-dkim-and-spf

  _SPF and DKIM are two types of TXT records in DNS that can help prevent email spoofing and ensure legitimate emails are delivered into the recipient’s inbox instead of spam folder. If your domain is abused by email spoofing, then your emails are likely to landed in recipient’s spam folder if they didn’t add you in address book._

 _SPF (Sender Policy Framework) record specifies which hosts or IP addresses are allowed to send emails on behalf of a domain. You should allow only your own email server or your ISP’s server to send emails for your domain._

 _DKIM (DomainKeys Identified Mail) uses a private key to add a signature to emails sent from your domain. Receiving SMTP servers verify the signature by using the corresponding public key, which is published in your DNS manager. _

### SPF
 We only want to send email through a single server which is accomplished with the following record. Which needs to be added for each domain using the email server.
	
	root@naomi:~# nano /etc/bind/zones/fromhell.hosts 
	... add the following ...
	@ TXT "v=spf1 ip4:198.202.31.141 -all"
	
### openDKIM
#### gotchas
* convoluted and complex configuration involving 3 major services (dns,postfix,opendkim).
* postfix is chrooted and milter version is currently 6
* sample output from current opendkim-tools is wrong and requires manual correction.
* Relaying requires masquerading.
#### installation

Install opendkim and edit configuration file
	
	root@naomi:~# apt-get install opendkim opendkim-tools
	root@naomi:~# nano /etc/opendkim.conf 
	... add/correct the following ...
	Socket			local:/var/spool/postfix/var/run/opendkim/opendkim.sock
	PidFile               /var/run/opendkim/opendkim.pid
	Syslog          yes
	UMask           002
	UserID          opendkim
	KeyTable            refile:/etc/opendkim/key.table
	SigningTable        refile:/etc/opendkim/signing.table
	ExternalIgnoreList  refile:/etc/opendkim/trusted.hosts
	InternalHosts       refile:/etc/opendkim/trusted.hosts
	
For each domain being handled create a signing key and add to dns zone files.
	
	root@naomi:~# cd /etc/opendkim/keys/
	root@naomi:/etc/opendkim/keys# opendkim-genkey -b 2048 -h rsa-sha256 -r -s 201807 -d suspectdevices.com -v
	root@naomi:/etc/opendkim/keys# mv 201807.private suspectdevices.private
	root@naomi:/etc/opendkim/keys# cat 201807.txt >>/etc/bind/zones/suspectdevices.hosts 
	
Fix the error in dns entry and increment the zones serial number
	
	root@naomi:/etc/opendkim/keys# nano /etc/bind/zones/suspectdevices.hosts 
	@               IN      SOA  dns1.digithink.com. don.digithink.com (
	                2018072200 10800 3600 3600000 86400 )
	...change.this. YYYYMMDDxx  ....
	...
	... and change h=rsa-sha256 to h=sha256 ...      ...as below...
	201807._domainkey       IN      TXT     ( "v=DKIM1; h=sha256; k=rsa; s=email; "
	          "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6ymvRll+pEDThA6fMersYbr6dB5HKIFl4SMSF3ORxkFmrYC//wm6/vrqWNft3AWy4zC7AQNiKyQGg7$
	          "BUpxeL2bSGUhMrcZ+OheWWzw7aF746IOYO0IR4oMTFNP9a6hrmwBrLmnA8ploFYUWCa2ETq/VYP6i14LU7P/yi8JhDMu4ZVI6ytlynBcLU42orcNWjWNLHqy/F3L$
	
Reload bind and check key
	
	root@naomi:/etc/opendkim/keys# service bind9 reload
	root@naomi:/etc/opendkim/keys# service bind9 status
	● bind9.service - BIND Domain Name Server
	   Loaded: loaded (/lib/systemd/system/bind9.service; enabled; vendor preset: enabled)
	....
	Jul 25 22:35:15 naomi named[28512]: reloading zones succeeded
	....
	root@naomi:/etc/opendkim/keys# opendkim-testkey -d suspectdevices.com  -s 201807 -vvv
	opendkim-testkey: using default configfile /etc/opendkim.conf
	opendkim-testkey: checking key '201807._domainkey.suspectdevices.com'
	opendkim-testkey: key not secure .... ignore this ....
	opendkim-testkey: key OK
	
Add entries to key.table signing.table and trusted hosts.

```	
	root@naomi:/etc/opendkim# nano key.table 
	fromhell     fromhell.com:201807:/etc/opendkim/keys/fromhell.private
	suspectdevices suspectdevices.com:201807:/etc/opendkim/keys/suspectdevices.private
	root@naomi:/etc/opendkim# nano signing.table 
*@fromhell.com fromhell
*@suspectdevices.com suspectdevices
	root@naomi:/etc/opendkim# nano trusted.hosts 
	127.0.0.1
	::1
	198.202.31.221
	198.202.31.242
	localhost
*.fromhell.com
*.suspectdevices.com
```
	
Configure socket file to communicate with postfix and add postfix to opendkim group. 

	root@naomi:~# mkdir -p /var/spool/postfix/var/run/opendkim
	root@naomi:~# chown -R opendkim:opendkim /var/spool/postfix/var/run/opendkim
	root@naomi:~# touch /var/spool/postfix/var/run/opendkim/opendkim.sock
	root@naomi:~# chmod 775 /var/spool/postfix/var/run/opendkim/opendkim.sock
	root@naomi:~# usermod -a -G opendkim postfix
	root@naomi:~# nano /etc/default/opendkim 
	...
	DAEMON_OPTS="-vvvv"
	SOCKET="local:/var/spool/postfix/var/run/opendkim/opendkim.sock"
	RUNDIR=/var/spool/postfix/var/run/opendkim
	USER=opendkim
	GROUP=opendkim
	PIDFILE=$RUNDIR/$NAME.pid
	EXTRAAFTER=
	...
	
Add filter to postfix and restart both services.
	
	root@naomi:~# nano /etc/postfix/main.cf
	...
	milter_protocol = 6
	milter_default_action = accept
	smtpd_milters = unix:/var/run/opendkim/opendkim.sock
	non_smtpd_milters = unix:/var/run/opendkim/opendkim.sock
	...
	root@naomi:~# service opendkim reload
	root@naomi:~# service postfix reload
	
Send test mail 
	
	root@naomi:~# echo "dkim test" |mail -testopendkim  check-auth@verifier.port25.com
	
#### adding signatures to relayed hosts
To relay mail from other hosts on the local networks requires the following additions to postfix's main.cf
	
	root@naomi:~# nano /etc/postfix/main.cf
	...
	mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128, 198.202.31.128/25
	...
	masquerade_domains = suspectdevices.com, fromhell.com
	
#### openDKIM/SPF links

* https://www.cioby.ro/2013/11/14/configuring-opendkim-to-sign-postfix-emails/
* https://linuxaria.com/howto/using-opendkim-to-sign-postfix-mails-on-debian
* http://www.openspf.org/SPF_Record_Syntax
* https://blog.whabash.com/posts/send-outbound-email-postfix-dkim-spf-ubuntu-16-04
* https://www.linode.com/docs/email/postfix/configure-spf-and-dkim-in-postfix-on-debian-8/
* https://www.linuxbabe.com/mail-server/setting-up-dkim-and-spf
* https://tools.ietf.org/html/rfc6376
* https://tweenpath.net/opendkim-postfix-smtp-relay-server-on-debian-7/
* https://qureshi.me/how-to-setup-postfixdkimspfdmarc-on-ubuntu-plesk-onyx/

## Configure root/notification mail from other systems (esp bs2020)
Systems need to be able send email to notify us of issues such as security updates (apticron) etc. 
In order for email to be signed by opendkim and validated by spf the email needs to strip the hostname from mail sent from it before being relayed through the mail server. 
	
	root@bs2020:~# apt-get install mailutils apticron
	... select satellite server when asked ...
	root@bs2020:~# nano /etc/postfix/main.cf
	... add the following ...
	relayhost = naomi.suspectdevices.com
	compatibility_level=2
	masquerade_domains = suspectdevices.com
	
Since all systems will be striped of their machine names insure the full name of common accounts is made to be uniq
	
	root@bs2020:~# chfn -f "Root at BS2020"
	
* http://www.postfix.org/STANDARD_CONFIGURATION_README.html
* https://www.tecmint.com/setup-postfix-mail-server-smtp-using-null-client-on-centos/
_Todo:_
* I think postfix is a little heavy handed to run a null client. Investigate simpler secure solution.
* add amivis,and other filters linked in at https://help.ubuntu.com/community/MailServer
* make procmail do some work since its enabled by default
* make damned sure that it wont accept mail from the entire c-block