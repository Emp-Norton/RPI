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
        miso (Pin): 
    """
