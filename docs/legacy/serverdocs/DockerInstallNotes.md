# Docker Installation on FranklinOnce the LXD container for docker was built out I followed the [directions at docker.com](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/) to install docker-ce
	
	root@franklin:~# apt-get remove docker docker-engine docker.io
	...
	Removing docker (1.5-1) ...
	...
	root@franklin:~# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	OK
	root@franklin:~# add-apt-repository \
	>    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	>    $(lsb_release -cs) \
	>    stable"
	root@franklin:~# apt-get update
	... Done
	root@franklin:~# apt-get install docker-ce
	Reading package lists... Done
	Building dependency tree       
	Reading state information... Done
	The following additional packages will be installed:
	  aufs-tools cgroupfs-mount libltdl7
	Suggested packages:
	  mountall
	The following NEW packages will be installed:
	  aufs-tools cgroupfs-mount docker-ce libltdl7
	0 upgraded, 4 newly installed, 0 to remove and 0 not upgraded.
	Need to get 21.2 MB of archives.
	After this operation, 100 MB of additional disk space will be used.
	Do you want to continue? [Y/n] 
	....
	root@franklin:~# exit
	  -w, --workdir string                 Working directory inside the container
	feurig@franklin:~$ sudo docker run hello-world
	[sudo] password for feurig: 
	Unable to find image 'hello-world:latest' locally
	latest: Pulling from library/hello-world
	5b0f327be733: Pull complete 
	Digest: sha256:07d5f7800dfe37b8c2196c7b1c524c33808ce2e0f74e7aa00e603295ca9a0972
	Status: Downloaded newer image for hello-world:latest
	
	Hello from Docker!
	.....
	
## References
* https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04