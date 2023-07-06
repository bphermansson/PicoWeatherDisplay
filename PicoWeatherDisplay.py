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
import chango_32 as c32
import chango_64 as c64
import boot

print ("main")

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


def main():
  print(boot.newip)
  display.text(font1, "Welcome!", 20, 40, st7789.GREEN, st7789.BLACK)
  print(boot.newip[0])
  
  display.text(font1, boot.newip[0], 20, 60, st7789.GREEN, st7789.BLACK)
  display.write(c64, boot.newip[0], 20, 60, st7789.GREEN, st7789.BLACK)
  display.write(c32, boot.newip[0], 20, 120, st7789.GREEN, st7789.BLACK)


if __name__ == "__main__":
    main()