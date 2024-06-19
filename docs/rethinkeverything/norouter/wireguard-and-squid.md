# Replacing the colo router with a container

After working through the complexities of using headscale/tailscale I realized that I really only needed the colo router to do 2 things. 

1) Provide us access to the admin lan (the servers and their remote consoles).
2) Allow the servers to reach the update repositories.

## SETTING UP THE CONTAINER

YOU ARE HERE DESCRIBING THE CONTAINER

### Install prerequisites and enable ip forwarding

```
apt install wireguard
apt install resolvconf
apt install squid
sysctl -w net.ipv4.ip_forward=1
```
### Set up wireguard
```
cd /etc/wireguard/
wg genkey | sudo tee private.key
chmod go= private.key
private.key | wg pubkey | sudo tee public.key
wg genpsk |tee preshared.psk
nano /etc/wireguard/wg-server.conf
```

```
# wg-server.conf
[Interface]
Address = 10.0.0.1/32
ListenPort = 1194
PrivateKey = <<contents of private.key>>
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth1 -j MASQUERADE

# merlot
[Peer]
PublicKey = <<contents of public.key>>
AllowedIPs =  10.0.0.2/32,192.168.128.0/17
PresharedKey = <<contents of preshared.key>>

# amyl dons laptop
[Peer]
PublicKey = <<key from wireguard client>>
AllowedIPs = 10.0.0.3/32
PresharedKey = <<contents of preshared.key>>
```
#### Enable it. 
```
wg-quick up wg0
systemctl enable wg-quick@wg0
```
### Setting up squid 
```
nano /etc/squid/squid.conf
```

```
# -------------------------------------------------------/etc/squid/squid.conf
acl localnet src 192.168.31.0/24		# RFC 1918 local private network (LAN)
acl SSL_ports port 443
acl Safe_ports port 80		# http
acl Safe_ports port 21		# ftp
acl Safe_ports port 443		# https
acl Safe_ports port 70		# gopher
acl Safe_ports port 210		# wais
acl Safe_ports port 1025-65535	# unregistered ports
acl Safe_ports port 280		# http-mgmt
acl Safe_ports port 488		# gss-http
acl Safe_ports port 591		# filemaker
acl Safe_ports port 777		# multiling http
acl CONNECT method CONNECT
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
include /etc/squid/conf.d/*
http_access allow localhost
http_access allow localnet
http_access deny all
http_port 3128
coredump_dir /var/spool/squid
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern \/(Packages|Sources)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern \/Release(|\.gpg)$ 0 0% 0 refresh-ims
refresh_pattern \/InRelease$ 0 0% 0 refresh-ims
refresh_pattern \/(Translation-.*)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern .		0	20%	4320
```
#### Enable it.
```
systemctl enable squid
systemctl start squid
```
```
root@kb2018:~# curl -x 192.168.31.227:3128 http://archive.ubuntu.com/ubuntu
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="http://archive.ubuntu.com/ubuntu/">here</a>.</p>
<hr>
<address>Apache/2.4.52 (Ubuntu) Server at archive.ubuntu.com Port 80</address>
</body></html>
```




## References / Linkdump
- https://www.wireguard.com
- https://www.freecodecamp.org/news/build-your-own-wireguard-vpn-in-five-minutes/
- https://linuxiac.com/how-to-use-apt-with-proxy/
- https://askubuntu.com/questions/257290/configure-proxy-for-apt#257296
- https://wiki.squid-cache.org/SquidFaq/SquidAcl
