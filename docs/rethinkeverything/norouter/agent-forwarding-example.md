This is an example of using agent forwarding to access hosts on the admin lan.


```
feurig@Amyl ~ % ssh-add
Identity added: /Users/feurig/.ssh/id_rsa (feurig@nix.lan)
feurig@Amyl ~ % ssh -A sitka.suspectdevices.com
Last login: Sat Oct 12 20:39:27 2024 from 209.66.79.150
FreeBSD 14.1-RELEASE (GENERIC) releng/14.1-n267679-10e31f0946d8

Welcome to FreeBSD!
...
feurig@sitka:~ $ ssh root@192.168.31.158
The authenticity of host '192.168.31.158 (192.168.31.158)' can't be established.
ED25519 key fingerprint is SHA256:GFIX+l6M/OOI5BJVWK1U1H5lKzDCkzbXNEgX1Sn7rK0.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.31.158' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-45-generic  x86_64)
...
Last login: Sat Oct 12 20:29:44 2024 from 192.168.31.228
root@kh2024:~#
```

```
Connection to virgil.suspectdevices.com closed.
feurig@Amyl ~ % ssh -A feurig@virgil
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-45-generic x86_64)
...
feurig@virgil:~$ ssh 192.168.31.2
The authenticity of host '192.168.31.2 (192.168.31.2)' can't be established.
ED25519 key fingerprint is SHA256:pEu5SYscD/+jLLcwzoyPcemXS2AyuOkF9zkC5r5WjDg.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.31.2' (ED25519) to the list of known hosts.
Last login: Sat Oct 12 20:40:09 2024 from 209.66.79.150
FreeBSD 14.1-RELEASE (GENERIC) releng/14.1-n267679-10e31f0946d8
...
feurig@sitka:~ $
```