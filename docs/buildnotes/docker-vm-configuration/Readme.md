# Centos 7 Docker Host (Franklin Rebuild *DRAFT*)
Lxd 4 introduced qemu/vm support making it possible to install docker in a way that doesnt compromise the underlying server. We want to use docker to present a private repository protected by an nginx proxy using LetsEncrypt SSL certificates.

## Basic process.
* Install centos7 vm
* Install prerequisites
* Add docker-ce repository
* Install docker-ce
* Install docker-registry
* Install nginx


### In order to let docker do its thing without leaking we use a vm.
#### Create the vm.

```
root@kb2018:/etc/ansible# lxc image copy images:centos/7 local: --copy-aliases --vm
root@kb2018:/home/feurig# lxc init centos/7 franklin --vm -pdefault -psusdev21vm
```

#### Add static networking.

```
root@kb2018:/home/feurig# lxc config edit franklin
architecture: x86_64
config:
  image.architecture: amd64
  image.description: Centos 7 amd64 (20210823_07:08)
  image.os: Centos
  image.release: "7"
  image.serial: "20210823_07:08"
  image.type: disk-kvm.img
  image.variant: default
  user.network-config: |
    version: 1
    config:
      - type: physical
        name: eth0
        subnets:
          - type: static
            ipv4: true
            address: 198.202.31.201
            netmask: 255.255.255.128
            gateway: 198.202.31.129
            control: auto
      - type: nameserver
        address: 198.202.31.132
  volatile.base_image: 812cf4c1b46f4ff2422a6e81c9991bdda12b36e53c58f4edc74580e21034860e
  volatile.eth0.host_name: tap62181f92
  volatile.eth0.hwaddr: 00:16:3e:ef:11:ac
  volatile.last_state.power: RUNNING
  volatile.uuid: ce2b1e78-5825-46d1-8335-88caca447a58
  volatile.vsock_id: "50"
devices: {}
ephemeral: false
profiles:
- default
- susdev21vm
stateful: false
description: ""
root@kb2018:/home/feurig# lxc start franklin
```

### And since the machine had no network the first time it came up it wont have run the cloud init that provides us with our users usw.
*There are centos/7/cloud vms that would let us skip this step.*

#### Install and rerun cloud init.

```
root@kb2018:/home/feurig# lxc exec franklin bash
[root@franklin feurig]# yum install cloud-init
[root@franklin feurig]# cloud-init-cfg all config
[root@franklin ~]# cloud-init clean
[root@franklin ~]# cloud-init init

```

### First we installed the docker that comes with centos7

```
[root@franklin feurig]# yum search docker
Loaded plugins: fastestmirror, product-id, search-disabled-repos, subscription-
...
Installing:
 docker-latest          x86_64   1.13.1-58.git87f2fab.el7.centos      extras    16 M
Installing for dependencies:
 criu                   x86_64   3.12-2.el7                           base     453 k
 docker-client-latest   x86_64   1.13.1-58.git87f2fab.el7.centos      extras   3.8 M
 libnet                 x86_64   1.1.6-7.el7                          base      59 k
 protobuf-c             x86_64   1.0.2-3.el7                          base      28 k

Transaction Summary
=====================================================================================
Install  1 Package (+4 Dependent packages)

Total download size: 21 M
Installed size: 71 M
Is this ok [y/d/N]: y
...
Complete!
```

### Then we realized its too old and so we got the current docker-ce from docker.

#### Uninstall what we just did.

```
[root@franklin feurig]# yum remove docker \
                   docker-client \
                   docker-client-latest \
                   docker-common \
                   docker-latest \
                   docker-latest-logrotate \
                   docker-logrotate \
                   docker-engine
...
Removing:
 docker                 x86_64   2:1.13.1-208.git7d71120.el7_9       @extras    64 M
 docker-client          x86_64   2:1.13.1-208.git7d71120.el7_9       @extras    13 M
 docker-client-latest   x86_64   1.13.1-58.git87f2fab.el7.centos     @extras    13 M
 docker-common          x86_64   2:1.13.1-208.git7d71120.el7_9       @extras   4.4 k
 docker-latest          x86_64   1.13.1-58.git87f2fab.el7.centos     @extras    57 M

Transaction Summary
=====================================================================================
Remove  5 Packages

Installed size: 146 M
Is this ok [y/N]: y
...
```

#### Add the docker repo and install.

```
[root@franklin feurig]#  yum --enablerepo=Extras
[root@franklin feurig]# yum install -y yum-utils
...
Installed:
  yum-utils.noarch 0:1.1.31-54.el7_8

Dependency Installed:
  python-kitchen.noarch 0:1.1.1-5.el7

Complete!
[root@franklin feurig]# yum-config-manager \
     --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
...
repo saved to /etc/yum.repos.d/docker-ce.repo
```

#### Check to see if the docker version is the one that's going to be installed.

```

[root@franklin feurig]# yum list docker-ce --showduplicates | sort -r |head
 * updates: mirror.keystealth.org
This system is not registered with an entitlement server. You can use subscription-manager to register.
              : manager
Loading mirror speeds from cached hostfile
Loaded plugins: fastestmirror, product-id, search-disabled-repos, subscription-
 * extras: centos-distro.1gservers.com
docker-ce.x86_64            3:20.10.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.6-3.el7                     docker-ce-stable

```

#### Install it.

```
[root@franklin feurig]# yum install docker-ce
...
Installing:
 docker-ce                    x86_64    3:20.10.8-3.el7    docker-ce-stable     23 M
Installing for dependencies:
 containerd.io                x86_64    1.4.9-3.1.el7      docker-ce-stable     30 M
 docker-ce-cli                x86_64    1:20.10.8-3.el7    docker-ce-stable     29 M
 docker-ce-rootless-extras    x86_64    20.10.8-3.el7      docker-ce-stable    8.0 M
 docker-scan-plugin           x86_64    0.8.0-3.el7        docker-ce-stable    4.2 M

Transaction Summary
=====================================================================================
Install  1 Package (+4 Dependent packages)

Total download size: 94 M
Installed size: 380 M
Is this ok [y/d/N]: y
Downloading packages:
warning: /var/cache/yum/x86_64/7/docker-ce-stable/packages/docker-ce-20.10.8-3.el7.x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID 621e9f35: NOKEY
Public key for docker-ce-20.10.8-3.el7.x86_64.rpm is not installed
...
Retrieving key from https://download.docker.com/linux/centos/gpg
Importing GPG key 0x621E9F35:
 Userid     : "Docker Release (CE rpm) <docker@docker.com>"
 Fingerprint: 060a 61c5 1b55 8a7f 742b 77aa c52f eb6b 621e 9f35
 From       : https://download.docker.com/linux/centos/gpg
Is this ok [y/N]: y
...
Installed:
  docker-ce.x86_64 3:20.10.8-3.el7

Dependency Installed:
  containerd.io.x86_64 0:1.4.9-3.1.el7
  docker-ce-cli.x86_64 1:20.10.8-3.el7
  docker-ce-rootless-extras.x86_64 0:20.10.8-3.el7
  docker-scan-plugin.x86_64 0:0.8.0-3.el7

Complete!
```

### Now we are ready to go. 

```
[root@franklin feurig]# docker run hello-world
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
[root@franklin feurig]# systemctl start docker
[root@franklin feurig]# systemctl enable docker
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.
[root@franklin feurig]# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
Digest: sha256:0fe98d7debd9049c50b597ef1f85b7c1e8cc81f59c8d623fcb2250e8bec85b38
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

[root@franklin feurig]#
```

### Set up nginx and Let's Encrypt / certbot.
#### Derp.

For this we need an fqdn. I picked derp.
Derp. Docker Eh? Really? Pfffft.

#### BLDGP.  (Here are some other plans).
The bouncing prompt at [https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-centos-7](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-centos-7) gets us an nginx front end to route our containers through with LetEncrypt ssl certificates that will manage themselves as long as .well-known/acme-challenge is a valid path on the server.

```
[feurig@franklin ~]$ sudo bash
[sudo] password for feurig: 
# VVVVV SYSTEM FEEDBACK OMMITTED BELOW VVVVV #
[root@franklin feurig]# yum install epel-release
[root@franklin feurig]# yum install certbot-nginx
[root@franklin feurig]# yum install nginx
[root@franklin feurig]# systemctl start nginx
[root@franklin feurig]# systemctl enable nginx
[root@franklin feurig]# nano /etc/nginx/nginx.conf
[root@franklin feurig]# ping derp.suspectdevices.com
[root@franklin feurig]# systemctl reload nginx
```

#### Cut a hole in the firewall for the http/https server

```
[root@franklin feurig]# iptables -I INPUT -p tcp -m tcp --dport 80 -j ACCEPT
[root@franklin feurig]# iptables -I INPUT -p tcp -m tcp --dport 443 -j ACCEPT
```

#### And finally install the certificate with certbot.

```
[root@franklin feurig]# certbot --nginx -d derp.suspectdevices.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator nginx, Installer nginx
Enter email address (used for urgent renewal and security notices)
 (Enter 'c' to cancel): don@suspectdevices.com
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server. Do you agree?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Yes

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing, once your first certificate is successfully issued, to
share your email address with the Electronic Frontier Foundation, a founding
partner of the Let's Encrypt project and the non-profit organization that
develops Certbot? We'd like to send you email about our work encrypting the web,
EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Yes
Account registered.
Requesting a certificate for derp.suspectdevices.com and docker.suspectdevices.com
Performing the following challenges:
http-01 challenge for derp.suspectdevices.com
http-01 challenge for docker.suspectdevices.com
Using default addresses 80 and [::]:80 ipv6only=on for authentication.
Waiting for verification...
Cleaning up challenges
Deploying Certificate to VirtualHost /etc/nginx/nginx.conf
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator nginx, Installer nginx
Starting new HTTPS connection (1): acme-v02.api.letsencrypt.org
Requesting a certificate for derp.suspectdevices.com
Deploying Certificate to VirtualHost /etc/nginx/nginx.conf
Redirecting all traffic on port 80 to ssl in /etc/nginx/nginx.conf

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations! You have successfully enabled https://derp.suspectdevices.com
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Subscribe to the EFF mailing list (email: don@suspectdevices.com).
Starting new HTTPS connection (1): supporters.eff.org

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/derp.suspectdevices.com-0001/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/derp.suspectdevices.com-0001/privkey.pem
   Your certificate will expire on 2021-11-24. To obtain a new or
   tweaked version of this certificate in the future, simply run
   certbot again with the "certonly" option. To non-interactively
   renew *all* of your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

### And now we are ready to set up our private repository in a docker container.

#### Run up a docker registry:2 image

*Change this to use local storage at some point for now the container stores the data*

```
[root@franklin feurig]# docker run -d -p 5000:5000 --restart always --name registry registry:2
[root@franklin feurig]# curl localhost:5000/v2/_catalog
{"repositories":[]}
[root@franklin feurig]# docker tag 1fd8e1b0bb7e localhost:5000/registry:2
[root@franklin feurig]# docker push localhost:5000/registry:2
[root@franklin feurig]# curl localhost:5000/v2/_catalog
{"repositories":["registry"]}

```

#### Configure the Proxy.

What we want is to merge the nginx configuration created by certbot and the one provided below. [https://docs.docker.com/registry/recipes/nginx/](https://docs.docker.com/registry/recipes/nginx/) Also the proxy is responsible for authentication. 


```
events {
    worker_connections  1024;
}

http {

  upstream docker-registry {
    server registry:5000;
  }

  ## Set a variable to help us decide if we need to add the
  ## 'Docker-Distribution-Api-Version' header.
  ## The registry always sets this header.
  ## In the case of nginx performing auth, the header is unset
  ## since nginx is auth-ing before proxying.
  map $upstream_http_docker_distribution_api_version $docker_distribution_api_version {
    '' 'registry/2.0';
  }

  server {
    listen 443 ssl;
    server_name myregistrydomain.com;

    # SSL
    ssl_certificate /etc/nginx/conf.d/domain.crt;
    ssl_certificate_key /etc/nginx/conf.d/domain.key;

    # Recommendations from https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
    ssl_protocols TLSv1.1 TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    # disable any limits to avoid HTTP 413 for large image uploads
    client_max_body_size 0;

    # required to avoid HTTP 411: see Issue #1486 (https://github.com/moby/moby/issues/1486)
    chunked_transfer_encoding on;

    location /v2/ {
      # Do not allow connections from docker 1.5 and earlier
      # docker pre-1.6.0 did not properly set the user agent on ping, catch "Go *" user agents
      if ($http_user_agent ~ "^(docker\/1\.(3|4|5(?!\.[0-9]-dev))|Go ).*$" ) {
        return 404;
      }

      # To add basic authentication to v2 use auth_basic setting.
      auth_basic "Registry realm";
      auth_basic_user_file /etc/nginx/conf.d/nginx.htpasswd;

      ## If $docker_distribution_api_version is empty, the header is not added.
      ## See the map directive above where this variable is defined.
      add_header 'Docker-Distribution-Api-Version' $docker_distribution_api_version always;

      proxy_pass                          http://docker-registry;
      proxy_set_header  Host              $http_host;   # required for docker client's sake
      proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
      proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header  X-Forwarded-Proto $scheme;
      proxy_read_timeout                  900;
    }
  }
}

```
##### After nginx Derp's nginx.conf looks like this.

```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
    if ($host = derp.suspectdevices.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        listen       80;
        listen       [::]:80;
        server_name  derp.suspectdevices.com;
    return 404; # managed by Certbot


}}

```
##### Adding basic Authentication to the proxy. 

But before we add the proxy pass we need to give it some basic authentication. Since we are a 2 admin user system .httpasswd is fine.

#### *YOU ARE STILL HERE CONFIGURING THE PROXY !!!!*


### References.

* [https://www.linuxtechi.com/install-docker-on-centos-7/](https://www.linuxtechi.com/install-docker-on-centos-7/)
* [https://www.linuxtechi.com/setup-docker-private-registry-centos-7-rhel-7/](https://www.linuxtechi.com/setup-docker-private-registry-centos-7-rhel-7/)
* [https://docs.genesys.com/Documentation/System/Current/DDG/InstallationofDockerEngineCommunityEditiononCentOS7](https://docs.genesys.com/Documentation/System/Current/DDG/InstallationofDockerEngineCommunityEditiononCentOS7)
* [https://blog.simos.info/how-to-use-virtual-machines-in-lxd/](https://blog.simos.info/how-to-use-virtual-machines-in-lxd/)
* [https://www.cyberciti.biz/faq/how-to-secure-nginx-lets-encrypt-on-centos-7/](https://www.cyberciti.biz/faq/how-to-secure-nginx-lets-encrypt-on-centos-7/)
* [https://linuxize.com/post/secure-nginx-with-let-s-encrypt-on-centos-7/](https://linuxize.com/post/secure-nginx-with-let-s-encrypt-on-centos-7/)
* [https://linuxconcept.com/how-to-secure-nginx-with-lets-encrypt-on-centos-7-linux/](https://linuxconcept.com/how-to-secure-nginx-with-lets-encrypt-on-centos-7-linux/)
* https://stackoverflow.com/questions/41456996/how-to-access-docker-registry-v2-with-curl
* https://bobcares.com/blog/docker-private-repository/
* [https://docs.docker.com/registry/recipes/nginx/](https://docs.docker.com/registry/recipes/nginx/)
* [https://www.digitalocean.com/community/tutorials/understanding-nginx-http-proxying-load-balancing-buffering-and-caching](https://www.digitalocean.com/community/tutorials/understanding-nginx-http-proxying-load-balancing-buffering-and-caching)
* 
