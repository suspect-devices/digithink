# Craig Johnson -- rebuild static http sites on Debian.

## ORGANIZE THIS PILE

### Go old school on the static network configuration.
Systemd/networkd is coming but I want something that works right now.

/etc/network/interfaces aint broken.

So tear out all the new and replace it with the old.
```
systemctl stop systemd-networkd
systemctl disable systemd-networkd
systemctl stop systemd-networkd.socket
systemctl disable systemd-networkd.socket
apt install ifupdown
```
#### Then configure it like it was a decade ago.

```
cat /etc/network/interfaces
auto lo
iface lo inet loopback


auto eth0
iface eth0 inet static
     address 198.202.31.221
     network 198.202.31.128
     netmask 255.255.255.128
     broadcast 198.202.31.255
     gateway 198.202.31.129 
     mtu 9000

auto eth0:1
iface eth0:1 inet static
     address 198.202.31.230
     network 198.202.31.128
     netmask 255.255.255.128
     broadcast 198.202.31.255
     gateway 198.202.31.129 
     mtu 9000

auto eth0:2
iface eth0:2 inet static
     address 198.202.31.231
     network 198.202.31.128
     netmask 255.255.255.128
     broadcast 198.202.31.255
     gateway 198.202.31.129 
     mtu 9000


auto eth0:3
iface eth0:3 inet static
     address 198.202.31.232
     network 198.202.31.128
     netmask 255.255.255.128
     broadcast 198.202.31.255
     gateway 198.202.31.129 
     mtu 9000


```
##

### nginx configuration
#### New config for www.3dangst.com (default)

```
server {

	#listen 443 ssl 198.202.31.221;
	root /var/www/3dangst/site;
	index index.html;

	server_name www.3dangst.com;

	location / {
		try_files $uri $uri/ =404;
	}

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/www.3dangst.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/www.3dangst.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = www.3dangst.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


	listen 80 default_server;

	server_name www.3dangst.com;
    return 404; # managed by Certbot


}
```

#### copy nginx config, /etc/letsencrypt and content (/var/www/*) from the old server

We copied the old servers default to /etc/nginx/sites-avaliable/digithink and then linked it into sites-enabled.

``` 
cat /etc/nginx/sites-avaliable/digithink
server {

    listen 198.202.31.230:80;
    server_name www.digithink.com;

    if ($host = www.digithink.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = 198.202.31.230) {
        return 444;
    } # managed by Certbot

    return 404; # managed by Certbot
}


server {
    listen 198.202.31.230:80;
    server_name  www.digithink.com;
    root /var/www/digithink/site;
    index index.html;

    listen 198.202.31.230:443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/www.digithink.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/www.digithink.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    if ($host = 198.202.31.230) {
       return 444;
    } # managed by Certbot
	
   error_page 404 /404.html;
   location  /404.html {
      internal;
   }

}

upstream bartender {
	server 127.0.0.1:5000;
}

server {
    server_name bartender.digithink.com;

    listen 198.202.31.232:443 ssl;
    server_name bartender.digithink.com;
    ssl_certificate /etc/letsencrypt/live/bartender.digithink.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/bartender.digithink.com/privkey.pem; # managed by Certbot

    root /var/www/digithink/whiskey/bartender;
    index index.html;
    location /whiskey {
        include proxy_params;
        proxy_pass http://bartender/whiskey;
    }

    error_page 404 /404.html;
    location  /404.html {
          internal;
    }

    location /lacuenta {
        root /var/www/digithink/whiskey/logs;
    }


}

server {
    if ($host = bartender.digithink.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 198.202.31.232:80;
    server_name bartender.digithink.com;
    return 404; # managed by Certbot
}


server {
        listen 198.202.31.231:80;
        server_name busholini.org w.busholini.org www.busholini.org;
        if ($host = www.busholini.org) {
           return 301 https://$host$request_uri;
        } # managed by Certbot
        if ($host = git.suspectdevices.com) {
           return 444;
        }
        if ($host = 198.202.31.231) {
           return 444;
        }
    return 404; # managed by Certbot


}

server {
        listen 198.202.31.231:443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/www.busholini.org/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/www.busholini.org/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

        server_name busholini.org w.busholini.org www.busholini.org;

        if ($host = git.suspectdevices.com) {
           return 444;
        }
        if ($host = 198.202.31.231) {
           return 444;
        }

        root /var/www/busholini/www;
        index index.html;

}
cd /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/digithink .
nginx -t
```
#### Install the parts that the bartender needs

```sh
apt install python3-flask
apt install python3-gunicorn

apt install at
echo www-data |tee /etc/at.allow
```