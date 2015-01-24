from launchpad import Launchpad

from threading import Thread

import requests
import time
import json

class Rest(object):

    CONFIG_FILE = "rest.config"

    def __init__(self):
        self.readConfigFile()


    def readConfigFile(self):
        self.config = json.load(open(self.CONFIG_FILE))


    def work(self, lp, coords):
        try: 
            btnCnf = self.config["buttons"][ str(coords[0]) + "/" + str(coords[1]) ]
            lp.lightButton(coords, green=1, red=1)
            for elem in btnCnf["URL"]:
                if not (elem.startswith("http://") or elem.startswith("https://")):
                    elem = "http://" + elem

                response = requests.get(elem, auth=(self.config["auth"]["username"], self.config["auth"]["password"]))
                print response

                if (btnCnf["awaitConfirmation"] == True):
                    if response.status_code == 200:
                        lp.lightButton(coords, green=1, red=0)
                    else:
                        lp.lightButton(coords, green=0, red=1)
                    
                    time.sleep(1)
                
                lp.lightButton(coords, green=0, red=0)
        except KeyError:
            pass


    def consume(self, buttonEvent):
        if buttonEvent.type is Launchpad.BUTTON_PRESSED:
            t = Thread(target=self.work, args=(buttonEvent.launchpad, buttonEvent.coords))
            t.start()
