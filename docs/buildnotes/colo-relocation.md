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

### add the new server to the upstream

Use the web.com site to update the addresses of your authoritative dns servers

### set up remaining dns nodes to pull from new server

on tk

```sh
incus exec teddy bash
```

then adjust the secondary dns server.
```sh
nano /etc/systemd/network/10-cloud-init-eth0.network
reboot
cd /etc/named/zones
sed -i s/198.202.31.141/69.41.138.98/ slave.conf
systemctl reload named
systemctl status named
```

While you're there clean up the rest of the 198.202.31.

```sh
grep -r 198.202.31 /etc
sed -i s/198.202.31.98/69.41.138.98/ /etc/resolv.conf.static
grep -r 198.202.31 /etc
exit
```

### Migrate vpn nodes.

#### Virgil.

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
sed -i s/198.202.31.132/69.41.138.99/ /etc/resolv.conf
root@virgil:~# sed -i s/198.202.31.132/69.41.138.99/ /etc/resolv.conf.static
reboot
```

#### Sitka

Adjust the ip address of the public interface and the name servers

```sh
nano /etc/rc.conf
hostname="sitka"

ifconfig_igb4="69.41.138.126 netmask 255.255.255.224"
defaultrouter="69.41.138.97"
...
^X y
cp resolv.conf /tmp/
sed s/198.202.31.141/69.41.138.98/ /tmp/resolv.conf|sed s/198.202.31.132/69.41.138.99/>/etc/resolv.conf

reboot
```

Adjust the ip address of master dns server.

```sh
cd /usr/local/etc/namedb/zones
cp slave.conf /tmp/
sed s/198.202.31.141/69.41.138.98/ /tmp/slave.conf >slave.conf
service named restart
tail /var/log/messages
```

### move static websites 

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
for c in `incus list -cn -f compact|grep -v NAME`; do echo $c ;incus exec $c -- grep -r 198.202.31. /etc/; done ; echo `hostname`; grep -r 198.202.31. /etc/
... clean up all container references ...
... then clean up tk ...
cd /etc/ansible/
mkdir profiles
incus profile show susdev23>profiles/susdev23.yaml
incus profile show susdev24>profiles/susdev24.yaml
sed -i s/198.202.31.200/69.41.138.113/ profiles/susdev23.yaml
sed -i s/198.202.31.129/69.41.138.97/ profiles/susdev23.yaml
sed -i s/198.202.31.141/69.41.138.99/ profiles/susdev23.yaml
sed -i s/198.202.31.132/69.41.138.98/ profiles/susdev23.yaml
sed -i s/255.255.255.128/255.255.255.244/ profiles/susdev23.yaml
cat profiles/susdev23.yaml |incus profile edit susdev23
incus profile show susdev24>profiles/susdev24.yaml
sed -i s/198.202.31.200/69.41.138.113/ profiles/susdev24.yaml
sed -i s/198.202.31.129/69.41.138.97/ profiles/susdev24.yaml
sed -i s/198.202.31.141/69.41.138.98/ profiles/susdev24.yaml
sed -i s/198.202.31.132/69.41.138.99/ profiles/susdev24.yaml
sed -i s/255.255.255.128/255.255.255.244/ profiles/susdev24.yaml
cat profiles/susdev24.yaml |incus profile edit susdev24
grep -r 198.202.31. .
mv files/merlot.profile.yaml profiles/merlot.yaml
sed -i s/198.202.31.160/69.41.138.120/ profiles/merlot.yaml
sed -i s/198.202.31.141/69.41.138.98/ profiles/merlot.yaml
grep -r 198.202.31. .
sed -i s/198.202.31.160/69.41.138.120/ README.md
git status
git add files README.md playbooks roles
git add profiles/
git commit -a -m migration
git push
grep -r 198.202.31. .
```
