from machine import Pin, I2C, reset, unique_id
from time import sleep
from boot import load_config
from umqttsimple import MQTTClient
from ubinascii import hexlify
from ssd1306_flipped import SSD1306_I2C
from mq9 import MQ

width = 64
height = 48
pin_scl = 5
pin_sda = 4
frequency = 100000
       
i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda), freq=frequency)
oled = SSD1306_I2C(width, height, i2c)
topic4 = b'LPG'
topic5 = b'CO'
topic6 = b'METHANE'

def connect_to_mqtt(config):
  global client_id
  client = MQTTClient(client_id, config['mqtt']['broker'])
  client.connect()
  print('Connected to %s MQTT broker' % (config['mqtt']['broker']))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()
  
# Main loop that will run forever:
def mainloop(config):
  
    try:
        client = connect_to_mqtt(config)
    except OSError as e:
        restart_and_reconnect()

    while True:
        mq = MQ()
        perc = mq.MQPercentage()
        gas_lpg = perc["GAS_LPG"]
        co = perc["CO"]
        methane = perc["SMOKE"]
        oled.fill(0)
        oled.show()
        oled.text("LP", 0, 0)
        oled.text(str(float("%.2g" % gas_lpg)), 24, 0)
        oled.text("CO", 0, 10)
        oled.text(str(float("%.2g" % co)), 24, 10 )
        oled.text("ME", 0, 20)
        oled.text(str(float("%.2g" % methane)), 24, 20)
        oled.show()
        print(gas_lpg)
        print(co)
        print(methane)
        client.publish(topic4, str(gas_lpg))
        client.publish(topic5, str(co))
        client.publish(topic6, str(methane))
        sleep(10)
            
if __name__ == "__main__":
    config = load_config()
    client_id = hexlify(unique_id())    
    mainloop(config)
