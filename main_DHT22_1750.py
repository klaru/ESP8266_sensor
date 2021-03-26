from machine import Pin, I2C, reset, unique_id, freq
from time import sleep
from boot import load_config
from umqttsimple import MQTTClient
from ubinascii import hexlify
from ssd1306_flipped import SSD1306_I2C
from dht import DHT22
import bh1750fvi

QOS=0
# select GPIO pins
if freq() > 80000000:   # ESP32
    pin_scl = 22
    pin_sda = 21
    pin_sens = 16
else:                   # ESP8266
    pin_scl = 5
    pin_sda = 4
    pin_sens = 2

width = 64
height = 48
frequency = 100000
OP_SINGLE_HRES2 = 0x21
       
i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda), freq=frequency)
oled = SSD1306_I2C(width, height, i2c)
sensor_Pin = Pin(pin_sens, Pin.IN)
sensor = DHT22(sensor_Pin)
topic1 = b'TempDHT22-2'
topic2 = b'HumidDHT22-2'
topic3 = b'Light'

client_id = hexlify(unique_id())

def connect_to_mqtt(config):
  global client_id  client = MQTTClient(client_id, config['mqtt']['broker'])
  client.connect()
  print('Connected to %s MQTT broker' % (config['mqtt']['broker']))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()
  
# Main loop that will run forever:
def main(config):
  
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
        light = bh1750fvi.sample(i2c, mode=OP_SINGLE_HRES2)
        oled.text("Temp=", 0, 0)
        oled.text(str(temperature)+" C", 0, 10)
        oled.text("Humid=", 0, 20)
        oled.text(str(humidity)+" %", 0, 30)
        oled.text("Lux="+str(light), 0, 40)
        oled.show()
        print(temperature)
        print(humidity)
        print(light)
        try:
            client.publish(topic1, str(temperature), qos=QOS)
            client.publish(topic2, str(humidity), qos=QOS)
            client.publish(topic3, str(light), qos=QOS)
        except OSError:
            restart_and_reconnect()
        sleep(10)
            
if __name__ == "__main__":
    main(load_config())
