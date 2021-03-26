from machine import Pin, I2C, reset, unique_id
from time import sleep
from boot import load_config
from umqttsimple import MQTTClient
from ubinascii import hexlify
from ssd1306_flipped import SSD1306_I2C
from dht import DHT22

width = 64
height = 48
pin_scl = 5
pin_sda = 4
frequency = 100000
       
i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda), freq=frequency)
oled = SSD1306_I2C(width, height, i2c)
pin2 = Pin(2, Pin.IN)
sensor = DHT22(pin2)
topic1 = b'TempDHT22-2'
topic2 = b'HumidDHT22-2'

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
    except OSError:
        restart_and_reconnect()

    while True:
        oled.fill(0)
        oled.show()
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        oled.text("Temp =", 0, 0)
        oled.text(str(temperature)+" C", 0, 10)
        oled.text("Humid =", 0, 20)
        oled.text(str(humidity)+" %", 0, 30)
        oled.show()
        print(temperature)
        print(humidity)
        try:
            client.publish(topic1, str(temperature))
            client.publish(topic2, str(humidity))
        except OSError:
            restart_and_reconnect()
        sleep(10)
            
if __name__ == "__main__":
    config = load_config()
    client_id = hexlify(unique_id())    
    mainloop(config)
