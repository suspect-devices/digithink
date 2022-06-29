``` yaml
# ------------------------------------ roles/ubuntu-unifi-server/tasks/main.yml
- name: download unifi-lastest script
  get_url:
    url: https://get.glennr.nl/unifi/install/install_latest/unifi-latest.sh
    dest: /root/unifi-latest.sh
    mode: '0700'

- name: Run Easy Unifi Script.
  command: "bash /root/unifi-latest.sh --skip --add-repository"

- name: install nginx
  apt:
    state: latest
    name: nginx

- name: remove default nginx site
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent

- name: Seed nginx configuration
  copy:
    src: "../files/nginx.conf"
    dest: /etc/nginx/nginx.conf
#
- name: Restart nginx service
  service: 
    name: nginx
    enabled: yes
    state: restarted
```

``` json
# -------------------------- ansible/roles/ubuntu-unifi-server/files/nginx.conf
# ---- simplest redirection I could figure out 

user www-data;
worker_processes auto;
pid /run/nginx.pid;

include /etc/nginx/modules-enabled/*.conf;

events {}

stream {
    upstream unifi {
        server localhost:8443;
    }
        server {
        listen        443;
        proxy_pass    unifi;
    }
}
http {
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        return 301 https://$host:8443$request_uri;
    }
	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;
	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}
```