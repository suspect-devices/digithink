<!-- MigrateUsers, Version: 1, Modified: 2018/12/02, Author: trac -->
	# Migrate Users UID/GID
	apt-get update
	apt-get dist-upgrade
	tasksel
	apt-get update
	apt-get dist-upgrade
	vipw
	export EDITOR=nano
	
	chown --from=1000:1000 999:999 /. -Rv
	
	
	