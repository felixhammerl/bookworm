sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"072f\", ATTRS{idProduct}==\"2200\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'

sudo udevadm control -R
