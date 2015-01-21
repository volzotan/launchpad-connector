from launchpad import Launchpad

import requests
import time
import json

class Rest():

    CONFIG_FILE = "config.json"

    def readConfigFile(self):
        self.config = json.load(open(self.CONFIG_FILE))

    def loop(self, lp):
        while True:
            try:
                inp = lp.receive()
                if inp is not None:
                    velocity = int("0b0110111", 2)

                    coords = inp[1]

                    try: 
                        btn_cnf = self.config["buttons"][ str(coords[0]) + "/" + str(coords[1]) ]
                        print btn_cnf

                        lp.lightButton(coords, green=1, red=1)
                        for elem in btn_cnf["URL"]:
                            if "http://" not in elem:
                                elem = "http://" + elem
                                print elem

                            print self.config["auth"]["username"]

                            response = requests.get(elem, auth=(self.config["auth"]["username"], self.config["auth"]["password"]))
                            print response

                            if (btn_cnf["awaitConfirmation"] == True):
                                if response.status_code == 200:
                                    lp.lightButton(coords, green=1, red=0)
                                else:
                                    lp.lightButton(coords, green=0, red=1)
                            else: 
                                lp.lightButton(coords, green=0, red=0)
                    except KeyError:
                        pass

                    #launchpad.send([144, inp[0][0][1], velocity])
                else:
                    time.sleep(0.1)
            except Exception as e:
                raise


    def main(self):
        self.readConfigFile()
        lp = Launchpad()
        lp.reset()

        self.loop(lp)

if __name__ == "__main__":
    Rest().main()