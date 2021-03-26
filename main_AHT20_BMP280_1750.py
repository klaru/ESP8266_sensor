from machine import Pin, I2C, reset, unique_id, freq
from time import sleep
from ubinascii import hexlify
from boot import load_config
from umqttsimple import MQTTClient
from ssd1306_flipped import SSD1306_I2C
#from dht import DHT22
from bme280 import BME280
import bh1750fvi
from ahtx0 import AHT20

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
#sensor_Pin = Pin(pin_sens, Pin.IN)
#sensor = DHT22(sensor_Pin)
sensor = BME280(i2c=i2c)
sensor2 = AHT20(i2c)
topic1 = b'TempBME280'
topic2 = b'Humid'
topic3 = b'PressBME280'
topic4 = b'Light'

client_id = hexlify(unique_id())

def connect_to_mqtt(config):
  client = MQTTClient(client_id, config['mqtt']['broker'])
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
        temperature = sensor.temperature
        humidity = sensor2.relative_humidity
        pressure = sensor.pressure
        light = bh1750fvi.sample(i2c, mode=OP_SINGLE_HRES2)       
        oled.text("T:"+("%.4s" % temperature)+" C", 0, 0)
        oled.text("H:"+("%.4s" % humidity)+" %", 0, 10)
        oled.text(("%.4s" % pressure)+" hPa", 0, 20)       
        oled.text(("%.4s" % light)+" lux", 0, 30)
        oled.show()
        print("T:"+("%.4s" % temperature)+" C")
        print("H:"+("%.4s" % humidity)+" %")
        print(("%.4s" % pressure)+" hPa")
        print(("%.4s" % light)+" lux")
        try:
            client.publish(topic1, str(temperature), qos=QOS)
            client.publish(topic2, str(humidity), qos=QOS)
            client.publish(topic3, str(pressure), qos=QOS)
            client.publish(topic4, str(light), qos=QOS)
        except OSError:
            restart_and_reconnect()
        sleep(10)
            
if __name__ == "__main__":
    main(load_config())
