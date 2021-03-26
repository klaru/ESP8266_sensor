from machine import I2C, Pin, freq
import time

# select GPIO pins
if freq() > 80000000:   # ESP32
    pin_scl = 22
    pin_sda = 21
else:                   # ESP8266
    pin_scl = 5
    pin_sda = 4

i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda))


def main():
    while True:
        print('Scan i2c bus...')
        devices = i2c.scan()

        print('i2c devices found:',len(devices))
 
        for device in devices:  
            print("Decimal address: ",device," | Hex address: ",hex(device))
        sleep(10)

            
if __name__ == "__main__":
    main()