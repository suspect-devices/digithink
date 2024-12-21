#!/usr/bin/python
"""-------------------------------------------------------------------------clone-repos.py

this is mostly stolen from code here
https://jpmens.net/2019/04/15/i-mirror-my-github-repositories-to-gitea/

Make mirror copies of repos from github and bitbucket.
Author: D. Delmar Davis <don@suspectdevices.com>
Copyleft: (c) 2021 D. Delmar Davis <don@suspectdevices.com>
Liscense: mit
"""
#from github import Github
#import json
import subprocess
#import urllib2

username = "feurig"
repodir = "/var/lib/gitea/gitea-repositories"

from github import Github		# https://github.com/PyGithub/PyGithub
import requests
import json
import sys
import os

repo_map = { "some-github-repo":		"a-gitea-org",
             "another-github-repo":		"another-gitea-org",
           }


#githubrepos=['feurig/arduino-core-105','feurig/Arduino_STM32_MIDI_project',
#    'feurig/Cohen','feurig/ems-light','feurig/ems2','feurig/failandflail',
#    'feurig/libmaple','feurig/libmaplemidi-cma','feurig/maple','feurig/maplebacon',
#    'feurig/midimonster2012','feurig/pubcrawler','feurig/python-dialog',
#    'feurig/redmine-configuration','feurig/rtmidi','feurig/Suspect-Devices-Open-Hardware',
#    'feurig/wsgi-bitbucket-mirror',
#]
# used to create lists of repos
#response = urllib2.urlopen("https://api.bitbucket.org/2.0/repositories/"+username+"?pagelen=100")
#data=json.loads(response.read())['values']
#for record in data:
#    url="git@bitbucket.org:"+username+"/"+record['slug']+".git"
#    print "Cloning :",url
#    subprocess.call(["/usr/bin/git", "clone", "--mirror", url], cwd=repodir)
#git clone git@bitbucket.org:feurig/missinglink-hardware.git


#g = Github()
#user = g.get_user(username)
#for repo in user.get_repos():
#    print"'"+username+"/"+repo.name+"',"
#!/usr/bin/env python

gitea_url = "http://127.0.0.1:3000/api/v1"
gitea_user = "feurig"
gitea_token = open(os.path.expanduser("~/.gitea-token")).read().strip()

session = requests.Session()        # Gitea
session.headers.update({
    "Content-type"  : "application/json",
    "Authorization" : "token {0}".format(gitea_token),
})

github_username = "feurig"
github_token = open(os.path.expanduser("~/.github-token")).read().strip()
gh = Github(github_token)

for repo in gh.get_user().get_repos():
    # Mirror to Gitea if I haven't forked this repository from elsewhere
    #if not repo.fork:
        print("* mirroring ",repo.full_name)
        real_repo = repo.full_name.split('/')[1]
        if real_repo in repo_map:
            # We're creating the repo in another account (most likely an organization)
            gitea_dest_user = repo_map[real_repo]
        else:
            gitea_dest_user = repo.full_name.split('/')[0]

        r = session.get("{0}/users/{1}".format(gitea_url, gitea_dest_user))
        if r.status_code != 200:
            print("Cannot get user id for '{0}'".format(gitea_dest_user), file=sys.stderr)
            exit(1)

        gitea_uid = json.loads(r.text)["id"]

        m = {
            "repo_name"         : "{0}".format(real_repo),
            "description"       : repo.description or "not really known",
            "clone_addr"        : repo.clone_url,
            "mirror"            : True,
            "private"           : repo.private,
            "uid"               : gitea_uid,
        }

        if repo.private:
            m["auth_username"]  = github_username
            m["auth_password"]  = "{0}".format(github_token)

        jsonstring = json.dumps(m)

        r = session.post("{0}/repos/migrate".format(gitea_url), data=jsonstring)
        if r.status_code != 201:            # if not CREATED
            if r.status_code == 409:        # repository exists
                continue
            print(r.status_code, r.text, jsonstring)

bitbucket_username = "feurig"
bitbucket_token = open(os.path.expanduser("~/.bit-bucket-token")).read().strip()
bitbucketrepos=['feurig/ems-light','feurig/musicbox','feurig/straight-from-hell.com',
       'feurig/trashterm','feurig/missinglink-hardware','feurig/bnc-proprietary',
       'feurig/ems-firmware','feurig/ems-golang','feurig/ems-framework',
       'joedumoulin/sesh','suspectdevicesadmin/ansible']


'''
for repo in bitbucketrepos:
'''
