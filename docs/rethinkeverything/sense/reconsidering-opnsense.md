# Reconsidering OpnSense

My initial tact was to take opnsense and use it as a prototype for the underlying freebsd based software (pf,dnsmasq,usw)
That is the configuration at the colo and it works well in that environment. However recently I started looking at what opnsense out of the box brings to the table. In particular I started looking at the total pile of shit that my centurylink provided router was letting into my network. And I decided that if I was hand rolling pf I would not have caught half of it.

I was in the middle of converting everything to /etc/ethers+/etc/hosts+dnsmasq and I said heck, lets just do the same in opnsense. Then we can look at getting rid of the pile of hot garbage that centurylink is charging me $15 a month for. 

## Well. That didn't work

So I turned on the dnsmasq dns and added all of the hosts in my network to /etc/hosts and /etc/ethers It seemed to work but the next time I did an update it overwrote both files, and stopped resolving the hosts I used most. So the main takaways were. 

1. It seems to work at first.
2. It overwrites your files.
3. You have to manually add everything using the gui.
4. It's not automatable or scriptable.
5. It doesn't work.

So I turned unbound back on and looked at the alternatives.

## You can't configure the software/services but you can run a jail.

So this is going to be a longer process than I would have liked but I have a test system to build the jail on. 


## Linkdump.

- https://forum.opnsense.org/index.php?topic=26975.0
- https://www.reddit.com/r/opnsense/comments/sjewa4/jails_under_opnsense_221/?rdt=59758