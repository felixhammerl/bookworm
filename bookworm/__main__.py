import signal
import asyncio
from bookworm.service.nfc import NFCReader
from bookworm.util.logger import LogEvents, get_logger

log = get_logger()

RUN_FLAG = True


async def shutdown():
    global RUN_FLAG
    log.info(event=LogEvents.SIGNAL_RECEIVED)
    RUN_FLAG = False


async def main() -> int:
    global RUN_FLAG
    log.info(event=LogEvents.STARTUP)
    card_present = lambda: log.warn(event=LogEvents.NFC_CARD_PRESENT)
    card_removed = lambda: log.warn(event=LogEvents.NFC_CARD_REMOVED)
    nfc_reader = NFCReader(card_present=card_present, card_removed=card_removed)
    nfc_reader.connect()
    while RUN_FLAG:
        await asyncio.sleep(0.1)
    return 0


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    signal.signal(signal.SIGINT, lambda _, __: asyncio.create_task(shutdown()))
    signal.signal(signal.SIGTERM, lambda _, __: asyncio.create_task(shutdown()))
    loop.run_until_complete(main())
