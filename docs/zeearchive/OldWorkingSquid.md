## Rehomed this pile from old document.
Squid is a complicated and burdensome beast its good to have at least and example of a working configuration.

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

- <https://wiki.squid-cache.org/SquidFaq/SquidAcl>
