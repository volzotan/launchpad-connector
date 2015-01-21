from launchpad import Launchpad

from threading import Thread

import requests
import time
import json

class Rest():

    CONFIG_FILE = "config.json"

    def readConfigFile(self):
        self.config = json.load(open(self.CONFIG_FILE))


    def work(self, lp, coords):
        try: 
            btnCnf = self.config["buttons"][ str(coords[0]) + "/" + str(coords[1]) ]
            lp.lightButton(coords, green=1, red=1)
            for elem in btnCnf["URL"]:
                if "http://" not in elem:
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


    def loop(self, lp):
        while True:
            try:
                inp = lp.receive()
                if inp is not None:
                    coords = inp[1]

                    t = Thread(target=self.work, args=(lp, coords))
                    t.start()

                else:
                    time.sleep(0.1)
            except Exception as e:
                raise


    def main(self):
        self.readConfigFile()
        lp = Launchpad()
        lp.reset()

        self.loop(lp)


def start():
    Rest().main()

if __name__ == "__main__":
    start()