sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"072f\", ATTRS{idProduct}==\"2200\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'

sudo udevadm control -R


# NFC Targets

brty = bitrate and type

bitrate is in kbit/s, e.g. 106 for NTAG215 chips
type is the NFC type A for NTAG215 chips


## Types

See: https://www.rfwireless-world.com/Terminology/NFC-A-vs-NFC-B-vs-NFC-F.html

NFC-A
The signalling type NFC-A is based on ISO/IEC 14443A. It is similar to RFID type A. In the type-A based communication delay encoding (miller encoding) technique is employed along with AM modulation. Here binary data is transmitted with the data rate of about 106 Kbps using type A communication. Here binary signal must change from 0 % to 100 % to distinguish between binary 1 and binary 0 data informations.

NFC-B
The signalling type NFC-B is based on ISO/IEC 14443B. It is similar to RFID type B. Here manchester encoding technique is employed. Here instead of 100%, AM modulationat 10% is used. This convention is used to distinguish between binary 1 and 0. 10% change from 90% for binay 0 (i.e. low) and 100% for binary 1 ( i.e high) is used.
In manchester coding zero cross over happens in the bit period used to represent both 0 and 1. Here a low to high transition represents binary 0 bit and high to low transition represents binary 1 bit. It is recommended to have the zero cross over in the middle of the bit period.

NFC-F
The signalling type NFC-F is based on FeliCA JIS X6319-4. It is the faster form of RFID communication. It is alse known as FeliCa. It is the technology most popularly used in Japan. It is used for variety of applications such as creadit card or debit card based payments, subway ticketing for access control to the trains, personal identification at the office and residential flats etc.
