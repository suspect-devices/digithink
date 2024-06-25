# Bartender: a wsgi server.

I wanted to do a simple git hook for a static website or two where the content was pulled down and converted from markdown with a little mermaid to static html. I have been doing this manually for a while but it gets to be a pain and besides all the kids are doing ci-cd and I thought it might help me actually write more.

Once apon a time when apache was really the best way to serve http writing interactive sites in python was a matter of enableing mod_wsgi and throwing up 20 lines of python. 

Gone are those days. 

Three days of swimming through uwsgi, unit and 3 other overtly complicated half thought out python solutions all of which require a separate standalone service I settled on a flask and gunicorn. Its still a kludgy pile. Time to go queue TurboNegros "I hate the kids" and just make it work.


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