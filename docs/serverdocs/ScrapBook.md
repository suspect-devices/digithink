<!-- MigrateUsers, Version: 1, Modified: 2018/12/02, Author: trac -->
# Scrapbook

## Migrate Users UID/GID

```sh
chown --from=1000:1000 999:999 /. -Rv
```

## clone drives and change uuids

```sh
screen dd if=/dev/sda of=/dev/sdj bs=1M status=progress
apt install uuid-runtime
printf '%s\n' p x i $(uuidgen) r w | sudo fdisk /dev/sdj
e2fsck -f /dev/sdj2
tune2fs -U $(uuidgen) /dev/sdj2
blkid
```

## Clean big files out of your git history

```sh
remote: error: Trace: 28fd3d0788632c40d1e72ba92fd845cec66f07e5260e2d9d7e4d0456566214f2
remote: error: See https://gh.io/lfs for more information.
remote: error: File docs/Travel/images/PortAngelesVictoria17oct25/lassothepier.mov is 104.56 MB; this exceeds GitHubs file size limit of 100.00 MB
remote: error: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
To github.com:feurig/3dangst.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'github.com:feurig/3dangst.git'
```

OH NO! And even if you remove it its still in your 'history'

```sh
feurig@MacBookPro PortAngelesVictoria17oct25 % git log --graph --full-history --all --pretty=format:"%h%x09%d%x20%s"
* 4035fc1        (HEAD -> main) shrink the mov
* d1a122c        Rough Draft Current Trip
* 540a25e        (origin/main, origin/HEAD) burgers
* b9685ff        clean up after fucking git.
*   b27e176      Merge branch 'main' of github.com:feurig/3dangst fuck you git
|\
* 4035fc1        (HEAD -> main) shrink the mov
* d1a122c        Rough Draft Current Trip
...
```

The magic below works if you leave the file where it is otherwise it will fail because you have unstaged changes.

```sh
feurig@MacBookPro 3dangst % git filter-branch --tree-filter 'rm -f docs/Travel/images/PortAngelesVictoria17oct25/lassothepier.mov' HEAD
WARNING: git-filter-branch has a glut of gotchas generating mangled history
	 rewrites.  Hit Ctrl-C before proceeding to abort, then use an
	 alternative filtering tool such as 'git filter-repo'
	 (https://github.com/newren/git-filter-repo/) instead.  See the
	 filter-branch manual page for more details; to squelch this warning,
	 set FILTER_BRANCH_SQUELCH_WARNING=1.
Proceeding with filter-branch...

Rewrite 4035fc149ca4c01c080a0ddc7ba14063d0ae846d (27/45) (1 seconds passed, remaining 0 predicted)
Ref 'refs/heads/main' was rewritten
feurig@MacBookPro 3dangst % git log --graph --full-history --all --pretty=format:"%h%x09%d%x20%s"
* 3c2354c        (HEAD -> main) shrink the mov
* fe6ab88        Rough Draft Current Trip
...
* 7631e0f        morestuff
```

Now you can push it.

```sh
feurig@MacBookPro 3dangst % git push
Enumerating objects: 22, done.
Counting objects: 100% (22/22), done.
Delta compression using up to 10 threads
Compressing objects: 100% (18/18), done.
Writing objects: 100% (18/18), 16.30 MiB | 1.28 MiB/s, done.
Total 18 (delta 4), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (4/4), completed with 3 local objects.
To github.com:feurig/3dangst.git
   540a25e..3c2354c  main -> main
```

* <https://www.geeksforgeeks.org/git/how-to-remove-a-large-file-from-commit-history-in-git/>
* <https://stackoverflow.com/questions/2100907/how-can-i-remove-delete-a-large-file-from-the-commit-history-in-the-git-reposito>
* <https://www.baeldung.com/ops/git-remove-file-commit-history>