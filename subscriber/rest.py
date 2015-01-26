from launchpad import Launchpad, ButtonEvent
import interfaces

from threading import Thread

import requests
import time
import json

import logging

logger = logging.getLogger(__name__)


class Rest(interfaces.Subscriber):

    CONFIG_FILE = "subscriber/rest.config"
    BUTTON_LED_DURATION = 1  # in sec


    def __init__(self):
        try:
            self.config = json.load(open(self.CONFIG_FILE))
        except Exception as e:
            logger.error("loading config file failed", e)


    def work(self, lp, coords):
        try: 
            btnCnf = self.config["buttons"][ str(coords[0]) + "/" + str(coords[1]) ]
            lp.lightButton(coords, green=1, red=1)
            for elem in btnCnf["URL"]:
                if not (elem.startswith("http://") or elem.startswith("https://")):
                    elem = "http://" + elem

                response = requests.get(elem, auth=(self.config["auth"]["username"], self.config["auth"]["password"]))

                if (btnCnf["awaitConfirmation"] == True):
                    if response.status_code == 200:
                        lp.lightButton(coords, green=3, red=0)
                    else:
                        lp.lightButton(coords, green=0, red=3)
                        logger.warning(response)
                    
                    time.sleep(self.BUTTON_LED_DURATION)
                
                lp.lightButton(coords, green=0, red=0)
        except KeyError:
            pass


    def consume(self, buttonEvent):
        if buttonEvent.type is ButtonEvent.BUTTON_PRESSED:
            t = Thread(target=self.work, args=(buttonEvent.launchpad, buttonEvent.coords))
            t.start()

