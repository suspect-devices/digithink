# Universal remote (NOTES/WIP).

This probably belongs elsewhere but I want to (un)mute/power(on/off) the tv and the radio from anywhere in the house


## Recieving data from the remote

The remote I bought on ebay seems to send 4 different signals per key (in this case the mute key)

```sh
root@breedx:/etc/lirc# ir-keytable -t -s rc2
Testing events. Please, press CTRL-C to abort.
91839.612032: lirc protocol(nec): scancode = 0x801e
91839.612055: event type EV_MSC(0x04): scancode = 0x801e
91839.612055: event type EV_SYN(0x00).
91839.720033: lirc protocol(nec): scancode = 0x47
91839.720052: event type EV_MSC(0x04): scancode = 0x47
91839.720052: event type EV_SYN(0x00).
91839.828035: lirc protocol(nec): scancode = 0x820c
91839.828064: event type EV_MSC(0x04): scancode = 0x820c
91839.828064: event type EV_SYN(0x00).
91839.932028: lirc protocol(necx): scancode = 0xc89120
91839.932045: event type EV_MSC(0x04): scancode = 0xc89120
91839.932045: event type EV_SYN(0x00).
```

The remote that came with the radio is more specific (0x45=KEY_POWER,0x47=KEY_MUTE)

```sh
root@breedx:/etc/lirc# ir-keytable -t -s rc2
Testing events. Please, press CTRL-C to abort.
92054.632034: lirc protocol(nec): scancode = 0x45
92054.632065: event type EV_MSC(0x04): scancode = 0x45
92054.632065: event type EV_SYN(0x00).
92054.680040: lirc protocol(nec): scancode = 0x45 repeat
92054.680060: event type EV_MSC(0x04): scancode = 0x45
92054.680060: event type EV_SYN(0x00).
92061.396035: lirc protocol(nec): scancode = 0x47
92061.396058: event type EV_MSC(0x04): scancode = 0x47
92061.396058: event type EV_SYN(0x00).
```

Which is different than the remote for the tv (0x408=KEY_POWER,0x404=KEY_MUTE)

```sh
92119.628035: lirc protocol(nec): scancode = 0x408
92119.628061: event type EV_MSC(0x04): scancode = 0x408
92119.628061: event type EV_SYN(0x00).
92126.468036: lirc protocol(nec): scancode = 0x404
92126.468057: event type EV_MSC(0x04): scancode = 0x404
92126.468057: event type EV_SYN(0x00).
```

## links

<https://spotpear.com/index.php/index/study/detail/id/843.html>
<https://unix.stackexchange.com/questions/227829/how-to-add-lirc-to-ir-keytable-protocols>
<https://www.sbprojects.net/knowledge/ir/nec.php>
<https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581>
<https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_Infrared_Remote_Control>
<https://askubuntu.com/questions/951432/ir-remote-some-media-keys-wont-work-key-nextsong-key-previoussong>
<https://lirc.readthedocs.io/en/latest/configuring-system-lirc.html>
<https://www.infradead.org/~mchehab/kernel_docs/userspace-api/media/rc/rc-protos.html>
<https://github.com/LibreELEC/documentation/blob/master/configuration/ir-remotes.md>
<https://stackoverflow.com/questions/58636136/ir-remote-control-using-lirc-nec>
<https://github.com/gordonturner/ControlKit/blob/master/Raspbian%20Setup%20and%20Configure%20IR.md>
<https://blog.gordonturner.com/2020/06/10/raspberry-pi-ir-transmitter/>
<https://www.instructables.com/Setup-IR-Remote-Control-Using-LIRC-for-the-Raspber/>
<https://aron.ws/projects/lirc_rpi/openelec_howto.html>
<https://projects-raspberry.com/raspberry-pi-as-ir-remote-lirc/#google_vignette>
<https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581>
<https://zaman.is-a.dev/posts/how-to-use-raspberry-pi-as-infrared-ir-remote/>
<https://www.drejo.com/blog/arduino-lirc/>
