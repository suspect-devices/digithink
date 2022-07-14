```shell
08:21 <+stgraber> feurig: I believe I made a video about it an MAAS some time ago
08:21 <+stgraber> feurig: anyway, it's basically:
08:22 <+stgraber> lxc init my-pxe --empty --vm
08:22 <+stgraber> lxc config device override my-pxe eth0 boot.priority=10
08:22 <+stgraber> lxc start my-pxe --console=vga
08:22 <+stgraber> the boot.priority step is to have QEMU prefer network boot over local disk
08:23 <+stgraber> you may also want to grow the root disk depending on your needs: lxc config device override my-pxe root size=50GiB
```
