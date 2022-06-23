```shell
Hoffa:~ don$ brew install lxc
Hoffa:~ don$ lxc remote add costello.local
Certificate fingerprint: c7b38e549c397aa9d5e63489bf9a5f3987ec8d67dada692cafdecca924d4b8bf
ok (y/n/[fingerprint])? y
Admin password for costello.local:
Client certificate now trusted by server: costello.local
Hoffa:~ don$ lxc remote set-default costello.local
Hoffa:~ don$ lxc remote list
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
|           NAME           |                   URL                    |   PROTOCOL    |  AUTH TYPE  | PUBLIC | STATIC | GLOBAL |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
| costello.local (current) | https://costello.local:8443              | lxd           | tls         | NO     | NO     | NO     |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
| images                   | https://images.linuxcontainers.org       | simplestreams | none        | YES    | NO     | NO     |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
| local                    | unix://                                  | lxd           | file access | NO     | YES    | NO     |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
| ubuntu                   | https://cloud-images.ubuntu.com/releases | simplestreams | none        | YES    | YES    | NO     |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+
| ubuntu-daily             | https://cloud-images.ubuntu.com/daily    | simplestreams | none        | YES    | YES    | NO     |
+--------------------------+------------------------------------------+---------------+-------------+--------+--------+--------+

```