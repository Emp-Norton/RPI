Note: 

On many microcontrollers, certain peripherals like SPI can only work with specific combinations of pins. For example, the Pico has two hardware SPI peripherals (SPI0 and SPI1), and each can only use certain GPIO pins for MISO, MOSI, and SCK.

For SPI0:

SCK can be GP2, GP6, or GP18
MOSI can be GP3, GP7, or GP19
MISO can be GP0, GP4, or GP16
For SPI1:

SCK can be GP10, GP14, or GP26
MOSI can be GP11, GP15, or GP27
MISO can be GP8, GP12, or GP28

So if you're using SPI0 and choose GP2 for SCK, you need to make sure you're using compatible pins for MISO and MOSI from the SPI0 group. You can't mix pins between SPI0 and SPI1.
