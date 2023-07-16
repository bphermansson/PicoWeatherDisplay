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

Web sockets code in folder uwebsockets from https://github.com/danni/uwebsockets/blob/esp8266/examples/client.py.


"""

import machine
import st7789py as st7789
from fonts import vga1_16x32 as font1
import chango_32 as c32
'''import chango_64 as c64'''
import boot
import ure as re
from ucollections import namedtuple
import uwebsockets.client

URL_RE = re.compile(r'http://([A-Za-z0-9\-\.]+)(?:\:([0-9]+))?(/.+)?')
URI = namedtuple('URI', ('hostname', 'port', 'path'))

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3YWQyZmQ0Y2U5NDA0ZDVkYjMzYTBhZWU1ZGQ2ODc4MCIsImlhdCI6MTY4ODYyNTkyMiwiZXhwIjoyMDAzOTg1OTIyfQ.rqs1s21lNIPPovpAjEP5wMvKOpTFdJdML-4LikOcc4Y"
host = "192.168.1.10"
port = 8123
cache = {}
entities = [
    "sensor.tempwithms",
    "sensor.satenas_luftfuktighet"
]

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

def urlparse(uri):
    """Parse http:// URLs"""
    match = URL_RE.match(uri)
    if match:
        return URI(match.group(1), int(match.group(2)), match.group(3))

def connect():
  uri = "http://192.168.1.10:8123/api/websocket"
  uri = urlparse(uri)
  print(uri)
  assert uri
  path = uri.path or '/' + 'socket.io/?EIO=3'

  ws_uri = 'ws://{hostname}:{port}{path}'.format(
      hostname=uri.hostname,
      port=uri.port,
      path=path)
  
  print("ws_uri: " + ws_uri)
 
  with uwebsockets.client.connect(ws_uri) as websocket:
    greeting = websocket.recv()
    print("< {}".format(greeting))
    
    mess = "{\"type\":\"auth\",\"access_token\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3YWQyZmQ0Y2U5NDA0ZDVkYjMzYTBhZWU1ZGQ2ODc4MCIsImlhdCI6MTY4ODYyNTkyMiwiZXhwIjoyMDAzOTg1OTIyfQ.rqs1s21lNIPPovpAjEP5wMvKOpTFdJdML-4LikOcc4Y\"}"
    print (mess)    
    websocket.send(mess)
    resp = websocket.recv()
    print("< {}".format(resp))
    
    # Try a ping response:
    mess = "{\"id\": 1,\"type\": \"ping\"}"
    print (mess)    
    websocket.send(mess)
    resp = websocket.recv()
    print("< {}".format(resp))

    '''
    mess = "{\"id\": 3, \"type\": \"get_states\"}"
    print (mess)    
    websocket.send(mess)
    resp = websocket.recv()
    print("< {}".format(resp))
    '''
    #mess = "{'id': 4, 'type': 'subscribe_trigger','trigger': {'platform': 'state','entity_id': 'binary_sensor.motion_occupancy','from': 'off', 'to':'on'}"
    mess = "{\"id\": 18,\"type\": \"subscribe_events\"}"
    print (mess)    
    websocket.send(mess)
    resp = websocket.recv()
    print("< {}".format(resp))

    while True:
#    try:
      message = websocket.recv() # This is blocking
      if len(message) > 0:
          print (message)
      # do what I need to do here
#   except WebSocketClosedError:
#      break
        
  websocket.close()
  return 1
 
def main():
  print(boot.newip)
  display.text(font1, "Welcome!", 20, 40, st7789.GREEN, st7789.BLACK)
  print(boot.newip[0])

  print(connect())

  display.text(font1, boot.newip[0], 20, 60, st7789.GREEN, st7789.BLACK)
  '''display.write(c64, boot.newip[0], 20, 60, st7789.GREEN, st7789.BLACK)'''
  display.write(c32, boot.newip[0], 20, 120, st7789.GREEN, st7789.BLACK)

  

if __name__ == "__main__":
    main()
    

        
