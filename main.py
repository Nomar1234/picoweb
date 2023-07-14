# project for the boys!
# using a raspberry pi pico w to server a web page.

import network
from time import sleep
import machine
import json

from microdot import Microdot, send_file
from picozero import pico_led

# read SSID and PASSWORD from config file
# and connect to wifi:

def connect():
    # connect to WLAN
    ssid = ''
    password = ''
    with open('wifi.json', 'r') as wifi_settings:
        wifi_dict = json.load(wifi_settings)
        ssid = wifi_dict['ssid']
        password = wifi_dict['password']

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for WiFi connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on: {ip}')
    return ip

app = Microdot()

HOME_TEMPLATE = open('index.html', 'r')

@app.before_request
def before_led_on(request):
    pico_led.on()
    return

@app.after_request
def after_led_off(request, response):
    pico_led.off()
    return

@app.route('/')
def index(request):
    #print(f"{request.client_addr}: {request.method} URL={request.url} HEADERS={request.headers}")
    print(f"{request.method} {request.url} from {request.client_addr[0]}:{request.client_addr[1]}")
    #return 'Hello, World!'
    return send_file('/index.html')

@app.route('/favicon.ico')
def favicon(request):
    return "🔥"

def main(app):

    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset()

    app.run(host=ip, port=80,debug=True)

if __name__ == "__main__":
    main(app)


