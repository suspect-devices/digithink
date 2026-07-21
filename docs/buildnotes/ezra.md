# Klein -- Transfer of mail from naomi to ezra

Dovecot 2.3 to Dovecot CE 2.4 Pain and suffering.

## TLDR

- Dovecot 2.4 has breaking changes
    - Configuration is different.
    - Community documentation ~~kind of~~ sucks.
        - In particular everything is defined but no examples are given 
- Default trixie install is a convoluted pile.
    - It's rubbish bin it. (remove/disable /etc/dovecot/conf.d/)
- use https://dovecot.org/upgrader/
    - on source server dovecot -n and copy results into upgrader
    - run convert and replace /etc/dovecot.conf with the results
    - update things such as ssl certs
- if your mail shows up wonky it probably needs:
    ```sh
    namespace inbox {
      ... other stuff ...
      prefix = .INBOX.
    }
    ```
- you may have to just do things the hard way. 

## Background

Naomi was built on ubuntu close to a decade ago. It's a procmail / imap server with enough stuff to more or less survive as a self standing mail server in a very hostile world. Like freebsd its biggest problem is that it works and has suffered much neglect. It didnt survive do-release-upgrading from 22.04 to 24.04 and so it's time to migrate it to debian It's the last critical piece of my infrastructure still running a canonical based operating system.

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
    - copy this readme to [document for public consumption on digithink](https://www.digithink.com/buildnotes/ezra/)
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
  - Fix any issues identified. 
- add remaining users (manually)
- shut down the old mail services
- copy home and mail spool directories (for rsync later)
- start the new server and test again.

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

The reverse for our current mailserver claims to be mailhost.suspectdevices.com is defined as mailhost.CURRENTDOMAIN.com for now we are going to test on mailhost.suspectdevices.com and point the mx record for all domains to that.
I dunno. Will fix this later.

```sh
$TTL 600
@	IN	SOA  dns.digithink.com. don.digithink.com (
	2026070801 10800 3600 3600000 86400 )
	IN	NS	dns1.digithink.com.
	IN	NS	dns2.digithink.com.
	IN	NS	dns.digithink.com.
	IN	MX	10 mailhost.suspectdevices.com.
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

```sh
incus init trixie -p default -p susdev25 ezra -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  eth0:
    addresses:
      - 69.41.138.110/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
EOF
)"
```

### Install mail server and set up certificate

Set up certbot to handle our mailhosts certificates

```sh
hostnamectl hostname mailhost.suspectdevices.com
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
```

Then install the mail server software following more or less the [fine instructions from linuxbabe.com](https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp)

```sh
apt install postfix postgrey dovecot-core dovecot-imapd opendkim
opendkim-testkey -d suspectdevices.com  -s 201807 -vvv
```

Then adjust the install based on the software installed on the old server.

```sh
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

### Create a "stock" branch and populate it with stock configuration from the install

```sh
git clone  --no-checkout git@bitbucket.org:suspectdevicesadmin/mailhost.git configs
cd configs
git config core.worktree "../../../"
git branch stock
cat > /.gitignore <<EOD
/**
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

The biggest PITA without tazzikki sause here is that breaking changes were made between Dovecot 2.3 and 2.4 and the community documentation does an absolutely awefull job of documenting how to translate them. Dovecot really wants you to purchase the professional version. Spent a few hours re-evaluating the alternatives before moving on.

The rough version of things that work at present is the following.

```sh
root@mailhost:/etc/dovecot/conf.d# doveconf -n
# 2.4.1-4 (7d8c0e5759): /etc/dovecot/dovecot.conf
# Pigeonhole version 2.4.1-4 (0a86619f)
# OS: Linux 6.12.30+bpo-amd64 x86_64 Debian 13.6
# Hostname: ezra.suspectdevices.com
dovecot_config_version = 2.4.1
dovecot_storage_version = 2.4.1
listen = *
mail_driver = maildir
mail_path = ~/Maildir
protocols {
  imap = yes
}
passdb pam {
}
userdb passwd {
}
namespace inbox {
  inbox = yes
  mailbox Drafts {
    special_use = "\\Drafts"
  }
  mailbox Junk {
    special_use = "\\Junk"
  }
  mailbox Trash {
    special_use = "\\Trash"
  }
  mailbox Sent {
    special_use = "\\Sent"
  }
  mailbox "Sent Messages" {
    special_use = "\\Sent"
  }
}
service imap-login {
  inet_listener imap {
  }
  inet_listener imaps {
    port = 993
    ssl = yes
  }
}
service lmtp {
  unix_listener lmtp {
  }
}
service imap {
}
service auth {
  unix_listener auth-userdb {
  }
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
  }
}
service auth-worker {
  user = root
}
service dict {
  unix_listener dict {
  }
}
ssl_server {
  cert_file = /etc/letsencrypt/live/mailhost.suspectdevices.com/fullchain.pem
  dh_file = /etc/letsencrypt/ssl-dhparams.pem
  key_file = /etc/letsencrypt/live/mailhost.suspectdevices.com/privkey.pem
}
```

The actual configuration is smeared all over a linux conf.d style pile of files and I am pretty sure I need to get rid of most of them. 

## Testing the new system

With the config above we are able to send mail from gmail but cant recieve it because spf and dkim haven't been set up for 3dangst.com
We were also unable to email between suspectdevices.com and 3dangst.com because 3dangst.com was still in naomis postfix config. This was fixed. 

## Adding / Fixing spf, dmark, and dkim

I never did get dkim to communicate with postfix via a local socket so it's going through the loopback. Need to make sure this doesn't bleed out any where.

### /etc/opendkim.conf

```sh
Socket inet:8891@localhost
...
KeyTable            refile:/etc/opendkim/key.table
SigningTable        refile:/etc/opendkim/signing.table
...
ExternalIgnoreList  refile:/etc/opendkim/trusted.hosts
InternalHosts       refile:/etc/opendkim/trusted.hosts
```

### /etc/opendkim/key|signing.tables

```sh
root@mailhost:~/mailhost# cat /etc/opendkim/signing.table
*@fromhell.com fromhell
*@suspectdevices.com suspectdevices
*@3dangst.com 3dangst
*@digithink.com digithink
*@busholini.org busholini
root@mailhost:~/mailhost# cat /etc/opendkim/key.table
fromhell     fromhell.com:201807:/etc/opendkim/keys/fromhell.private
suspectdevices suspectdevices.com:201807:/etc/opendkim/keys/suspectdevices.private
3dangst 3dangst.com:default:/etc/opendkim/keys/3dangst.private
digithink digithink.com:default:/etc/opendkim/keys/digithink.private
busholini busholini.org:default:/etc/opendkim/keys/busholini.private
root@mailhost:~/mailhost# cat /etc/opendkim/trusted.hosts
127.0.0.1
69.41.138.98/27
localhost
*.digithink.com
*.fromhell.com
*.suspectdevices.com
*.busholini.org
*.3dangst.com
```

### /etc/postfix/main.cf

```sh
...
smtpd_milters = inet:127.0.0.1:8891
non_smtpd_milters = $smtpd_milters
...
```

### Dns changes

```sh
$TTL 600
digithink.com.  IN      SOA     dns.digithink.com. don.digithink.com. (
                2026071400 108000 36000 960000 864000 )
                IN      NS      dns.digithink.com.
                IN      NS      dns1.digithink.com.
                IN      NS      dns2.digithink.com.
                IN      MX      10 mailhost.suspectdevices.com.
                IN      A       69.41.138.100
$ORIGIN digithink.com.
... other hosts ...
mailhost        IN      A       69.41.138.102
mail            IN      CNAME   mailhost
... other stuff ...
@               TXT     "v=spf1 ip4:69.41.138.97/27 -all"
_dmarc          TXT     "V=DMARC1; p=none; pct=100; fo=1; rua=mailto:don@digithink.com"
default._domainkey      IN      TXT     ( "v=DKIM1; h=sha256; k=rsa; "
          "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAo6SVMubkHnZu8f15O08LJfD1EzLKEo17Yw/KZGhOZ8VFvXHY8FK/Wi//odNsq66B8PYC+reRdnueIvY>
          "WBT5NL/dzF5+6THLC3jEL03GtenjQSAE6BgXdc7gSfeFaYIWsm19GEMgEt1Yz9Z6fLqtHVaLcesL0dcXdpSSd8bJWME/q8rRmiG5hoUpsyrEE90yDR7eNmT5nWQ6l>

```
## Checking the mail data and transferring the mail from the old host

I didnt see any difference between the new account and the transferred ones so I transferred the mail the old shcool way. 
*This was wrong.*

After tarring, copying and untarring, the /var/mail and /home directories I pointed thunderbird to the new server. I was able to see and send mail but everything was mangled.

## Cleaning up the mess.

I was going to eliminate the /etc/doveconf/conf.d directory but something is missing from the single conf file created by dovecot.org/upgrader/ file and so I just put everything that was working back and cleaned up the remaining mess by migrating things the hard way.

### Migrating things the hard way

As I already had mail coming in I needed to get the mailboxes on my local system and on the new mail server sorted out. It turns out I probably only needed to add "prefix = .INBOX." to the inbox namespace. But by that time I had already migrated most of my mail the hard way.

#### The hard way.

- Set up the accounts or point the old accounts to the new server 
   *this was in an attempt to keep the rules/filters* 
- Move the ~Maildir to ~MaildirFoobarred for later removal
- Find file location of of the account storage.
- Quit thunderbird. (imap client)
- clean everything out of that directory *(for old accounts)*
- Open thunderbird.
- Stand up a temporary account and point it at the old server
- Drag the mail (folder at a time) from one server to the next
- Delete the temporary account.

## Other Mistakes.

After I migrated all of my mx records to point to mailhost.suspectdevices.com I forgot to put a period at the end of the mx record and gmail started trying to send things to hosts like mailhost.suspectdevices.com.digithink.com. This was fixed.

I forgot to rename the default private key to digithink.private and set the owner to opendkim:opendkim so google rejected things from digithink.com for a bit.

## Improvements made.

- 3 of the 5 domains served did not have spf,_dmarc, and dkim set up. 
  - This is done for all domains.
- Snake oil certs are now set up through LetsEncrypt.

## Getting rid of the staging ip.

Given the way I created the initial ip I was having a hard time deleting it. Which did two things. 

1) Rather than swapping the staging and production ips it required me to change the ip on the of the original email server.

2) Scratch my head until I had to ask dumb questions on [discuss.linuxcontainers.org](https://discuss.linuxcontainers.org/t/reinitializing-network-config-in-existing-container/5790/12)

Since the incus debian/13/cloud image doesn't install network manager (which is a good thing) I installed ifupdown

```sh
apt update && sudo apt install ifupdown
cat > /etc/network/interfaces <<EOD
auto eth0
iface eth0 inet static
     address 69.41.138.102
     network 69.41.138.96
     netmask 255.255.255.224
     broadcast 69.41.138.127
     gateway 69.41.138.97
     mtu 9000

auto eth1
iface eth1 inet static
    address 192.168.31.141/24
EOD
reboot
```

But rather than allowing me to replace the staging ip it created a second one.
It turns out you need to get cloud init to reset the network config. I also tried to get it to seed the new address but really the ifupdown seemed to be what worked. 

```sh
root@tk2022:~# incus config edit ezra
root@tk2022:~# incus exec ezra -- cloud-init clean --seed --logs --configs network
root@tk2022:~# incus stop ezra
root@tk2022:~# incus config set ezra volatile.apply_template=create
root@tk2022:~# incus start ezra
```

Since ifupdown seemed to be required to configure both interfaces I believe that the right thing to do would be to delete "cloud-init.network-config" from the container and do the steps above.

## And we are done (for now)

I think there is still clean up that can be done on the conf.d which I may revisit.

## References

### Host repositories

- [https://www.wangzerui.com/2017/03/06/using-git-to-manage-system-configuration-files/](https://www.wangzerui.com/2017/03/06/using-git-to-manage-system-configuration-files/)

### Postfix, spf, _dmarc, dkim

- [https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp](https://www.linuxbabe.com/mail-server/build-email-server-from-scratch-debian-postfix-smtp)
- [http://www.postfix.org/STANDARD_CONFIGURATION_README.html](http://www.postfix.org/STANDARD_CONFIGURATION_README.html)
- [old mail server install docs](https://www.digithink.com/serverdocs/UbuntuMailServerSetup/)
- [https://www.digithink.com/buildnotes/ezra/](https://www.digithink.com/buildnotes/ezra/)
- [https://serverfault.com/questions/905225/migrate-from-old-to-new-postfix-dovecot-mail-server](https://serverfault.com/questions/905225/migrate-from-old-to-new-postfix-dovecot-mail-server)
- [https://www.linuxbabe.com/mail-server/spf-dkim-postfix-debian-server](https://www.linuxbabe.com/mail-server/spf-dkim-postfix-debian-server)

### Dovecot

- [https://doc.dovecot.org/2.4.4/core/config/quick.html](https://doc.dovecot.org/2.4.4/core/config/quick.html)
- [https://zunzuncito.oriole.systems/28/](https://zunzuncito.oriole.systems/28/)
- [https://github.com/dovecot/tools/blob/main/dovecot-2.4.0-example-config.tar.gz](https://github.com/dovecot/tools/blob/main/dovecot-2.4.0-example-config.tar.gz)
- [https://gist.github.com/roojs/d065c29b1d35d2b9d754cc78fc8f3b56](https://gist.github.com/roojs/d065c29b1d35d2b9d754cc78fc8f3b56)
- [https://monospace.games/posts/20250815-dovecot-24.html](https://monospace.games/posts/20250815-dovecot-24.html)
- [https://thomas-leister.de/en/mailserver-migrate-config-to-dovecot-2.4-debian-trixie/](https://thomas-leister.de/en/mailserver-migrate-config-to-dovecot-2.4-debian-trixie/)
#### INBOX
- [https://dovecot.org/mailman3/archives/list/dovecot@dovecot.org/message/2GFRCKC52A37FV6ZOU4VBBF3CKGV5NEK/](https://dovecot.org/mailman3/archives/list/dovecot@dovecot.org/message/2GFRCKC52A37FV6ZOU4VBBF3CKGV5NEK/) -- This may have been what I was missing.
- [https://marc.info/?l=dovecot&m=176241480007764](https://marc.info/?l=dovecot&m=176241480007764)

#### cloud-init 
-[https://discuss.linuxcontainers.org/t/reinitializing-network-config-in-existing-container/5790/12](https://discuss.linuxcontainers.org/t/reinitializing-network-config-in-existing-container/5790/12)