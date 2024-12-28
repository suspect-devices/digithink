# Bartender: a wsgi server.

I wanted to do a simple git hook for a static website or two where the content was pulled down and converted from markdown with a little mermaid to static html. I have been doing this manually for a while but it gets to be a pain and besides all the kids are doing ci-cd and I thought it might help me actually write more.

Once apon a time when apache was really the best way to serve http writing interactive sites in python was a matter of enableing mod_wsgi and throwing up 20 lines of python. 

Gone are those days. 

Three days of swimming through uwsgi, unit and 3 other overtly complicated half thought out python solutions all of which require a separate standalone service I settled on a flask and gunicorn. It's still a kludgy pile. Time to go queue TurboNegros "I hate the kids" and just make it work.

This part of the digithink repo contains the wsgi app that is called whenever changes are pushed to digithink.com as well as the documentation and files needed to deploy it. The details and source code are found under [bartender/docs](bartender/docs/README.md).

At some point I may make the bartender and the digithink.com separate repos. At that point I will probably serve more than whiskey/neat and start developing some of my other web sites.


```