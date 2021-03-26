from machine import Pin, I2C, reset, unique_id
from time import sleep
from boot import load_config
from umqttsimple import MQTTClient
from ubinascii import hexlify
from ssd1306_flipped import SSD1306_I2C
from dht import DHT22
import BME280

frequency = 100000
   
HW = runs_on()
if HW == 32:
# ESP32 - Pin assignment
    i2c_if = I2C(scl=Pin(22), sda=Pin(21), freq=frequency)
else:
# ESP8266 - Pin assignment
    i2c_if = I2C(scl=Pin(5), sda=Pin(4), freq=frequency)
 
width = 64
height = 48
oled = SSD1306_I2C(width, height, i2c_if)

bme = BME280.BME280(i2c=i2c_if)

pin2 = Pin(2, Pin.IN)
dht = DHT22(pin2)

topic1 = b'TempBME280'
topic2 = b'HumidBME280'
topic3 = b'PressBME280'

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
        temp_dht = dht.temperature()
        humid_dht = dht.humidity()       
        temp_bme = bme.temperature
        humid_bme = bme.humidity
        pressure = bme.pressure
        temperature = (temp_dht + 2*temp_bme)/3
        humidity = (humid_dht + 2*humid_bme)/3
        oled.text("Temp =", 0, 0)
        oled.text(str(temperature)+" C", 0, 10)
        oled.text("Humid =", 0, 20)
        oled.text(str(humidity)+" %", 0, 30)
        oled.text(str(pressure)+" mb", 0, 40)
        oled.show()        
        print(temperature)
        print(humidity)
        print(pressure)
        try:
            client.publish(topic1, str(temperature))
            client.publish(topic2, str(humidity))
            client.publish(topic3, str(pressure))
        except OSError:
            restart_and_reconnect()
        sleep(10)
            
if __name__ == "__main__":
    config = load_config()
    client_id = hexlify(unique_id())    
    mainloop(config)
