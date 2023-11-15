"""
Note: This is not finished as I couldnt get larger fonts to wor with the display. Therefor I used another solution.


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
import json
import time
import config
from urequests import get, post

URL_RE = re.compile(r'http://([A-Za-z0-9\-\.]+)(?:\:([0-9]+))?(/.+)?')
URI = namedtuple('URI', ('hostname', 'port', 'path'))


#cache = {}
'''entities = [
    "sensor.tempwithms",
    "sensor.satenas_luftfuktighet"
]
'''

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
  #uri = urlparse(config.host)
  #print("URI: " + uri)
  
  #curl   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3YWQyZmQ0Y2U5NDA0ZD
  #VkYjMzYTBhZWU1ZGQ2ODc4MCIsImlhdCI6MTY4ODYyNTkyMiwiZXhwIjoyMDAzOTg1OTIyfQ.rqs1s21lNIPPovpAjEP5wMvKOpTFdJdML-4LikOcc4Y"
  #-H "Content-Type: application/json"   http://192.168.1.10:8123/api/states
  
  url = "http://192.168.1.10:8123/api/"
  headers = {
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3YWQyZmQ0Y2U5NDA0ZDVkYjMzYTBhZWU1ZGQ2ODc4MCIsImlhdCI6MTY4ODYyNTkyMiwiZXhwIjoyMDAzOTg1OTIyfQ.rqs1s21lNIPPovpAjEP5wMvKOpTFdJdML-4LikOcc4Y",
      "content-type": "application/json",
  }
  response = get(url, headers=headers)
  print(response.text)
  
  url = "http://192.168.1.10:8123/api/config/core/check_config"
  response = post(url, headers=headers)
  print(response.text)
  
  '''
  # This doesnt fit in memory
  url = "http://192.168.1.10:8123/api/states"
  response = get(url, headers=headers)
  print(response.text)
  '''
  url = "http://192.168.1.10:8123/api/states/sensor.satenas_luftfuktighet"
  response = get(url, headers=headers)
  print(response.text)
  
  
  #print("< {}".format(response))
  #outp = (json.loads(response))          
  #print(outp[0].text)
  #print(response.text)
  
  #assert uri
  #path = uri.path or '/' + 'socket.io/?EIO=3'

  '''
  ws_uri = 'ws://{hostname}:{port}{path}'.format(
      hostname=uri.hostname,
      port=uri.port,
      path=path)
  
  print("ws_uri: " + ws_uri)
  
  with uwebsockets.client.connect(ws_uri) as websocket:
    greeting = websocket.recv()
    print("< {}".format(greeting))
    
    tokenmess = "{\"type\":\"auth\",\"access_token\":\"" + config.token + "\"}"    
    print ("Tokenmess: " + tokenmess)    
    websocket.send(tokenmess)
    resp = websocket.recv()
    print("< {}".format(resp))
    
    # Try a ping response:
    pingmess = "{\"id\": 1,\"type\": \"ping\"}"
    print (pingmess)    
    websocket.send(pingmess)
    resp = websocket.recv()
    print("< {}".format(resp))

<<<<<<< HEAD

=======
>>>>>>> 8ba86a4706f3142b89a04d4b1c0553d9233648b9
    
    # We cant fetch all states, the response message is to large
    #statemess = "{\"id\": 21, \"type\": \"get_states\"}"
    statemess = "{\"id\": 26, \"type\": \"get_single_entity\", \"entity_to_get\": \"media_player.vardagsrum\"}"
    #mess = "{\"id\": 22, \"type\": \"subscribe_events\"}"
    print (statemess)    
    websocket.send(statemess)
    resp = websocket.recv()
    print("< {}".format(resp))
    
    
    mess = "{\"id\": 28,\"type\": \"subscribe_events\"}"
    print (mess)    
    websocket.send(mess)
    resp = websocket.recv()
    print("< {}".format(resp))

    while True:
      message = websocket.recv() # This is blocking
      if message is None:
        pass
      else: 

          if len(message) > 0:
              outp = (json.loads(message))          
              if "event" in outp:
                if "data" in outp['event']:
                  if "new_state" in outp['event']['data']:
                    if "sensor.tempwithms" in outp['event']['data']['entity_id']:
                      print("ent: " + outp['event']['data']['entity_id'])
                      print(outp['event']['data']['new_state']['state'])
                      value = outp['event']['data']['new_state']['state']
                      print()
                      display.text(font1, value, 20, 70, st7789.GREEN, st7789.BLACK)

                      
                    if "binary_sensor.ikea_of_sweden_tradfri_motion_sensor_16f699fe_on_off" in outp['event']['data']['entity_id']:
                      print("ent: " + outp['event']['data']['entity_id'])
                      print(outp['event']['data']['new_state']['state'])
                      print()
            
     '''   
        
  #mess = "{\"id\": 19,\"type\": \"unsubscribe_events\", \"subscription\": 18}"
  #print (mess)    
  #websocket.send(mess)
  #websocket.close()
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
    

        

