from launchpad import Launchpad, ButtonEvent
import interfaces

from threading import Thread
import time
import logging

import unicornhat as corn

logger = logging.getLogger(__name__)


class Cornhat(interfaces.Subscriber):

    BUTTON_LED_DURATION = 1  # in sec

    def __init__(self):
        corn.brightness(0.7)

    def work(self, lp, coords):
        try: 
            lp.lightButton(coords, green=1, red=1)  
            corn.set_pixel(coords[0], coords[1], 100, 100, 100)     
            corn.show()  
            time.sleep(self.BUTTON_LED_DURATION)    
            lp.lightButton(coords, green=0, red=0)
            corn.set_pixel(coords[0], coords[1], 0, 0, 0)     
            corn.show()  
        except KeyError:
            pass


    def consume(self, buttonEvent):
        if buttonEvent.type is ButtonEvent.BUTTON_PRESSED:
            t = Thread(target=self.work, args=(buttonEvent.launchpad, buttonEvent.coords))
            t.start()
