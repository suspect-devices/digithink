# Need to move the colocated systems to a different network. ASAP.
***WORK IN PROGRESS -- Documenting as we go....***
## Basic Process
- get the new ip addresses

- put dns zone files into a repo (done)
- set dns ttls to be small. (600=10m)
- stand up dns server and connect it to the new ip address range. (in progress)
- 


### put the dns zone files into a repo

### new dns server (dns.digithink.com)

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
ls
git clone https://x-token-auth:ATCTT3xFfGN0SodQXb30YN_jT98revfOAKnaHPMqVK2a2ARF1Lgx3OX6cYRA0thIh6K-Pr_ySp4ItX8PoWu1XFqiV_94ZEMHOizR4Ktk8S8cm_1i6o1xkpioYGAc5oll4G_wYwKCDpnrM4LlWDnaE8Fl_djiihXkh3
mv named.conf.local /tmp/
ln -s zones/named.conf.local .
systemctl reload named
systemctl status named
cd zones
ls
nano named.conf.local
nano master.conf
systemctl reload named
systemctl status named.service
nano master.conf
systemctl reload named
systemctl status named.service
nano master.conf
nano master.conf
systemctl reload named
systemctl status named.service
git status
git commit -a -m "delete unused domains"
git config user.email ul0xnzfaxu14vn34v75polnfqm8v6q@bots.bitbucket.org
git commit -a -m "delete unused domains"
git push
history
history|cut -c8-200
root@piage:/etc/bind/zones# history -1000 |cut -c8-200
-bash: history: -1: invalid option
history: usage: history [-c] [-d offset] [n] or history -anrw [filename] or history -ps arg [arg...]
root@piage:/etc/bind/zones# history 1000 |cut -c8-200
ip a
cd /etc/
grep -ri 198.202.31.200
nano systemd/network/10-cloud-init-eth0.network
apt install nano
exit
ip a
nano systemd/network/10-cloud-init-eth0.network
grep -ri 198.202.31.200
grep -ri 198.202.31.200
ip a
reboot
cloud-init status
cd /etc/
grep -ri 198.202.31.200
nano systemd/network/10-cloud-init-eth0.network
reboot
ip a
ping digithink.som
ping digithink.com
history
history|cut c8-200
history|cut -c8-200
exit
cd /etc/named
cd /etc/bind
git clone https://x-token-auth:REDACTED@bitbucket.org/suspectdevicesadmin/susdev-dns.git
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
