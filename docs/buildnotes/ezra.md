# Klein -- Transfer of mail from naomi to ezra

Naomi was built on ubuntu close to a decade ago. It's a procmail / imap server with enough stuff to more or less survive as a self standing mail server in a very hostile world. Like freebsd its biggest problem is that it works and has suffered much neglect. It didnt survive do-release-upgrading from 22.04 to 24.04 and so it't time to migrate it to debian It's the last critical piece of my infrastructure still running a canonical based operating system.

I am following along with [this guide](https://www.wangzerui.com/2017/03/06/using-git-to-manage-system-configuration-files/) to transfer the existing mail server to git via a private bitbucket repository.

## The pieces

- postfix
- dovecot
- opendkim
- postgrey
- spf

### Additions

- certbot

## The Plan

- Create repository with all of the current configs in it
  - Make a "reference" copy branch with current configs in it.
  - Add a README.md a doc updating this process as we go.
    - copy / edit this readme for public consumption on digithink 
- Create a dns entry for the new server and make it the default MX for a domain you don't currently use for email (3dangst.com)
- Stand up a new mail server on Debian (trixie)
  - Install reference email server software and certbot
  - Add software based on --get-selections from current server
- Create a letsencrypt based ssl cert for the new server
- Create a "stock" branch and add all of the stuff installed by the software on the new server
  - push it
- pull the main branch down with all of the configs from the old server
- Modify the configurations updating them as needed
  - replace the self signed certs with those maintained by certbot
  - update and fix issues until we have a running base
- Test server using new user delmar@3dangst.com
- add remaining users (manually)
- scp home and mail spool directories (for rsync later)

## Work on the original server (naomi)

### Creating the config repository from the old server

```sh
git init
git config --global init.defaultBranch main
git config core.worktree "../../../"
git status
git add /etc/postfix
git add /etc/postgrey
git status
cat > /.gitignore <<EOD
/**
EOD
git add -f ../../etc/aliases
git add -f ../../etc/opendkim.conf ../../etc/opendkim
git add -f ../../etc/mail ../../etc/mail*
git add -f ../../etc/procmailrc ../../etc/dkimkeys
git status
git remote add origin git@bitbucket.org:suspectdevicesadmin/mailhost.git
git commit -a -m"naomi's config"
git branch -m master main
git push origin
git push --set-upstream origin main
dpkg --get-selections|grep mail
git add -f /etc/dovecot
git commit -a -m"don't forget dovecot"
git push
```

### Check installed packages on naomi
get all of the related packages installed on the reverence server you can feed this list to sed s/^/apt install/|sh or whatever.

```sh
dpkg --get-selections|grep mail|cut -f1|sed 's/^/apt install -y /'>/tmp/selections
dpkg --get-selections|grep post|cut -f1|sed 's/^/apt install -y /'>>/tmp/selections
dpkg --get-selections|grep dkim|cut -f1|sed 's/^/apt install -y /'>>/tmp/selections
dpkg --get-selections|grep dove|cut -f1|sed 's/^/apt install -y /'>>/tmp/selections
```

### Make the current main be the reference branch

```sh
git branch -m main reference
git push origin reference
git branch main
```

## DNS Changes

The reverse for our current mailserver claims to be mailhost.suspectdevices.com but is actually mailhost.\<CURRENTDOMAIN\>.com for now we are going to test on mailhost.suspectdevices.com and point the mx record for suspectdevices.com to mailhost.digithink.com.
I dunno. Will fix this later.

```sh
$TTL 600
@	IN	SOA  dns.digithink.com. don.digithink.com (
	2026070801 10800 3600 3600000 86400 )
	IN	NS	dns1.digithink.com.
	IN	NS	dns2.digithink.com.
	IN	NS	dns.digithink.com.
	IN	MX	5 mailhost.digithink.com
	IN	MX	10 mailhost.suspectdevices.com
	IN	HINFO	"UltraSparc" "Solaris"
	IN	A	69.41.138.105
$ORIGIN @

... other stuff ...
naomi       IN  A   69.41.138.102
ezra    	IN	A	69.41.138.110
mailhost	IN	CNAME	ezra
mail		IN	CNAME   ezra
... more stuff and dkim and spf records ...
```

## New server (ezra)

### Install container

### Install mail server and set up certificate

Break this out and explain it a bit. 
```
hostnamectl hostname mailhost.suspectdevices.com
apt install postfix postgrey dovecot-core dovecot-imapd opendkim
apt install -y certbot nginx python3-certbot-nginx
... fix the stupid default ipv6 entry ...
nano /etc/nginx/sites-enabled/default
apt install -y certbot nginx python3-certbot-nginx
... add servername to default config ...
nano /etc/nginx/sites-enabled/default
certbot run -a nginx --agree-tos --no-eff-email --staple-ocsp --email don@suspectdevices.com -d mailhost.suspectdevices.com
nano /etc/nginx/sites-enabled/default
systemctl start nginx
systemctl status nginx
opendkim-testkey -d suspectdevices.com  -s 201807 -vvv
apt install -y bsd-mailx
apt install -y libmail-spf-perl
apt install -y mailcap
apt install -y procmail
apt install -y postfix
apt install -y postfix-policyd-spf-perl
apt install -y postgrey
apt install -y libopendkim11:amd64
apt install -y opendkim
apt install -y opendkim-tools
apt install -y dovecot-core
apt install -y dovecot-imapd
apt install -y git
```

### Create stock branch and populate it with stock configuration 

```sh
git clone  --no-checkout git@bitbucket.org:suspectdevicesadmin/mailhost.git configs
cd configs
git config core.worktree "../../../"
git branch stock
cat > /.gitignore <<EOD
**
EOD
git add -f ../../etc/postfix
git add -f ../../etc/aliases
git add -f ../../etc/opendkim.conf ../../etc/opendkim
git add -f ../../etc/mail ../../etc/mail*
git add -f ../../etc/procmailrc ../../etc/dkimkeys
git add -f ../../etc/postgrey
git add -f ../../etc/dovecot
git status
git commit -a --author "D Delmar Davis <don@suspectdevices.com>" -m"stow stock configs in the stock branch"
git push origin stock

```

### Pull down the main branch.

```sh
git checkout main
git reset --hard origin/main
git pull
```

### Fix the new configs and add the new stuff.

YOU ARE HERE....

## References
- [https://www.wangzerui.com/2017/03/06/using-git-to-manage-system-configuration-files/](https://www.wangzerui.com/2017/03/06/using-git-to-manage-system-configuration-files/)
- [https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp](https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp)
- [http://www.postfix.org/STANDARD_CONFIGURATION_README.html](http://www.postfix.org/STANDARD_CONFIGURATION_README.html)
- [old mail server install docs](https://www.digithink.com/serverdocs/UbuntuMailServerSetup/)# 
