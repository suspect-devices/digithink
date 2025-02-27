# Need to move the colocated systems to a different network. ASAP.
***WORK IN PROGRESS -- Documenting as we go....***
## Basic Process
- get the new ip addresses

- put dns zone files into a repo (done)
- set dns ttls to be small. (600=10m) (done)
- add new dns server to ns records for digithink.com (done)
- stand up dns server and connect it to the new ip address range. (done)
- add the new server to the upstream 


### put the dns zone files into a repo

- Create a blank repo in bitbucket and create an access token
- Clone the repo into /etc/bind/zones using the access token
- Move the .git folder into place and clean up.
- Add contents of /etc/bind/zones to the repo.
- Commit and push it.
```sh
cd /etc/bind/zones
git clone https://x-token-auth:REDACTED@bitbucket.org/suspectdevicesadmin/susdev-dns.git
ls -lsa susdev-dns/
mv susdev-dns/.git .
rmdir susdev-dns/
ls
git add *
git status
git commit -a -m"first checkin"
git push
cp named.conf.local zones
git add zones/named.conf.local
git commit -a -m"add the named.conf.local"
git push
```

### Stand up new dns (dns.digithink.com)

Start a new bookworm container.

```sh
incus init bookworm piage -p default -p susdev24
incus start piage
incus exec piage bash
```

Configure the network

```sh
ip a
apt install nano
cd /etc/
grep -ri 198.202.31.200
nano systemd/network/10-cloud-init-eth0.network
reboot
ip a
ping digithink.com
```

Pull down zone files from git and configure bind9 to use them.

```sh
cd /etc/bind
git clone https://x-token-auth:REDACTED@bitbucket.org/suspectdevicesadmin/susdev-dns.git zones
mv named.conf.local /tmp/
ln -s zones/named.conf.local .
nano master.conf
systemctl reload named
systemctl status named.service
git status
git commit -a -m "delete unused domains"
git config user.email REDACTED@bots.bitbucket.org
git commit -a -m "delete unused domains"
git push
```
