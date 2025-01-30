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
	mount_path (str): String representing where the virtual file system will mount the sdcard module FS.

    Example:
    >>> import board
    >>> sd_card = SDCardModule(sck=board.GP11, miso=board.GP9,
				mosi=board.GP8, cs=board.GP10)
    """
    def __init__(self, miso, mosi, cs, sck, mount_path="/sd"):
        self.miso = miso
	self.mosi = mosi
	self.cs = cs
	self.sck = sck
	self.mount_path = mount_path

    def __init_spi(self):
	try:
	    self.spi = busio.SPI(self.sck, MOSI=self.mosi, MISO=self.miso)

	except Exception as e:
	    print(f"Failed to initialize SPI object: {e}")

    def __init_sdcard(self):
	try:
	    self.sdcard = sdcardio.SDCard(self.spi, self.cs)

	except Exception as e:
	    print(f"Failed to create SDCard object: {e}")

    def __init_virtual_fs(self):
	try:
	    self.vfs = storage.VfsFat(sdcard)

	except Exception as e:
	    print(f"Failed to virtualize filesystem: {e}")

    def __mount_vfs(self):
	try:
	    storage.mount(self.vfs, self.mount_path)

	except Exception as e:
	    print(f"Unable to mount {self.mount_path}: {e}")

    def list_files(self, path=self.mount_path, recursive=False):
	def recurse_dirs(dirs):
	    for dir in dirs:
                recurse_dirs(os.listdir(dir))

	if recursive:
            dirs = os.listdir(path)
	    recurse_dirs(dirs)
	else:
	    print(f"{os.listdir(path)}")
