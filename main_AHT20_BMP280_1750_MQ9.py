from machine import Pin, I2C, reset, unique_id, freq
from time import sleep
from ubinascii import hexlify
from boot import load_config
from umqttsimple import MQTTClient
from ssd1306_flipped import SSD1306_I2C
from bme280 import BME280
from ahtx0 import AHT20
from mq9 import MQ
import bh1750fvi
from writer_minimal import Writer
import Arial11

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

frequency = 100000
width = 64
height = 48
BME280_OSAMPLE_16 = 5
OP_SINGLE_HRES2 = 0x21

display_address1 = 0x3C
bmx_address1 = 0x76
light_address1 = 0x23
display_address2 = 0x3D
bmx_address2 = 0x77
light_address2 = 0x5C

display_present1 = False
bmx_present1 = False
light_present1 = False
display_present2 = False
bmx_present2 = False
light_present2 = False

i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda), freq=frequency)
devices = i2c.scan()

for device in devices:
    if device == display_address1:
            display_present1 = True
    if device == bmx_address1:
            bmx_present1 = True
    if device == light_address1:
            light_present1 = True  
    if device == display_address2:
            display_present2 = True
    if device == bmx_address2:
            bmx_present2 = True
    if device == light_address2:
            light_present2 = True 
            
if display_present1:
    oled = SSD1306_I2C(width, height, i2c, addr=display_address1)
if display_present2:
    oled = SSD1306_I2C(width, height, i2c, addr=display_address2)    
sensor = AHT20(i2c)
if bmx_present1:
    sensor2 = BME280(mode=BME280_OSAMPLE_16, address=bmx_address1,i2c=i2c)
if bmx_present2:
    sensor2 = BME280(mode=BME280_OSAMPLE_16, address=bmx_address2,i2c=i2c)
    
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

    if (display_present1 or display_present2):
        writer = Writer(oled, Arial11)
    while True:
        if (display_present1 or display_present2):
            oled.fill(0)
            oled.show()
        temperature = sensor.temperature
        temp_only = ("%.4s" % temperature)
        humidity = sensor.relative_humidity
        humid_only = ("%.4s" % humidity)
        if (bmx_present1 or bmx_present2):
            pressure = sensor2.pressure
            press_float = float(pressure[:-3])        
            press_only = str("%.0f" % press_float)
        if (light_present1 or light_present2):
            light = bh1750fvi.sample(i2c, mode=OP_SINGLE_HRES2)
        if ((display_present1 or display_present2) and (light_present1 or light_present2) and light > 0):
            writer.set_textpos(0,0)
            writer.printstring("T: "+temp_only+"°C")
            writer.set_textpos(12,0)
            writer.printstring("H: "+humid_only+" %")
            if (bmx_present1 or bmx_present2):
                writer.set_textpos(24,0)
                writer.printstring(press_only+" hPa")
            if (light_present1  or light_present2):
                writer.set_textpos(36,0)
                writer.printstring(("%.4s" % light)+" lux")
            oled.show()
        print("Temperature: "+temp_only+"°C")
        print("Humidity: "+humid_only+" %")
        if (bmx_present1 or bmx_present2):
            print("Pressure: "+press_only+" hPa")
        if (light_present1 or light_present2):
            print("Light Intensity: "+("%.4s" % light)+" lux")
        sleep(25)
        if (display_present1 or display_present2):
            oled.fill(0)
            oled.show()        
        mq = MQ()
        perc = mq.MQPercentage()
        gas_lpg = perc["GAS_LPG"]
        co = perc["CO"]
        methane = perc["SMOKE"]
        light = bh1750fvi.sample(i2c, mode=OP_SINGLE_HRES2)    
        if ((display_present1 or display_present2) and (light_present1 or light_present2) and light > 0):
            writer.set_textpos(0,0)
            writer.printstring("LP "+str(float("%.2g" % gas_lpg)))          
            writer.set_textpos(12,0)
            writer.printstring("CO "+str(float("%.2g" % co)))           
            writer.set_textpos(24,0)
            writer.printstring("ME "+str(float("%.2g" % methane)))   
            oled.show()
        print("Gas_LPG: "+str(float("%.2g" % gas_lpg)))
        print("CO: "+str(float("%.2g" % co)))
        print("Methane: "+str(float("%.2g" % methane)))
        try:
            client.publish(topic1, str(temp_only), qos=QOS)
            client.publish(topic2, str(humid_only), qos=QOS)
            if (bmx_present1 or bmx_present2):
                client.publish(topic3, str(press_only), qos=QOS)
            if (light_present1 or light_present2):
                client.publish(topic4, str(light), qos=QOS)
            client.publish(topic5, str(gas_lpg), qos=QOS)
            client.publish(topic6, str(co), qos=QOS)
            client.publish(topic7, str(methane), qos=QOS)
        except OSError:
            restart_and_reconnect()
        sleep(25)
        if (display_present1 or display_present2):
            oled.fill(0)
            oled.show()      
        sleep(25)

if __name__ == "__main__":
    main(load_config())
