# Mkdocs Server Configuration.
For the past several years I have been using Trac to maintain server notes and create a todo sort of ticketing system for our systems. Trac is kind of a pain to setup and maintain and though I work well with the wiki (documenting as I go), and the ticketing communicates the work being done, I have not been able to get others to contribute to the documentation. I tried the trac extention to allow markdown to be embedded in the wiki pages but its kind of jenky.

Recently I started documenting my builds and projects in markdown and then storing them along with any configuration files and scripts in Github or Bitbucket repositories.
Assuming that this is the way forward I am rebuilding the digithink.com site using  markdown as the source.

## Markdown based web services.
 
After looking at several options I narrowed my search to mk-docs and allmark. Mkdocs was in the supported ubuntu repos so I started there. I good results but was dissappointed with the themeing avaliable, until I looked at [Material for Mk-docs (https://squidfunk.github.io/mkdocs-material/)](https://squidfunk.github.io/mkdocs-material/) 
### Installing Material for Mk-doc

mkdocs-material unfortunatly isn't packaged however, it can be installed through pip3. To export the complete site as a pdf we also install the mkdocs-with-pdf.

    apt-get install python3-pip
    pip3 install mkdocs-material
    apt-get install build-essential python3-dev python3-pip python3-setuptools python3-   wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
    pip3 install WeasyPrint
    pip3 install mkdocs-with-pdf

### Converting Trac Wiki Entries to Markdown
I was able to convert the 50 or so wiki pages on serverdocs and clean them up. 

#### Ruby
I found a [gist (and three refinements)](https://gist.github.com/somebox/619537), which even though I don't ruby well I was able to adapt to pg-ruby. It isnt perfect but it worked.

[export.rb](export.rb)
#### Python 
I found this [python based script (trac2down.py)](https://gist.githubusercontent.com/sgk/1286682/raw/b744dd2e47a68d60373ad39df87cfe8256f517af/trac2down.py) which needed to be adapted for postgres and python 3. It does not handle tables. It does however insert an author and timestamp into the document. If I can I would like to finish this with table support. In the mean time. I have a working copy that is clean enough. 

[export.py](export.py)

... add some explanation for getting the resulting 
### Building the static web site (staging server).

    cd /theflatfield/static/digithink/
    mkdocs build
    chown -R www-data:www-data site/

### Serving it up with lighttpd

    root@nina:/# nano /etc/lighttpd/lighttpd.conf
    ...
	 server.document-root        = "/theflatfield/static/digithink/site"
	 server.upload-dirs          = ( "/var/cache/lighttpd/uploads" )
	 server.errorlog             = "/var/log/lighttpd/error.log"
	 server.pid-file             = "/run/lighttpd.pid"
	 server.username             = "www-data"
	 server.groupname            = "www-data"
	 server.port                 = 80
	 ...
    root@nina:/# service lighttpd restart
 
### Moving the site to production. 
The source code for the site is on github under feurig/digithink. Any changes made to the source files (like this one) should be pushed. Then the site is updated and rebuilt on herbert our lightttpd server (serves digitihink,busholini, and 3dangst).


