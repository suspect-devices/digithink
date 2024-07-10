# gitea-configuration
(Build notes for getea server.)

Master Copy: [https://github.com/feurig/gitea-configuration/blob/main/README.md](https://github.com/feurig/gitea-configuration/blob/main/README.md)

Gitea is a github like environment written in go. It provides git in an accessable form and allows you to create issues and write wiki pages like redmine and trac while also serving those repositories. 

It is less convoluted than gitlab but more configurable than GCOS which it is based on.  


## Server Setup
### Installing pre-requisites

We are building on a ubuntu/focal/cloud (from lxc's images) container with preseeded admin accounts. 

```
apt-get -y install curl postgresql apache2 git
apt-get install postfix
... add as a Satelite (null client) ...
```
We want to use a single git user so we add it (will deal with this later)

```
adduser --system --shell /bin/bash --group --disabled-password --home /home/git git
```
We are going to use the package provided by packaging.gitlab.io 

```
curl -sL -o /etc/apt/trusted.gpg.d/morph027-gitea.asc https://packaging.gitlab.io/gitea/gpg.key
deb [trusted=yes arch=amd64] https://packaging.gitlab.io/gitea gitea main" | sudo tee /etc/apt/sources.list.d/morph027-gitea.list
update.sh
apt-get install gitea
```
### Setting up postgresql database
```
su - postgres
postgres@shelly:~$ createuser -P git
... add passwd
postgres@shelly:~$ createdb gitea -O git
```
### Initial configuration
Once gitea is installed go to myservername:3000 and navigate to the login in the upper right corner. Fill in the database,username, and dbpassword. Replace localhost with your servers fqdn. Create admin user (remember password here)

## Testing it out.
The first thing we want to do here is to mirror our github repositories.

### Mirroring Github Repositories.
We want to automate mirroring all of our repositories hosted on github (and bitbucket at some point). To do this we create a personal-access-token from our github developer tools. (save the token somewhere as it will not be recoverable). Once we have that token we select New migration. Fill in the https://github.com/myuser/myrepo and paste the token into the form, select mirror and the magic begins.

### Editing the mirror interval
The default mirror interval is 8 hours with a minimum of 10 minutes. 
To fix this we add the following to /etc/gitea/app.ini

```
nano /etc/gitea.app.ini
...
[cron.update_mirrors]
SCHEDULE = @every 2m

[mirror]
DEFAULT_INTERVAL = 1h
MIN_INTERVAL = 2m
...
service gitea restart
```

### Automating creation of mirrors (github).
We were able to automate mirroring our github repos with the help of some python provided by jpmens.net we modified it to allow us to separate local mirrors by the same organizations used by github though this required us to manually add the local users and organizations. The script in progress is here.

[https://github.com/feurig/gitea-configuration/blob/main/mirror-repos.py](https://github.com/feurig/gitea-configuration/blob/main/mirror-repos.py)

#### Manually migrating bitbucket mirrors.
Like github mirroring bitbucket repositories required the creation of an application password. Then add a new "Git" migration using the application password as your credentials.
 
## Setting up ssl and apache proxy.
Gitea runs as an unprivilaged user on port 3000. To present it as a normal web server required a proxy server (apache). Since we had created letsEncrypt certificates for the old git server we moved them. There are still permissions issues with giving gitea access to the certificates which were worked around by copying the files.

Getting apache to proxy the https required enabling 'proxy\_http2' and 'proxy' module (not 'proxy\_http')

```
a2enmod proxy proxy_http2
```
* Gitea configuration [etc/gitea/app.ini](https://github.com/feurig/gitea-configuration/blob/main/etc/gitea/app.ini)
* Apache configuration [etc/apache2/sites-avaliable/gitea.conf](https://github.com/feurig/gitea-configuration/blob/main/etc/apache2/sites-avaliable/gitea.conf)

### Manually updating LetsEncrypt certificates.
Gitea serves static content under the public/custom directory. In order to update the lets encrypt certificates you will need to open two shells into the git server. 

In the first window initiate the update request.

```
certbot certonly --manual
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator manual, Installer None
Account registered.
Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c'
to cancel): git.suspectdevices.com
Generating a certificate request for git.suspectdevices.com
Performing the following challenges:
http-01 challenge for git.suspectdevices.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Create a file containing just this data:

loIND53_1yZLSZX1lKkLqhCBY7YhNo_vzdyrEznXHSQ.MQ0FIIV4g1TA8EJatJpiciDipeqHIMHJsetBrs2tzqM

And make it available on your web server at this URL:

http://git.suspectdevices.com/.well-known/acme-challenge/loIND53_1yZLSZX1lKkLqhCBY7YhNo_vzdyrEznXHSQ

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Press Enter to Continue
```

In the second window create the file requested file.

```
root@shelly:/var/lib/gitea# cd public/custom/
root@shelly:/var/lib/gitea/public/custom# echo loIND53_1yZLSZX1lKkLqhCBY7YhNo_vzdyrEznXHSQ.MQ0FIIV4g1TA8EJatJpiciDipeqHIMHJsetBrs2tzqM >.well-known/acme-challenge/loIND53_1yZLSZX1lKkLqhCBY7YhNo_vzdyrEznXHSQ
root@shelly:/var/lib/gitea/public/custom# chown -R gitea:gitea .

```
Then continue in the first window and copy the new keys to where gitea expects them.

```
Press Enter to Continue
... when finished copy the new certs to gitea ...
cd /etc/letsencrypt/live/git.suspectdevices.com/
cp fullchain.pem privkey.pem /var/lib/gitea/keys/
chown -R gitea:gitea /var/lib/gitea/keys/
reboot
```

### Todo (No Major Issues)
* Document making gitea less ugly (add Susdev brand look and feel)
* Fix permission issues with certificate issues to allow for autorenewal if possible.
* Consider normalizing git user and repo locations.

## references/linkdump
* [https://gitlab.com/packaging/gitea](https://gitlab.com/packaging/gitea)
* [https://bryangilbert.com/post/devops/how-to-setup-gitea-ubuntu/](https://bryangilbert.com/post/devops/how-to-setup-gitea-ubuntu/) 
* [https://luxagraf.net/src/gitea-nginx-postgresql-ubuntu-1804](https://luxagraf.net/src/gitea-nginx-postgresql-ubuntu-1804)
* [https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* [https://jpmens.net/2019/04/15/i-mirror-my-github-repositories-to-gitea/](https://jpmens.net/2019/04/15/i-mirror-my-github-repositories-to-gitea/)
* [https://websiteforstudents.com/how-to-install-gitea-git-server-on-ubuntu-16-04-18-04-18-10-with-mariadb/](https://websiteforstudents.com/how-to-install-gitea-git-server-on-ubuntu-16-04-18-04-18-10-with-mariadb/)
* [https://docs.gitea.io/en-us/config-cheat-sheet/](https://docs.gitea.io/en-us/config-cheat-sheet/)
* [https://charlesreid1.github.io/setting-up-a-self-hosted-github-clone-with-gitea.html](https://charlesreid1.github.io/setting-up-a-self-hosted-github-clone-with-gitea.html)
* [https://charlesreid1.com/wiki/Gitea#Using_Binary](https://charlesreid1.com/wiki/Gitea#Using_Binary)
* [https://mindefrag.net/2018/07/how-to-install-and-configure-gitea-a-self-hosted-github-like-service/](https://mindefrag.net/2018/07/how-to-install-and-configure-gitea-a-self-hosted-github-like-service/)
