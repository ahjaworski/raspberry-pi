import requests
import json
import sys
import logging
from PIL import Image,ImageDraw,ImageFont
from time import time, sleep
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in9


url = 'https://blockchain.info/ticker'

epd = epd2in9.EPD()
logging.info("init and Clear")
epd.init(epd.lut_full_update)
epd.Clear(0xFF)

font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

## below commented lines can be uncommented for shutting down the epaper display  
# epd.sleep()
# sleep(3)
# epd.Dev_exit()
# sleep(30)

epd.init(epd.lut_partial_update)    
epd.Clear(0xFF)

def showPrice():
    response = requests.get(url)
    if (response.ok):
        data = json.loads(response.content)
        print("Bitcoin data:", data)
        
        bitcoinPriceEur = data['EUR']['buy']
        bitcoinPriceUsd = data['USD']['buy']
                
        try:
            Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            bmp = Image.open(os.path.join(picdir, 'bitcoin.bmp'))
            Himage.paste(bmp, (20,0))
            draw = ImageDraw.Draw(Himage)
            draw.text((165, 30), '€ ' + str(bitcoinPriceEur), font = font24, fill = 0)
            draw.text((165, 70), '$ ' + str(bitcoinPriceUsd), font = font24, fill = 0)
            epd.display(epd.getbuffer(Himage))
            
        except IOError as e:
            logging.info(e)
            logging.info("Goto Sleep...")
            epd.sleep()
            sleep(3)
            epd.Dev_exit()

    else:
        response.raise_for_status()
        logging.info("Goto Sleep...")
        epd.sleep()
        sleep(3)
        epd.Dev_exit()


showPrice()
while True:
    sleep(30 - time() % 30)
    showPrice()
