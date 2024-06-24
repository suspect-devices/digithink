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

https://www.stackovercloud.com/2020/05/27/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04/


```
apt install uwsgi
systemctl enable uwsgi
nano /etc/uwsgi/apps-enabled/whisky.ini
apt install python3-flask
root@guenter:~# ls -ls /run/uwsgi/app/whisky/socket
0 srw-rw---- 1 www-data root 0 Jun 23 18:31 /run/uwsgi/app/whisky/socket

```