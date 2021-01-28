
# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import uos
#uos.dupterm(None, 1) # disable REPL on UART(0)import gc
import machine
import gc
import webrepl
import ujson
import network
import micropython
import secrets
    
def load_config():
    with open('config.json') as f:
        return ujson.loads(f.read())

def do_connect(config):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.scan()
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)
        print('Network config:', sta_if.ifconfig())

do_connect(load_config())

last_message = 0
message_interval = 5
counter = 0

    
webrepl.start()
gc.collect()
