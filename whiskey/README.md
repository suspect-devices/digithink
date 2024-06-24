```
root@guenter:~# cat /etc/uwsgi/apps-enabled/whisky.ini
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = whiskey.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```
## linkdump

- https://www.stackovercloud.com/2020/05/27/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04/
- https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04
- https://stackoverflow.com/questions/10748108/nginx-uwsgi-unavailable-modifier-requested-0#11055729

```
apt install uwsgi
systemctl enable uwsgi
nano /etc/uwsgi/apps-enabled/whisky.ini
apt install python3-flask
apt install uwsgi-plugin-python3
root@guenter:~# ls -ls /run/uwsgi/app/whisky/socket
0 srw-rw---- 1 www-data root 0 Jun 23 18:31 /run/uwsgi/app/whisky/socket

```