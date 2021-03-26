from machine import I2C, Pin, freq

# select GPIO pins
if freq() > 80000000:   # ESP32
    pin_scl = 22
    pin_sda = 21
else:                   # ESP8266
    pin_scl = 5
    pin_sda = 4

ahtx0_addresses = [0x38]
bmx_addresses = [0x76,0x77]
bh1750_addresses = [0x23]
sht3x_addresses = [0x44,0x45]
sgp30_addresses = [0x58]
sgp40_addresses = [0x59]
scd30_addresses = [0x61]
tsl2561_addresses = [0x29,0x39,0x49]        
ssd130x_addresses = [0x35,0x36]
ds1307_addresses = [0x68]

i2c = I2C(scl=Pin(pin_scl), sda=Pin(pin_sda))

def main():
    print('Scan i2c bus...')
    devices = i2c.scan()

    print('i2c devices found:',len(devices))
 
    for device in devices:
        for address in ahtx0_addresses:
            if device == address:
                print("AHTx0 temperature, humidity sensor at: ",hex(device))
        for address in bmx_addresses:
            if device == address:
                print("BMx temperature, humidity sensor at: ",hex(device))
        for address in bh1750_addresses:
            if device == address:
                print("BH1750 light intensity sensor at: ",hex(device))
        for address in sht3x_addresses:
            if device == address:
                print("SHT3x temperature, humidity sensor at: ",hex(device))      
        for address in sgp30_addresses:
            if device == address:
                print("SGP30 air quality sensor at: ",hex(device))
        for address in sgp40_addresses:
            if device == address:
                print("SGP40 air quality sensor at: ",hex(device))
        for address in scd30_addresses: 
            if device == address:
                print("SCD30 CO2 sensor at: ",hex(device))
        for address in tsl2561_addresses:
            if device == address:
                print("TSL2561 light intensity sensor at: ",hex(device))
        for address in ssd130x_addresses:
            if device == address:
                print("SSD130x display at: ",hex(device))
         for address in ds1307_addresses:
            if device == address:
                print("DS1307 RTC at: ",hex(device))
                
if __name__ == "__main__":
    main()