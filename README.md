# Bookworm

This project is a very simple audiobook reader. It is designed to be used with a Raspberry Pi and a NFC reader. The NFC reader is used to select the book to read. The book is read from an m3u playlist and played using the VLC player in a headless mode. The sound is played through the 3.5mm audio jack.

# Getting Started

We are starting from a fresh install of Raspberry OS. My test device was a 4GB Raspberry Pi 4.

## Make sure the system is up to date

```bash
sudo apt update
sudo apt upgrade
git clone https://github.com/felixhammerl/bookworm.git
cd bookworm
```

## Install the dependencies

* make: `sudo apt install make`
* git: `sudo apt install git`
* pyenv: `curl https://pyenv.run | bash`
* poetry: `curl -sSL https://install.python-poetry.org | python3 -`
* VLC: `sudo apt install vlc`

Please note that pyenv and poetry require a restart of the shell to be available. Also, this needs to be added to the `.bashrc` file:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
export PATH="/home/pi/.local/bin:$PATH"
```

Once this is done, you can install the python dependencies:

```bash
make install
```

This should install the required Python dependencies.

## Install the NFC reader

In order to use the NFC reader, we need to give a non-root user access to the device. This is done by adding a rule to the udev system.

```bash
poetry run python -m nfc
```

There should be an output along the lines of:

```
This is the 1.0.4 version of nfcpy run in Python 3.12.9
on Linux-6.6.74+rpt-rpi-v8-aarch64-with-glibc2.36
I'm now searching your system for contactless devices
** found ACS ACR122U PN532v1.6 at usb:001:007
I'm not trying serial devices because you haven't told me
-- add the option '--search-tty' to have me looking
-- but beware that this may break other serial devs
```

This means that the device is found. Remember the USB path, in this case `usb:001:007`.

Now we need to add a rule to the udev system to give access to the device. First, we need to find out the device's USB vendor and device IDs. This can be done with the following command:

```bash
lsusb
```

This should give an output like this:

```
Bus 001 Device 011: ID 072f:2200 Advanced Card Systems, Ltd ACR122U
```

Remember the `072f:2200` part, just be aware that your values may be different! This is the first part is the vendor ID and the second the device ID. We need to add this to the udev rules.

The following commands should do the trick:

```bash
sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"072f\", ATTRS{idProduct}==\"2200\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'

sudo udevadm control -R
```

This should give the user access to the device. You can check this by running the `poetry run python -m nfc` command again. If the device is found, everything is set up correctly.

## NFC Targets

`nfcpy` is not able to communicate with Mifare cards. This is because Mifare cards are not NFC compliant. They are based on the ISO 14443 standard, but they are not fully compliant with it. Make sure you understand this caveat when ordering your cards!

## Playlist files

They playlists for the audio books are simple m3u files. Put your MP3 and your m3u files on a USB stick. The m3u file should contain the path to the MP3 files. The MP3 files should be in the same directory as the m3u file.

In order to make sure that your MP3 files are in the correct path, you can figure out the device and edit `/etc/fstab` to mount the device at the correct path. First, get the device identifier via `lsblk` (to identify the device) and `blkid` (to get the UUID). Then, add the device to the `/etc/fstab` file. Here is an example:

```
UUID=B11B-1E14 /mnt/usb0 vfat defaults,auto,users,rw,nofail,umask=000 0 0
```

Please be careful when editing the `/etc/fstab` file. Incorrect entries can lead to a non-bootable system.

## NFC writing

I use NFC Tools for macOS and Android to write the NFC tags. The tags should contain a single NDEF entry with a file URI, pointing to the m3u playlist file.

## Let's go!

To start it manually, run:


```bash
poetry run python -m bookworm
```

To start it automatically upon device start, add it as a systemd service:

```bash
sudo cp bookworm.service /etc/systemd/system/bookworm.service
sudo systemctl daemon-reload
sudo systemctl start bookworm
sudo systemctl enable bookworm
```

That's it! You should now be able to scan your NFC tags and listen to your audiobooks.

# About NFC

If you're as clueless as I am about NFC, here are some notes that might help you understand the NFC reader a bit better.

`nfcpy` is a Python library that allows you to interact with NFC devices. In order to scan for a card, you can specify targets. The `brty` parameter is a shorthand for "bitrate and type", tuple with two values. The first value is the bitrate in kbit/s (e.g. 106 for NTAG215 chips) and the second value is the NFC type (e.g. NFC type A for NTAG215 chips). The bitrate is an integer and the NFC type is a string. The NFC type can be `A`, `B`, or `F`.

See: https://www.rfwireless-world.com/Terminology/NFC-A-vs-NFC-B-vs-NFC-F.html

### NFC-A
The signalling type NFC-A is based on ISO/IEC 14443A. It is similar to RFID type A. In the type-A based communication delay encoding (miller encoding) technique is employed along with AM modulation. Here binary data is transmitted with the data rate of about 106 Kbps using type A communication. Here binary signal must change from 0 % to 100 % to distinguish between binary 1 and binary 0 data informations.

### NFC-B
The signalling type NFC-B is based on ISO/IEC 14443B. It is similar to RFID type B. Here manchester encoding technique is employed. Here instead of 100%, AM modulationat 10% is used. This convention is used to distinguish between binary 1 and 0. 10% change from 90% for binay 0 (i.e. low) and 100% for binary 1 ( i.e high) is used.
In manchester coding zero cross over happens in the bit period used to represent both 0 and 1. Here a low to high transition represents binary 0 bit and high to low transition represents binary 1 bit. It is recommended to have the zero cross over in the middle of the bit period.

### NFC-F
The signalling type NFC-F is based on FeliCA JIS X6319-4. It is the faster form of RFID communication. It is alse known as FeliCa. It is the technology most popularly used in Japan. It is used for variety of applications such as creadit card or debit card based payments, subway ticketing for access control to the trains, personal identification at the office and residential flats etc.
