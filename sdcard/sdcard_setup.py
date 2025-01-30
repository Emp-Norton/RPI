import board, busio, os, sdcardio, storage

MISO, CS, SCK, MOSI = board.GP8, board.GP9, board.GP10, board.GP11

spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP8)

sdcard = sdcardio.SDCard(spi, CS)
vfs = storage.VfsFat(sdcard)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

os.listdir()


class SDCardModule:
    """
    Convenience class to facilitate setting up SDCard storage for Raspberry Pi Pico.
    Expects serial peripheral interface (SPI) only at this time.

    Args:
        miso (microcontroller.Pin): The MISO (Master In Slave Out) pin, e.g., board.GP9
	mosi (microcontroller.Pin): The MOSI (Master Out Slave In) pin, e.g., board.GP8
	sck  (microcontroller.Pin): The SCLK (Serial Clock) pin, e.g., board.GP11
	cs   (microcontroller.Pin): The CS (Chip Select) pin, e.g., board.GP10

    Example:
    >>> import board
    >>> sd_card = SDCardModule(sck=board.GP11, miso=board.GP9,
				mosi=board.GP8, cs=board.GP10)
    """
