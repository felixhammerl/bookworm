from pathlib import Path
from threading import Timer
from urllib.parse import unquote, urlparse

import nfc

from bookworm.config import config
from bookworm.util.logger import LogEvents, get_logger

log = get_logger()


class NFCReader:
    def __init__(self, card_present, card_removed):
        self.card_present = card_present
        self.card_removed = card_removed
        self.reader = nfc.ContactlessFrontend()
        if not self.reader.open("usb"):
            log.error(event=LogEvents.NFC_DEVICE_NOT_FOUND)

        log.info(event=LogEvents.NFC_DEVICE_INITIALIZED, device=self.reader.device)

    def connect(self):
        self.reader.connect(
            rdwr={
                "on-connect": self.on_connect,
                "on-release": self.on_release,
            }
        )

    def on_connect(self, tag):
        self.tag = tag
        if not tag.ndef:
            log.warn(event=LogEvents.TAG_NO_NDEF_RECORDS)
            return True

        log.info(event=LogEvents.NFC_TAG_CONNECTED, ndef_records=tag.ndef.records)

        file = Path(unquote(urlparse(tag.ndef.records[0].text).path))
        self.card_present(file)
        return True

    def check_card_presence(self):
        if self.reader.sense(self.tag):
            Timer(0.5, self.check_card_presence).start()
            return

        log.info(event=LogEvents.NFC_TAG_REMOVED)
        self.card_removed()
        Timer(0.5, self.connect).start()

    def on_release(self):
        Timer(0.5, self.check_card_presence).start()
        return True
