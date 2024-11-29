<!-- LetsEncryptCertificates, Version: 2, Modified: 2020/11/02, Author: feurig -->
# Lets Encrypt Certificates

Recently a recruiter was unable to see my blog because the certificate was self signed.
So I fixed the certificate on the blog and servrerdocs with one of the EFF sponsored certs from LetsEncrypt.
You can install certbot using the snap recommended by their docs or you can just 
	 
```
apt-get install certbot 
```
Once its d
one you need to open 2 terminals on the target machine.
In the first one you need to make whatever adjustments to your server to serve the url  !http://myserver.mydomain.whatever/.well-known/acme-challenge/xxxx
At which point you can run certbot and create your cert. 
```
root@herbert:/var/www/html# certbot certonly --manual
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): don@suspectdevices.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: A

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y
Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c'
to cancel): serverdocs.suspectdevices.com
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for serverdocs.suspectdevices.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOTE: The IP of this machine will be publicly logged as having requested this
certificate. If you're running certbot in manual mode on a machine that is not
your server, please ensure you're okay with that.

Are you OK with your IP being logged?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Create a file containing just this data:

_bbuZOGf0JHOqF1F1lEAGe9s-e9b3IUyq6ClUUAg7xA.bvfoagN5gvQVzT-7dZuyvhNibIYAUGx3MBNp0YLFo_g

And make it available on your web server at this URL:

http://serverdocs.suspectdevices.com/.well-known/acme-challenge/_bbuZOGf0JHOqF1F1lEAGe9s-e9b3IUyq6ClUUAg7xA

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
	- Congratulations! Your certificate and chain have been saved at:
	/etc/letsencrypt/live/serverdocs.suspectdevices.com/fullchain.pem
	Your key file has been saved at:
	/etc/letsencrypt/live/serverdocs.suspectdevices.com/privkey.pem
	Your cert will expire on 2021-02-01. To obtain a new or tweaked
	version of this certificate in the future, simply run certbot
	again. To non-interactively renew *all* of your certificates, run
	"certbot renew"
	- Your account credentials have been saved in your Certbot
	configuration directory at /etc/letsencrypt. You should make a
	secure backup of this folder now. This configuration directory will
	also contain certificates and private keys obtained by Certbot so
	making regular backups of this folder is ideal.
	- If you like Certbot, please consider supporting our work by:

	Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
	Donating to EFF:                    https://eff.org/donate-le

	- We were unable to subscribe you the EFF mailing list because your
	e-mail address appears to be invalid. You can try again later by
	visiting https://act.eff.org.


```
* https://www.ssllabs.com/ssltest/analyze.html?d=blog.suspectdevices.com