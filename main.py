from machine import Pin, I2C, reset, unique_id, freq
from time import sleep, time, localtime
from boot import load_config
from umqttsimple import MQTTClient
from ubinascii import hexlify
from ssd1306_flipped import SSD1306_I2C
#from dht import DHT22
from sht30 import SHT30
from mq9 import MQ
import bme280
import ds1307

QOS=1
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

i2c_if = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda), freq=frequency)
oled = SSD1306_I2C(width, height, i2c_if)
bme = bme280.BME280(mode=BME280_OSAMPLE_16, i2c=i2c_if)
rtc = ds1307.DS1307(i2c_if)

#sensor_Pin = Pin(pin_sens, Pin.IN)
#dht = DHT22(sensor_Pin)

topic1 = b'TempDHT22'
topic2 = b'HumidDHT22'
#topic1 = b'TempSHT30
#topic2 = b'HumidSHT30
topic3 = b'Press'
topic4 = b'LPG'
topic5 = b'CO'
topic6 = b'ME'
topic7 = b'TempBME280'
topic8 = b'Sens_Date'
topic9 = b'Sens_Time'

def connect_to_mqtt(config):
  global client_id
  client = MQTTClient(client_id, config['mqtt']['broker'])
  client.connect()
  print('Connected to %s MQTT broker' % (config['mqtt']['broker']))
  return client
        
def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Restarting and reconnecting...')
  reset()
  
def zfill(s, width):
    return "{:0>{w}}".format(s, w=width)
    
# Main loop that will run forever:
def mainloop(config):
  
    try:
        client = connect_to_mqtt(config)
    except OSError:
        sleep(10)
        restart_and_reconnect()

    while True:
        oled.fill(0)
        oled.show()
 #       dht.measure()
 #       temp_dht = dht.temperature()
 #       humidity = dht.humidity()   
        sensor = SHT30() 
        temp_sht, humidity = sensor.measure() 
        press_bme = bme.pressure
        pressure = float(press_bme[:-3])
        temp_bme = bme.temperature
 #       temp_bme_float = float(temp_bme[:-1])
 #       temperature = (temp_dht + 2*temp_bme_float)/3
 #       temperature = (temp_sht + 2*temp_bme_float)/3
        temperature = float(temp_bme[:-1])
        oled.text("Temp =", 0, 0)
        oled.text(str("%.1f" % temperature)+" C", 0, 10)
        oled.text("Humid =", 0, 20)
        oled.text(str("%.1f" % humidity)+" %", 0, 30)
        oled.text(str("%.0f" % pressure)+" hPa", 0, 40)
        oled.show()
        print(temperature)
        print(humidity)
        print(pressure)       
        sleep(5)
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
        datetime = rtc.datetime()
#        datetime = localtime()
        minute_str = str(datetime[5])
        date_str = str(datetime[1])+"-"+str(datetime[2])+"-"+str(datetime[0])[-2:]
        oled.text(date_str, 0, 30)
        time_str = str(datetime[4])+"h:"+zfill(minute_str, 2)+"m"
        oled.text(time_str, 0, 40)
        oled.show()        
        print(gas_lpg)
        print(co)
        print(methane)     
        try:        
            client.publish(topic1, str(temperature), qos=QOS)
            client.publish(topic2, str(humidity), qos=QOS)
            client.publish(topic3, str(pressure), qos=QOS)
            client.publish(topic4, str(gas_lpg), qos=QOS)
            client.publish(topic5, str(co), qos=QOS)
            client.publish(topic6, str(methane), qos=QOS)   
            client.publish(topic7, str(temperature), qos=QOS)
            client.publish(topic8, date_str, qos=QOS)
            client.publish(topic9, time_str, qos=QOS)   
        except OSError:
            restart_and_reconnect()        
        sleep(10)
            
if __name__ == "__main__":
    config = load_config()
    client_id = hexlify(unique_id())    
    mainloop(config)
