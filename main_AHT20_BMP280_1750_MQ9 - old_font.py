from machine import Pin, I2C, reset, unique_id, freq
from time import sleep
from ubinascii import hexlify
from boot import load_config
from umqttsimple import MQTTClient
from ssd1306_flipped import SSD1306_I2C
from bme280 import BME280
from ahtx0 import AHT20
from mq9 import MQ
#from dht import DHT22
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
#sensor_Pin = Pin(pin_sens, Pin.IN)
#sensor = DHT22(sensor_Pin)
sensor = BME280(i2c=i2c)
sensor2 = AHT20(i2c)
topic1 = b'TempDHT22'
topic2 = b'HumidDHT22'
topic3 = b'Press'
topic4 = b'Light'
topic5 = b'LPG'
topic6 = b'CO'
topic7 = b'ME'

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
        temp_only = ("%.4s" % temperature)
        humidity = sensor2.relative_humidity
        humid_only = ("%.4s" % humidity)
        pressure = sensor.pressure
        press_only = ("%.4s" % pressure)
        light = bh1750fvi.sample(i2c, mode=OP_SINGLE_HRES2)
        if light > 0:
            oled.text("T:"+temp_only+" C", 0, 0)
            oled.text("H:"+humid_only+" %", 0, 10)
            oled.text(press_only+" hPa", 0, 20)
            oled.text(("%.4s" % light)+" lux", 0, 30)
            oled.show()
        else:
            oled.fill(0)
            oled.show()
        print("Temperature: "+("%.4s" % temperature)+" C")
        print("Humidity: "+("%.4s" % humidity)+" %")
        print("Pressure: "+("%.4s" % pressure)+" hPa")
        print("Light Intensity: "+("%.4s" % light)+" lux")
        sleep(5)
        mq = MQ()
        perc = mq.MQPercentage()
        gas_lpg = perc["GAS_LPG"]
        co = perc["CO"]
        methane = perc["SMOKE"]
        if light > 0:
            oled.fill(0)
            oled.show()
            oled.text("LP", 0, 0)
            oled.text(str(float("%.2g" % gas_lpg)), 24, 0)
            oled.text("CO", 0, 10)
            oled.text(str(float("%.2g" % co)), 24, 10 )
            oled.text("ME", 0, 20)
            oled.text(str(float("%.2g" % methane)), 24, 20)
            oled.show()
        else:
            oled.fill(0)
            oled.show()
        print("Gas_LPG: "+str(float("%.2g" % gas_lpg)))
        print("CO: "+str(float("%.2g" % co)))
        print("Methane: "+str(float("%.2g" % methane)))
        try:
            client.publish(topic1, str(temp_only), qos=QOS)
            client.publish(topic2, str(humid_only), qos=QOS)
            client.publish(topic3, str(press_only), qos=QOS)
            client.publish(topic4, str(light), qos=QOS)
            client.publish(topic5, str(gas_lpg), qos=QOS)
            client.publish(topic6, str(co), qos=QOS)
            client.publish(topic7, str(methane), qos=QOS)
        except OSError:
            restart_and_reconnect()
        sleep(10)

if __name__ == "__main__":
    main(load_config())
