# SSACLI - hp's utilities for configuring its hardware raid controller

## Install ssacli

Note: for the hp recommended way to get the signatures see [the buildnotes for tx2022](Buildnotes/tina/)

```
echo "deb [trusted=yes] https://downloads.linux.hpe.com/SDR/repo/mcp/debian bookworm/current non-free" >>/etc/apt/sources.list
apt install gpg
apt install curl
curl -x http://192.168.31.2:3128/ -fsSL https://downloads.linux.hpe.com/SDR/hpPublicKey2048.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpPublicKey2048.gpg
curl -x http://192.168.31.2:3128/ -fsSL https://downloads.linux.hpe.com/SDR/hpePublicKey2048_key1.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpePublicKey2048_key1.gpg
curl -x http://192.168.31.2:3128/-fsSL https://downloads.linux.hpe.com/SDR/hpPublicKey2048_key1.pub | gpg --dearmor -o /etc/apt/trusted.gpg.d/hpPublicKey2048_key1.gpg
apt update
apt install ssacli
```
## Using ssacli

### Using ssacli to set the primary boot disk.

```sh
=> set target ctrl slot=0

   "controller slot=0"

=> show config detail
... find the drive that coresponds to what you want

=> ld 10 modify bootvolume=primary
=>
```

###

To recover if the selected drive does not boot log into the ilo.

```sh
</>hpiLO-> power reset

status=0
status_tag=COMMAND COMPLETED
Thu Nov 28 17:04:30 2024

Server resetting .......

</>hpiLO-> vsp
```

Wait for the eternity it takes to run through the hardware and memory on the hp. Once it gets to the actual bios change to the text console.

```sh
<ESC>(
</>hpiLO-> textcons
```

The text console is nice because (inspite of char set differences) the function keys work. Press f8 when you get to the raid controller (after it searches for the disks)

Text console will not work until it actually gets to the bios and you can switch back to the VSP by escaping out 

```sh
<ESC>(
</>hpiLO-> vsp

Virtual Serial Port Active: COM2
```

## References

- https://www.n0tes.fr/2024/03/04/CLI-HPE-ssacli-and-hpssacli-tools/
