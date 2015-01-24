from launchpad import Launchpad
from rest import Rest

class ButtonEvent(object):

    def __init__(self, _lp, _coords, _type):
        self.launchpad = _lp
        self.coords = _coords
        self.type = _type


class Connector(object):

    def __init__(self):
        self.lp = Launchpad()
        self.register_handlers()

    def register_handlers(self):
        self.handlers = [Rest().consume]

    def loop(self):
        while True:
            try:
                inp = self.lp.receive()
                if inp is not None:
                    coords = inp[1]

                    for func in handlers:
                        func(lp, coords, inp[2])

                else:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                lp.close()

def start(self):
    self.loop()

if __name__ == "__main__":
    Connector().start()