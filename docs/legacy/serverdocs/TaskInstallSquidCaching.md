# Squid Caching Server
(... explain what we want to get our of squid ...
Basic proxy ... proxy forwarded to remote proxy .... reverse proxy ...
more words here....)

## Why is this taking so long ???

"I installed squid3 (on Ubuntu), but looking at the configuration file, I am lost. I tried googling but it looks all too complicated."  -- stack overflow user

Squid is a monster. Years of development and added features have created a configuration file that has 8000 lines of comments and 20 actual lines of configuration which need to be modified for it to work at all.

## basic proxy configuration

The configuration below can be found on the squid containers  on both basement servers (Joey and DeeDee). 
To use this server set your web browser proxy to the http_port in the configuration file (3128).

	
	acl SSL_ports port 443
	acl Safe_ports port 80          # http
	acl Safe_ports port 21          # ftp
	acl Safe_ports port 443         # https
	acl Safe_ports port 70          # gopher
	acl Safe_ports port 210         # wais
	acl Safe_ports port 1025-65535  # unregistered ports
	acl Safe_ports port 280         # http-mgmt
	acl Safe_ports port 488         # gss-http
	acl Safe_ports port 591         # filemaker
	acl Safe_ports port 777         # multiling http
	acl CONNECT method CONNECT
	http_access deny !Safe_ports
	http_access deny CONNECT !SSL_ports
	http_access allow localhost manager
	http_access deny manager
	http_access allow localhost
	acl my_internal_net src 192.168.0.0/24
	http_access allow my_internal_net
	http_port 3128
	coredump_dir /var/spool/squid
	refresh_pattern ^ftp:           1440    20%     10080
	refresh_pattern ^gopher:        1440    0%      1440
	refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
	refresh_pattern (Release|Packages(.gz)*)$      0       20%     2880
	refresh_pattern .               0       20%     4320
	

## reverse proxy configuration
_Work in progress._
### minimal (no ssl) configuration
With an ssh tunnel set from our local static web server coming onto the server (jules.suspectdevices.com) at port 8085 we tell squid to route all traffic on port 80 to the server on the other end of the tunnel.
	
	debug_options ALL,2 28,9
	http_port 80 accel no-vhost defaultsite=jules.suspectdevices.com
	cache_peer 127.0.0.1 parent 8085 0 no-query originserver name=corbin
	acl theworld src all
	acl our_sites dstdomain all
	http_access allow theworld
	http_access allow our_sites
	cache_peer_access corbin allow our_sites
	cache_peer_access corbin allow theworld
	http_access deny all
	
### Secure reverse proxy
... working on it ...

From: squid example configurations
	
	https_port 443 accel defaultsite=jules.suspectdevices.com \
	  cert=/etc/ssl/certs/ssl-cert-snakeoil.pem \
	  key=/etc/ssl/private/ssl-cert-snakeoil.key
	
	# First (HTTP) peer
	cache_peer 127.0.0.1 parent 8086 0 no-query originserver login=PASS name=lilly
	
	acl pdx dstdomain jules.suspectdevices.com
	cache_peer_access lilly allow pdx
	http_access allow pdx
	
	# Security block for non-hosted sites
	http_access deny all
	
From: https://serverfault.com/questions/735535/squid-reverse-proxy-redirect-rewrite-http-to-https
	
	acl PORT80 myport 80
	http_access deny PORT80 pdx
	deny_info 301:https://foo.server.com%R pdx
	
## Dual Proxy Configuration

TODO: Having a local proxy combined with a "pihole" dns server seems to improve browsing performance considerably. Adding a second proxy upstream would allow less location based garbage as well.
[ TaskDualProxyConfiguration Dual Proxy Configuration Notes]


## Preliminary Linkdump
* http://cosmolinux.no-ip.org/raconetlinux/html/17-squid.html
* https://wiki.squid-cache.org/SquidFaq/ConfiguringSquid#Before_you_start_configuring
* https://www.tekyhost.com/squid-proxy-squid-caching-and-filtering-proxy/
* https://www.rootusers.com/configure-squid-proxy-to-forward-to-a-parent-proxy/
* https://wiki.squid-cache.org/Features/CacheHierarchy
* https://www.tecmint.com/install-squid-in-ubuntu/
* http://www.squidguard.org/about.html
* https://wiki.alpinelinux.org/wiki/Setting_up_Transparent_Squid_Proxy
