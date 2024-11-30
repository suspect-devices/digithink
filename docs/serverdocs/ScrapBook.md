<!-- MigrateUsers, Version: 1, Modified: 2018/12/02, Author: trac -->
# Scrapbook
### Migrate Users UID/GID
YOU ARE HERE (Consolidate this into a scraps)
```
chown --from=1000:1000 999:999 /. -Rv
```

### clone drives and change uuids

```
screen dd if=/dev/sda of=/dev/sdj bs=1M status=progress
apt install uuid-runtime
printf '%s\n' p x i $(uuidgen) r w | sudo fdisk /dev/sdj
e2fsck -f /dev/sdj2
tune2fs -U $(uuidgen) /dev/sdj2
blkid
```