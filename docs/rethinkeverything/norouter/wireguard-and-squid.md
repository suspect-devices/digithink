# Replacing the colo router with a container

After working through the complexities of using headscale/tailscale I realized that I really only needed the colo router to do 2 things.

1. Provide us access to the admin lan (the servers and their remote consoles).
2. Allow the servers to reach the update repositories.

By using a container with access to both the external lan and the admin lan we can set up wireguard and squid. Wireguard allows us to securely connect to the admin lan while squid allows the servers a mechanism to recieve software updates.


``` 
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```

## SETTING UP THE CONTAINER

```
root@aoc2024:~# lxc init ubuntu:22.04 homer -c security.privileged=true -p susdev23 -p infra
root@aoc2024:~# lxc config edit homer
name: homer
description: "wireguard/squid host"
...
devices:
  eth1:
    name: eth1
    nictype: bridged
    parent: br3
    type: nic
^x
root@aoc2024:~# lxc start homer
root@aoc2024:~# lxc exec homer bash
root@homer:~# nano /etc/netplan/50-cloud-init.yaml
network:
    version: 2
    ethernets:
        eth0:
            addresses:
            - 198.202.31.227/25
            nameservers:
                addresses:
                - 198.202.31.132
                - 8.8.8.8
                search:
                - suspectdevices.com
                - styx.suspectdevices.com
            routes:
            -   to: default
                via: 198.202.31.129
        eth1:
            addresses:
            - 192.168.31.227/24
^x
root@homer:~# netplan apply
```
Backcheck the interfaces
```
root@homer:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
45: eth0@if46: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:ba:f0:be brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 198.202.31.227/25 brd 198.202.31.255 scope global eth0
       valid_lft forever preferred_lft forever
47: eth1@if48: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:2e:6f:d8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.31.227/24 brd 192.168.31.255 scope global eth1
       valid_lft forever preferred_lft forever
```

### Install prerequisites and enable ip forwarding
The next few sections are done on the gateway container (homer)
```
apt install wireguard
apt install resolvconf
apt install squid
sysctl -w net.ipv4.ip_forward=1
```

## Wireguard

### Set up wireguard

```
cd /etc/wireguard/
wg genkey | sudo tee private.key
chmod go= private.key
cat private.key | wg pubkey | sudo tee public.key
wg genpsk |tee preshared.psk
nano /etc/wireguard/wg0.conf
```

```
# wg0.conf
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

#### Enable it

```
wg-quick up wg0
systemctl enable wg-quick@wg0
```
## Squid proxy for main servers

### Setting up squid

```
nano /etc/squid/squid.conf
```

```
# -------------------------------------------------------/etc/squid/squid.conf
acl localnet src 192.168.31.0/24  # RFC 1918 local private network (LAN)
acl SSL_ports port 443
acl Safe_ports port 80  # http
acl Safe_ports port 21  # ftp
acl Safe_ports port 443  # https
acl Safe_ports port 70  # gopher
acl Safe_ports port 210  # wais
acl Safe_ports port 1025-65535 # unregistered ports
acl Safe_ports port 280  # http-mgmt
acl Safe_ports port 488  # gss-http
acl Safe_ports port 591  # filemaker
acl Safe_ports port 777  # multiling http
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
refresh_pattern ^ftp:  1440 20% 10080
refresh_pattern ^gopher: 1440 0% 1440
refresh_pattern -i (/cgi-bin/|\?) 0 0% 0
refresh_pattern \/(Packages|Sources)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern \/Release(|\.gpg)$ 0 0% 0 refresh-ims
refresh_pattern \/InRelease$ 0 0% 0 refresh-ims
refresh_pattern \/(Translation-.*)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern .  0 20% 4320
```

#### Enable it

```
systemctl enable squid
systemctl start squid
```

### Test the proxy

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

### Set up apt to use proxy
```
nano /etc/apt/apt.conf.d/00proxy.conf
```
```
Acquire::http::Proxy "http://192.168.31.227:3128/";
```
### Test apt through proxy
```
root@aoc2024:/etc/apt/apt.conf.d# ip route delete default
root@aoc2024:/etc/apt/apt.conf.d# ip route
192.168.31.0/24 dev br3 proto kernel scope link src 192.168.31.158
root@aoc2024:/etc/apt/apt.conf.d# apt update
Hit:1 http://us.archive.ubuntu.com/ubuntu noble InRelease
Get:2 https://pkgs.tailscale.com/stable/ubuntu noble InRelease
Hit:3 http://us.archive.ubuntu.com/ubuntu noble-updates InRelease
Hit:4 http://security.ubuntu.com/ubuntu noble-security InRelease
Hit:5 http://us.archive.ubuntu.com/ubuntu noble-backports InRelease
Fetched 6575 B in 1s (9357 B/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
All packages are up to date.
```

## References / Linkdump

- <https://www.wireguard.com>
- <https://www.freecodecamp.org/news/build-your-own-wireguard-vpn-in-five-minutes/>
- <https://linuxiac.com/how-to-use-apt-with-proxy/>
- <https://askubuntu.com/questions/257290/configure-proxy-for-apt#257296>
- <https://wiki.squid-cache.org/SquidFaq/SquidAcl>
