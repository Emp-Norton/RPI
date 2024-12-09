import time
import board
import busio
import displayio
from adafruit_ssd1306 import SSD1306_I2C

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the display object
oled = SSD1306_I2C(128, 32, i2c)

# Clear the display to start fresh
oled.fill(0)
oled.show()

# Create a bitmap and a display context
bitmap = displayio.Bitmap(128, 32, 1)  # 128x32 monochrome display
palette = displayio.Palette(1)
palette[0] = 0xFFFFFF  # White color for the text

# Create a Group to hold the bitmap
tilegrid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tilegrid)

# Display the group
oled.show(group)

# Create a text object and draw it
from adafruit_display_shapes.rect import Rect
import adafruit_displayio_ssd1306

# Write some text on the OLED
oled.fill(0)  # Clear screen
oled.show()

# Display some text
oled.text("Hello, World!", 0, 0)
oled.text("CircuitPython!", 0, 10)
oled.text("Raspberry Pi Pico", 0, 20)

# Update display
oled.show()

time.sleep(2)
