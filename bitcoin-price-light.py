import requests
import json
from time import time, sleep
from gpiozero import LED

red = LED(22)
orange = LED(27)
green = LED(17)

red.off()
orange.off()
green.off()

url = 'https://bitonic.nl/api/buy?btc=1'
oldPrice = 0

while True:
    sleep(30 - time() % 30)
    myResponse = requests.get(url)
    if (myResponse.ok):
        jData = json.loads(myResponse.content)

        print("Bitcoin prijs eerst in euro:", oldPrice)
        print("\n")
        print("Bitcoin prijs nu in euro:", jData['eur'])
        newPrice = jData['eur']
        if (oldPrice < newPrice):
            red.off()
            orange.off()
            green.blink(1, 1, 1)
        else:
            red.blink(1, 1, 1)
            orange.off()
            green.off()

        if (newPrice > 35000):
            green.on()

        oldPrice = newPrice

    else:
        myResponse.raise_for_status()
