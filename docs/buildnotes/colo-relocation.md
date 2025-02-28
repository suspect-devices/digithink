# Need to move the colocated systems to a different network. ASAP.

***WORK IN PROGRESS -- Documenting as we go....***

## Basic Process

- get the new ip addresses
- put dns zone files into a repo (done)
- set dns ttls to be small. (600=10m) (done)
- add new dns server to ns records for digithink.com (done)
- stand up dns server and connect it to the new ip address range. (done)
- add the new server to the upstream (web.com) (done)
- set up remaining dns nodes to pull from new server (done) 
- add new servers to upstream (web.com) (done)
- move static websites first (done)
  - move dns (wait 10 minutes)
  - move ip configurations to new ips
- repeat above to move remaining servers ending with the mail server. (done)
- move the mail (done)
- test the mail (done)
- clean up all references to 198.202.31

### Put the dns zone files into a repo

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

### Stand up dns new server (dns.digithink.com) and connect it to the new ip address range. (done)

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

YOU ARE HERE Giving the cliffnotes version

### add the new server to the upstream

### set up remaining dns nodes to pull from new server

YOU ARE HERE Giving the cliffnotes version

### migrate vpn nodes first

Set dns entries for wireguard hosts then adjust their ips.

```sh
grep -r 198.202.31. /etc/
nano /etc/netplan/50-cloud-init.yaml
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 69.41.138.125/27
            nameservers:
                addresses:
                - 69.41.138.99
                - 8.8.8.8
                search: []
            routes:
            -   to: default
                via: 69.41.138.97
        eth1:
            addresses:
            - 192.168.31.228/24
root@virgil:~#
^x
netplan apply
ip a
sed -i s/198.202.31.132/198.202.31.99/ /etc/resolv.conf
root@virgil:~# sed -i s/198.202.31.132/198.202.31.99/ /etc/resolv.conf.static
reboot
```

YOU ARE HERE REPEATING THIS FOR SITKA

### move static websites first

- move dns (wait 10 minutes)

  YOU ARE HERE Giving the cliffnotes version

- move ip configurations to new ips

  YOU ARE HERE Giving the cliffnotes version

### repeat above to move remaining servers ending with the mail server. (done)

### move the mail (done)

YOU ARE HERE Giving the cliffnotes version

### test the mail (done)

### clean up all references to 198.202.31

```sh
root@tk2022:/etc/ansible# for c in `incus list -cn -f compact|grep -v NAME`; do echo $c ;incus exec $c -- grep -r 198.202.31. /etc/; done ; echo `hostname`; grep -r 198.202.31. /etc/
```
