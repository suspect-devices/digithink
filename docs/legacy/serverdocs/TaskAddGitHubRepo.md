## Add "Trac"king (and Mirroring) to Github Repos
Trac supports git repos on the local machine which can be extended to GitHub repos by using the provided post commit hook. Adding the repos is a little convoluted but once set up all commits to the GitHub repository cause a backup copy to be made on the local server.

There are two components at work here. The built in git/svn repository browser and the GitHub plugin. The GitHub plugin provides the webhook.
 
### Process
In this example we are going to add one of suspect devices repos to the git server and add a webhook to synchronize the two.

[[Image(TaskAddGitHubRepo:github-example.png,100%)]]
Ssh in and clone the repo to the git/trac server. (repos are at /var/trac/devel/repos/)
 
  _To make life less of a pain www-data is set up so that you can su to the account._
  	
	haifisch:~ don$ ssh feurig@git
	...
	feurig@douglas:~$ sudo bash
	[sudo] password for feurig: 
	root@douglas:~# su - www-data
	www-data@douglas:~$ cd /var/trac/devel/repo/
	www-data@douglas:/var/trac/devel/repo$ git clone --mirror git@github.com:suspect-devices/errata_physical_computing.git
	Cloning into bare repository 'errata_physical_computing.git'...
	remote: Enumerating objects: 26, done.
	remote: Total 26 (delta 0), reused 0 (delta 0), pack-reused 26
	Receiving objects: 100% (26/26), 19.48 KiB | 19.48 MiB/s, done.
	Resolving deltas: 100% (8/8), done.
	www-data@douglas:/var/trac/devel/repo$ 
	
Log into the [git/trac site](https://trac.suspectdevices.com/devel/wiki/WikiStart) and navigate to admin->repositories
[[Image(TaskAddGitHubRepo:add-repo.png,100%)]]
Add the repo.
[[Image(TaskAddGitHubRepo:repo-added.png,100%)]]
Copy the command presented and execute it as www-data.
	
	www-data@douglas:/var/trac/devel/repo$ trac-admin "/var/trac/devel/env" repository resync "PC-errata"
	Resyncing repository history for PC-errata... 
	0 revisions cached.
	PC-errata is not a cached repository.
	Done.
	www-data@douglas:/var/trac/devel/repo$  
	
Check the the GitHub web hook url by browsing git.suspectdevices.com/devel/github/<reponame>

 It should return the following: "Endpoint is ready to accept GitHub notifications."
[[Image(TaskAddGitHubRepo:endpoint-ready.png,100%)]]

Enable the web hook on your GitHub repository.  _Navigate to the settings -> webhooks -> Add Webhook_
  * Paste the url you just tested 
  * Make sure that you select json
  * Disable checking the certificate since its self signed. _(it will bitch)_
[[Image(TaskAddGitHubRepo:add-webhook.png,100%)]]

Make changes to the repository.

	
	haifisch:~ don$ cd /tmp/
	haifisch:tmp don$ git clone git@github.com:suspect-devices/errata_physical_computing.git
	Cloning into 'errata_physical_computing'...
	remote: Enumerating objects: 26, done.
	remote: Total 26 (delta 0), reused 0 (delta 0), pack-reused 26
	Receiving objects: 100% (26/26), 19.48 KiB | 6.49 MiB/s, done.
	Resolving deltas: 100% (8/8), done.
	haifisch:tmp don$ cd errata_physical_computing/
	haifisch:errata_physical_computing don$ nano proof.md 
	haifisch:errata_physical_computing don$ git commit -a -m "Fix weird cruft at the top of the markdown"
	[master 2cc1d07] Fix weird cruft at the top of the markdown
	 1 file changed, 1 insertion(+), 1 deletion(-)
	haifisch:errata_physical_computing don$ git push
	Counting objects: 3, done.
	Delta compression using up to 4 threads.
	Compressing objects: 100% (3/3), done.
	Writing objects: 100% (3/3), 318 bytes | 318.00 KiB/s, done.
	Total 3 (delta 2), reused 0 (delta 0)
	remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
	To github.com:suspect-devices/errata_physical_computing.git
	   57401a6..2cc1d07  master -> master
	
Check the GitHub repos recent deliveries at the bottom of Settings->Webhooks->Manage Webhook
[[Image( TaskAddGitHubRepo:webhook-log.png,100%)]]
Browse the code changes on the git/trac server.
[[Image( TaskAddGitHubRepo:changes-in-trac.png)]]

## References
* https://serverdocs.suspectdevices.com/tracdocs/wiki/TracRepositoryAdmin
* https://github.com/trac-hacks/trac-github