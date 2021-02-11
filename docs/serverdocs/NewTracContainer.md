<!-- NewTracContainer, Version: 1, Modified: 2018/12/02, Author: trac -->
# New Trac Container
## background
Our trac server has been setup using the old trac implementation running on 16.04. It works but needs to be updated and cleaned up. 
#### Philosophy
* Where possible use only ubuntu/debian supported packages as apposed to manual/pip so that updates can be kept abreast of.
* Move the excellent online documentation to a separate section so that copies (pdf books, static html, etc) of the site include only the relevant pages.
* Leverage lxc container to create a reusable trac image.
* Leverage lxc container to create a backup of the old content.
* Add SSL functionality. 

#### Linkdump / References
* https://trac.edgewall.org/wiki/TracInstall
* https://trac.edgewall.org/wiki/TracModWSGI#ConfiguringAuthentication
* https://www.hiroom2.com/2018/11/16/ubuntu-1810-trac-en/
* https://seattle.poly.edu/wiki/TracModWSGI
* https://github.com/viktorTarasov/OpenSC-SM/wiki/Trac-and-mod_wsgi
* https://help.ubuntu.com/community/TracApacheModWsgi
* https://blog.niklasottosson.com/linux/setup-trac-project-on-debian-wheezy-with-apache-using-the-mod_wsgi-and-basic-authentication/
* https://stackoverflow.com/questions/6097515/deleting-trac-tickets-created-since-a-certain-date-until-today 
#### Raw dump of install
	
	root@douglas:~# apt-get install git
	...
	root@douglas:~# apt-get install mercurial
	...
	root@douglas:~# apt-get install postgresql
	...
	root@douglas:~# apt-get install python-psycopg2
	...
	root@douglas:~# apt-get install trac
	...
	Suggested packages:
	  www-browser apache2-doc apache2-suexec-pristine | apache2-suexec-custom libjs-jquery-ui-docs liblcms2-utils fonts-linuxlibertine | ttf-linux-libertine texlive-lang-french
	  texlive-latex-base texlive-latex-recommended doc-base python-genshi-doc python-pil-doc python-pil-dbg ttf-bitstream-vera python-setuptools-doc python-subversion-dbg
	  sgml-base-doc libapache2-mod-wsgi python-textile trac-accountmanager trac-authopenid trac-bitten trac-bzr trac-customfieldadmin trac-email2trac trac-graphviz trac-ja-resource
	  trac-mastertickets trac-mercurial trac-spamfilter trac-wikiprint trac-wikirename trac-wysiwyg trac-xmlrpc debhelper
	...
	root@douglas:~# apt-get update&&apt-get dist-upgrade&&apt-get auto remove
	... go back to his t.. lxc file push douglas /usr/local/bin/update.sh ....
	root@douglas:~# chmod 774 /usr/local/bin/update.sh 
	root@douglas:~# update.sh 
	--------------- begin updating douglas ----------------
	...
	==================#### done====================
	root@douglas:~# apt-cache search trac
	... way too much crap here ...
	python-offtrac - Python-based xmlrpc client library for trac instances (Python 2)
	....
	trac - Enhanced wiki and issue tracking system for software development projects
	trac-accountmanager - account management plugin for Trac
	trac-announcer - enhanced e-mail notification system for Trac
	trac-authopenid - OpenID authentication plugin for Trac
	trac-bitten - continuous integration plugin for Trac
	trac-bitten-slave - continuous integration plugin for Trac
	trac-codecomments - code comments and review plugin for Trac
	trac-customfieldadmin - panel for administrating custom ticket fields in Trac
	trac-datefield - Add custom date fields to Trac tickets
	trac-diavisview - Renders dia and vdx files in Trac
	trac-email2trac - Creates and amends Trac tickets from e-mail
	trac-graphviz - Graphs printing plugin for Trac
	trac-httpauth - Force HTTP authentication from within Trac
	trac-icalview - Provides iCalendar feeds for ticket queries
	trac-includemacro - Include external resources in a Trac wiki page
	trac-jsgantt - displays Trac tickets as a Gantt chart in a wiki page
	trac-mastertickets - adds inter-ticket dependencies to Trac
	trac-mercurial - Mercurial version control backend for Trac
	trac-navadd - add custom items to main and meta navigation bar in Trac webapp
	trac-privatetickets - Allows Trac users to only see tickets they are associated with
	trac-privateticketsplugin - transitional dummy package for trac-privatetickets
	trac-privatewiki - add private wiki ability to Trac
	trac-roadmap - enhances the Trac roadmap with sorting and filtering
	trac-sensitivetickets - Plugin for Trac ticketing system to hide tickets marked as sensitive
	trac-spamfilter - Spam-prevention plugin for Trac
	trac-subcomponents - use multiple layers of components in Trac
	trac-subtickets - sub-ticket feature for Trac tickets
	trac-tags - Tagging plugin for Trac wiki and issue tracking system
	trac-translatedpages - Show translated versions of wiki page in the Trac web application
	trac-virtualticketpermissions - Extended permissions plugin for Trac ticketing system
	trac-wikiprint - Make Trac wiki pages printable, exporting to PDF or printable HTML
	trac-wikitablemacro - SQL Table in Wiki Page for Trac
	trac-wysiwyg - WYSIWYG style editor for the Trac issue tracking system
	trac-xmlrpc - XML-RPC interface to the Trac wiki and issue tracking system
	...
	root@douglas:~# apt-cache search psycopg*
	python-psycopg2 - Python module for PostgreSQL
	python-psycopg2-dbg - Python module for PostgreSQL (debug extension)
	python-psycopg2-doc - Python module for PostgreSQL (documentation package)
	python3-psycopg2 - Python 3 module for PostgreSQL
	python3-psycopg2-dbg - Python 3 module for PostgreSQL (debug extension)
	python-psycogreen - psycopg2 integration with coroutine libraries
	python3-aiopg - PostgreSQL integration with asyncio
	root@douglas:~# apt-get install python3-psycopg2
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	Suggested packages:
	  python-psycopg2-doc
	The following NEW packages will be installed:
	  python3-psycopg2
	0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
	Need to get 152 kB of archives.
	After this operation, 838 kB of additional disk space will be used.
	Get:1 http://archive.ubuntu.com/ubuntu bionic/main amd64 python3-psycopg2 amd64 2.7.4-1 [152 kB]
	Fetched 152 kB in 1s (178 kB/s)           
	Selecting previously unselected package python3-psycopg2.
	(Reading database ... 56846 files and directories currently installed.)
	Preparing to unpack .../python3-psycopg2_2.7.4-1_amd64.deb ...
	Unpacking python3-psycopg2 (2.7.4-1) ...
	Setting up python3-psycopg2 (2.7.4-1) ...
	root@douglas:~# apt-get install libapache2-mod-wsgi python-textile trac-accountmanager trac-authopenid trac-bitten  trac-customfieldadmin trac-email2trac trac-graphviz
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following additional packages will be installed:
	  adwaita-icon-theme at-spi2-core dconf-gsettings-backend dconf-service fontconfig fontconfig-config fonts-dejavu-core fonts-liberation glib-networking glib-networking-common
	  glib-networking-services graphviz gsettings-desktop-schemas gtk-update-icon-cache hicolor-icon-theme humanity-icon-theme libann0 libatk-bridge2.0-0 libatk1.0-0 libatk1.0-data
	  libatspi2.0-0 libavahi-client3 libavahi-common-data libavahi-common3 libcairo-gobject2 libcairo2 libcdt5 libcgraph6 libcolord2 libcroco3 libcups2 libdatrie1 libdconf1
	  libegl-mesa0 libegl1 libepoxy0 libfontconfig1 libgbm1 libgd3 libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common libglapi-mesa libglvnd0 libgraphite2-3 libgtk-3-0
	  libgtk-3-bin libgtk-3-common libgts-0.7-5 libgts-bin libgvc6 libgvpr2 libharfbuzz0b libice6 libjs-flot libjs-jquery-flot libjson-glib-1.0-0 libjson-glib-1.0-common
	  liblab-gamut1 libltdl7 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpathplan4 libpixman-1-0 libproxy1v5 libpython2.7 librest-0.7-0 librsvg2-2 librsvg2-bin
	  librsvg2-common libsm6 libsoup-gnome2.4-1 libsoup2.4-1 libthai-data libthai0 libwayland-client0 libwayland-cursor0 libwayland-egl1-mesa libwayland-server0 libx11-xcb1 libxaw7
	  libxcb-dri2-0 libxcb-dri3-0 libxcb-present0 libxcb-render0 libxcb-shm0 libxcb-sync1 libxcb-xfixes0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxinerama1
	  libxkbcommon0 libxmu6 libxpm4 libxrandr2 libxrender1 libxshmfence1 libxt6 libxtst6 python-html5lib python-openid python-pygraphviz python-six python-webencodings
	  trac-bitten-slave ubuntu-mono x11-common
	Suggested packages:
	  gsfonts graphviz-doc colord cups-common libgd-tools gvfs libjs-jquery-flot-docs python-lxml python-pygraphviz-doc python-regex getmail4
	The following NEW packages will be installed:
	  adwaita-icon-theme at-spi2-core dconf-gsettings-backend dconf-service fontconfig fontconfig-config fonts-dejavu-core fonts-liberation glib-networking glib-networking-common
	  glib-networking-services graphviz gsettings-desktop-schemas gtk-update-icon-cache hicolor-icon-theme humanity-icon-theme libann0 libapache2-mod-wsgi libatk-bridge2.0-0
	  libatk1.0-0 libatk1.0-data libatspi2.0-0 libavahi-client3 libavahi-common-data libavahi-common3 libcairo-gobject2 libcairo2 libcdt5 libcgraph6 libcolord2 libcroco3 libcups2
	  libdatrie1 libdconf1 libegl-mesa0 libegl1 libepoxy0 libfontconfig1 libgbm1 libgd3 libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common libglapi-mesa libglvnd0
	  libgraphite2-3 libgtk-3-0 libgtk-3-bin libgtk-3-common libgts-0.7-5 libgts-bin libgvc6 libgvpr2 libharfbuzz0b libice6 libjs-flot libjs-jquery-flot libjson-glib-1.0-0
	  libjson-glib-1.0-common liblab-gamut1 libltdl7 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpathplan4 libpixman-1-0 libproxy1v5 libpython2.7 librest-0.7-0
	  librsvg2-2 librsvg2-bin librsvg2-common libsm6 libsoup-gnome2.4-1 libsoup2.4-1 libthai-data libthai0 libwayland-client0 libwayland-cursor0 libwayland-egl1-mesa
	  libwayland-server0 libx11-xcb1 libxaw7 libxcb-dri2-0 libxcb-dri3-0 libxcb-present0 libxcb-render0 libxcb-shm0 libxcb-sync1 libxcb-xfixes0 libxcomposite1 libxcursor1
	  libxdamage1 libxfixes3 libxi6 libxinerama1 libxkbcommon0 libxmu6 libxpm4 libxrandr2 libxrender1 libxshmfence1 libxt6 libxtst6 python-html5lib python-openid python-pygraphviz
	  python-six python-textile python-webencodings trac-accountmanager trac-authopenid trac-bitten trac-bitten-slave trac-customfieldadmin trac-email2trac trac-graphviz ubuntu-mono
	  x11-common
	0 upgraded, 119 newly installed, 0 to remove and 79 not upgraded.
	Need to get 18.0 MB of archives.
	After this operation, 83.3 MB of additional disk space will be used.
	Do you want to continue? [Y/n]
	…
	root@douglas:~# apt-get install trac-mastertickets trac-mercurial trac-spamfilter trac-wikiprint trac-xmlrpc debhelper
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following additional packages will be installed:
	  autoconf automake autopoint autotools-dev binutils binutils-common binutils-x86-64-linux-gnu build-essential cpp cpp-7 dh-autoreconf dh-strip-nondeterminism dpkg-dev fakeroot
	  g++ g++-7 gcc gcc-7 gcc-7-base gcc-8-base gettext gsfonts intltool-debian libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libarchive-cpio-perl
	  libarchive-zip-perl libart-2.0-2 libasan4 libatomic1 libbinutils libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libdpkg-perl libfakeroot libfile-fcntllock-perl
	  libfile-stripnondeterminism-perl libgcc-7-dev libgcc1 libgomp1 libisl19 libitm1 liblsan0 libltdl-dev libmail-sendmail-perl libmpc3 libmpx2 libquadmath0 libstdc++-7-dev
	  libstdc++6 libsys-hostname-long-perl libtimedate-perl libtool libtsan0 libubsan0 linux-libc-dev m4 make manpages-dev mercurial mercurial-common po-debconf python-dns
	  python-dnspython python-httplib2 python-lockfile python-pypdf2 python-renderpm python-reportlab python-reportlab-accel python-xhtml2pdf spambayes
	Suggested packages:
	  autoconf-archive gnu-standards autoconf-doc binutils-doc cpp-doc gcc-7-locales dh-make dwz debian-keyring g++-multilib g++-7-multilib gcc-7-doc libstdc++6-7-dbg gcc-multilib
	  flex bison gdb gcc-doc gcc-7-multilib libgcc1-dbg libgomp1-dbg libitm1-dbg libatomic1-dbg libasan4-dbg liblsan0-dbg libtsan0-dbg libubsan0-dbg libcilkrts5-dbg libmpx2-dbg
	  libquadmath0-dbg gettext-doc libasprintf-dev libgettextpo-dev glibc-doc bzr libtool-doc libstdc++-7-doc gfortran | fortran95-compiler gcj-jdk m4-doc make-doc kdiff3
	  | kdiff3-qt | kompare | meld | tkcvs | mgdiff qct python-mysqldb python-openssl wish libmail-box-perl python-lockfile-doc python-renderpm-dbg pdf-viewer
	  python-egenix-mxtexttools python-reportlab-doc
	The following NEW packages will be installed:
	  autoconf automake autopoint autotools-dev binutils binutils-common binutils-x86-64-linux-gnu build-essential cpp cpp-7 debhelper dh-autoreconf dh-strip-nondeterminism dpkg-dev
	  fakeroot g++ g++-7 gcc gcc-7 gcc-7-base gettext gsfonts intltool-debian libalgorithm-diff-perl libalgorithm-diff-xs-perl libalgorithm-merge-perl libarchive-cpio-perl
	  libarchive-zip-perl libart-2.0-2 libasan4 libatomic1 libbinutils libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libdpkg-perl libfakeroot libfile-fcntllock-perl
	  libfile-stripnondeterminism-perl libgcc-7-dev libgomp1 libisl19 libitm1 liblsan0 libltdl-dev libmail-sendmail-perl libmpc3 libmpx2 libquadmath0 libstdc++-7-dev
	  libsys-hostname-long-perl libtimedate-perl libtool libtsan0 libubsan0 linux-libc-dev m4 make manpages-dev mercurial mercurial-common po-debconf python-dns python-dnspython
	  python-httplib2 python-lockfile python-pypdf2 python-renderpm python-reportlab python-reportlab-accel python-xhtml2pdf spambayes trac-mastertickets trac-mercurial
	  trac-spamfilter trac-wikiprint trac-xmlrpc
	The following packages will be upgraded:
	  gcc-8-base libgcc1 libstdc++6
	3 upgraded, 78 newly installed, 0 to remove and 76 not upgraded.
	Need to get 48.6 MB of archives.
	After this operation, 197 MB of additional disk space will be used.
	Do you want to continue? [Y/n] 
	.....
	root@douglas:~# nano /etc/postgresql/10/main/pg_hba.conf 
	root@douglas:~# su - postgres
	postgres@douglas:~$ psql template1
	psql (10.6 (Ubuntu 10.6-0ubuntu0.18.04.1))
	Type "help" for help.
	
	template1=# create database tracdb with encoding = 'utf8';
	CREATE DATABASE
	template1=# create user tracuser password 'password';
	CREATE ROLE
	template1=# grant all on database tracdb to tracuser;
	GRANT
	template1=# \q
	postgres@douglas:~$ exit
	logout
	..... grumble grumble ..... bad password ....
	root@douglas:~# service postgres reload
	postgres: unrecognized service
	root@douglas:~# service postgresql reload
	root@douglas:~# mkdir /var/
	backups/ cache/   crash/   lib/     local/   lock/    log/     mail/    opt/     run/     snap/    spool/   tmp/     www/     
	root@douglas:~# mkdir /var/trac/devel
	mkdir: cannot create directory ‘/var/trac/devel’: No such file or directory
	root@douglas:~# mkdir /var/trac/
	root@douglas:~# mkdir /var/trac/devel
	root@douglas:~# cd /var/trac/devel/
	root@douglas:/var/trac/devel# mkdir repo env
	root@douglas:/var/trac/devel# trac-admin /var/trac/devel/env/ initenv
	Creating a new Trac environment at /var/trac/devel/env
	
	Trac will first ask a few questions about your environment
	in order to initialize and prepare the project database.
	
	 Please enter the name of your project.
	 This name will be used in page titles and descriptions.
	
	Project Name [My Project]> Development
	
	 Please specify the connection string for the database to use.
	 By default, a local SQLite database is created in the environment
	 directory. It is also possible to use an existing MySQL or
	 PostgreSQL database (check the Trac documentation for the exact
	 connection string syntax).
	
	Database connection string [sqlite:db/trac.db]>  postgres://tracuser:password@localhost/tracdb
	
	Creating and Initializing Project
	 Installing default wiki pages
	  InterWiki imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/InterWiki
	  WikiProcessors imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiProcessors
	  TracUpgrade imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracUpgrade
	  TracUnicode imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracUnicode
	  WikiPageNames imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiPageNames
	  TracRevisionLog imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracRevisionLog
	  TracWiki imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracWiki
	  TracSearch imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracSearch
	  TracGuide imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracGuide
	  TracLinks imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracLinks
	  TracInterfaceCustomization imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracInterfaceCustomization
	  TracBrowser imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracBrowser
	  TracTickets imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracTickets
	  WikiNewPage imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiNewPage
	  TracSupport imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracSupport
	  TracStandalone imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracStandalone
	  TracChangeLog imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracChangeLog
	  TracNavigation imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracNavigation
	  TracAccessibility imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracAccessibility
	  TracSyntaxColoring imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracSyntaxColoring
	  TracFineGrainedPermissions imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracFineGrainedPermissions
	  TracInstall imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracInstall
	  InterTrac imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/InterTrac
	  WikiMacros imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiMacros
	  TracImport imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracImport
	  TitleIndex imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TitleIndex
	  SandBox imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/SandBox
	  TracCgi imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracCgi
	  TracBackup imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracBackup
	  WikiHtml imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiHtml
	  TracTicketsCustomFields imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracTicketsCustomFields
	  CamelCase imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/CamelCase
	  TracModWSGI imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracModWSGI
	  WikiFormatting imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiFormatting
	  RecentChanges imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/RecentChanges
	  TracBatchModify imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracBatchModify
	  TracRepositoryAdmin imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracRepositoryAdmin
	  InterMapTxt imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/InterMapTxt
	  TracRoadmap imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracRoadmap
	  WikiDeletePage imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiDeletePage
	  TracWorkflow imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracWorkflow
	  WikiRestructuredText imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiRestructuredText
	  TracIni imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracIni
	  TicketQuery imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TicketQuery
	  TracNotification imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracNotification
	  TracEnvironment imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracEnvironment
	  TracPlugins imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracPlugins
	  WikiStart imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiStart
	  TracReports imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracReports
	  TracAdmin imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracAdmin
	  WikiRestructuredTextLinks imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/WikiRestructuredTextLinks
	  TracChangeset imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracChangeset
	  TracQuery imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracQuery
	  TracFastCgi imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracFastCgi
	  TracRss imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracRss
	  TracTimeline imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracTimeline
	  TracModPython imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracModPython
	  TracLogging imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracLogging
	  PageTemplates imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/PageTemplates
	  TracPermissions imported from /usr/lib/python2.7/dist-packages/trac/wiki/default-pages/TracPermissions
	
	---------------------------------------------------------------------
	Project environment for 'Development' created.
	
	You may now configure the environment by editing the file:
	
	  /var/trac/devel/env/conf/trac.ini
	
	If you'd like to take this new project environment for a test drive,
	try running the Trac standalone web server `tracd`:
	
	  tracd --port 8000 /var/trac/devel/env
	
	Then point your browser to http://localhost:8000/env.
	There you can also browse the documentation for your installed
	version of Trac, including information on further setup (such as
	deploying Trac to a real web server).
	
	The latest documentation can also always be found on the project
	website:
	
	  http://trac.edgewall.org/
	
	Congratulations!
	
	root@douglas:/var/trac/devel# tracd --port 8000 /media/shared/Admin/trac/repo/
	...
	root@douglas:/var/trac/devel# trac-admin /var/trac/devel/env/ deploy /var/trac/devel/www/
	Copying resources from:
	  trac.web.chrome.Chrome
	    /usr/lib/python2.7/dist-packages/trac/htdocs
	    /var/trac/devel/env/htdocs
	Creating scripts.
	root@douglas:/var/trac/devel# nano /etc/apache2/sites-enabled/000-default.conf 
	root@douglas:/var/trac/devel# service apache2 reload
	root@douglas:/var/trac/devel# chmod u+x www/cgi-bin/trac.wsgi 
	root@douglas:/var/trac/devel# chown www-data env/conf/trac.ini
	root@douglas:/var/trac/devel# trac-admin
	trac-admin - The Trac Administration Console 1.2
	
	Usage: trac-admin </path/to/projenv> [command [subcommand] [option ...]]
	
	Invoking trac-admin without command starts interactive mode.
	
	help     Show documentation
	initenv  Create and initialize a new environment
	root@douglas:/var/trac/devel# trac-admin /var/trac/devel/env/
	Welcome to trac-admin 1.2
	Interactive Trac administration console.
	Copyright (C) 2003-2013 Edgewall Software
	
	Type:  '?' or 'help' for help on commands.
	        
	Trac [/var/trac/devel/env]> ?
	trac-admin - The Trac Administration Console 1.2
	help                 Show documentation
	initenv              Create and initialize a new environment
	attachment add       Attach a file to a resource
	attachment export    Export an attachment from a resource to a file or stdout
	attachment list      List attachments of a resource
	attachment remove    Remove an attachment from a resource
	changeset added      Notify trac about changesets added to a repository
	changeset modified   Notify trac about changesets modified in a repository
	component add        Add a new component
	component chown      Change component ownership
	component list       Show available components
	component remove     Remove/uninstall a component
	component rename     Rename a component
	config get           Get the value of the given option in "trac.ini"
	config remove        Remove the specified option from "trac.ini"
	config set           Set the value for the given option in "trac.ini"
	deploy               Extract static resources from Trac and all plugins
	hotcopy              Make a hot backup copy of an environment
	milestone add        Add milestone
	milestone completed  Set milestone complete date
	milestone due        Set milestone due date
	milestone list       Show milestones
	milestone remove     Remove milestone
	milestone rename     Rename milestone
	permission add       Add a new permission rule
	permission export    Export permission rules to a file or stdout as CSV
	permission import    Import permission rules from a file or stdin as CSV
	permission list      List permission rules
	permission remove    Remove a permission rule
	priority add         Add a priority value option
	priority change      Change a priority value
	priority list        Show possible ticket priorities
	priority order       Move a priority value up or down in the list
	priority remove      Remove a priority value
	repository add       Add a source repository
	repository alias     Create an alias for a repository
	repository list      List source repositories
	repository remove    Remove a source repository
	repository resync    Re-synchronize trac with repositories
	repository set       Set an attribute of a repository
	repository sync      Resume synchronization of repositories
	resolution add       Add a resolution value option
	resolution change    Change a resolution value
	resolution list      Show possible ticket resolutions
	resolution order     Move a resolution value up or down in the list
	resolution remove    Remove a resolution value
	session add          Create a session for the given sid
	session delete       Delete the session of the specified sid
	session list         List the name and email for the given sids
	session purge        Purge anonymous sessions older than the given age or date
	session set          Set the name or email attribute of the given sid
	severity add         Add a severity value option
	severity change      Change a severity value
	severity list        Show possible ticket severities
	severity order       Move a severity value up or down in the list
	severity remove      Remove a severity value
	ticket remove        Remove ticket
	ticket_type add      Add a ticket type
	ticket_type change   Change a ticket type
	ticket_type list     Show possible ticket types
	ticket_type order    Move a ticket type up or down in the list
	ticket_type remove   Remove a ticket type
	upgrade              Upgrade database to current version
	version add          Add version
	version list         Show versions
	version remove       Remove version
	version rename       Rename version
	version time         Set version date
	wiki dump            Export wiki pages to files named by title
	wiki export          Export wiki page to file or stdout
	wiki import          Import wiki page from file or stdin
	wiki list            List wiki pages
	wiki load            Import wiki pages from files
	wiki remove          Remove wiki page
	wiki rename          Rename wiki page
	wiki replace         Replace the content of wiki pages from files (DANGEROUS!)
	wiki upgrade         Upgrade default wiki pages to current version
	Trac [/var/trac/devel/env]> help wiki dump
	wiki dump <directory> [page] [...]
	
	    Export wiki pages to files named by title
	
	    Individual wiki page names can be specified after the directory. A name
	    ending with a * means that all wiki pages starting with that prefix should
	    be dumped. If no name is specified, all wiki pages are dumped.
	
	Trac [/var/trac/devel/env]> 
	root@douglas:/var/trac/devel# mv ~feurig/tracpwd.old env/.htpasswd
	root@douglas:/var/trac/devel#  trac-admin /var/trac/devel/env/ permission add feurig TRAC_ADMIN
	root@douglas:/var/trac/devel# trac-admin /var/trac/devel/env/ permission add joe TRAC_ADMIN
	root@douglas:/var/trac/devel# cp ~feurig/sd_logo_sm.png env/htdocs/
	root@douglas:/var/trac/devel# chmod oug+r env/htdocs/sd_logo_sm.png 
	root@douglas:/var/trac/devel# nano env/conf/trac.ini
	
	