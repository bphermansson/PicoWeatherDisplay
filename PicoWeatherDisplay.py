"""
Pico Weather Display
Download the file st7789py.py from https://github.com/russhughes/st7789py_mpy/tree/master/lib and
open it in Thonny, then save it to the Pico.

Connections:
CS - GND
DC - GP13
RST - GP12
SDA - GP11
SCL - GP10
VCC - 3V3
GND - GND

"""

import machine
import st7789py as st7789
from fonts import vga1_16x32 as font1

spi1_sck=10
spi1_mosi=11
st7789_res = 12
st7789_dc  = 13
disp_width = 320
disp_height = 240
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
display = st7789.ST7789(spi1, disp_width, disp_height,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          rotation=0)

display.text(font1, "Welcome!", 20, 140, st7789.GREEN, st7789.BLACK)

