from launchpad import Launchpad, ButtonEvent
import subscriber

import pkgutil, sys
import time
import imp, os

import logging

logger = logging.getLogger(__name__)


class Connector(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        self.sub = []
        self.handlers = []

        self.load_all_modules_from_dir("subscriber")
        self.register_handlers()

        self.lp = Launchpad()
        self.lp.reset()

        self.init_animation()


    def load_all_modules_from_dir(self, dirname):
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            full_package_name = '%s.%s' % (dirname, package_name)
            if full_package_name not in sys.modules:
                module = importer.find_module(package_name).load_module(full_package_name)
                
                class_object = getattr(module, str(module.__name__).split('.')[-1].title())
                class_instance = class_object()
                self.sub.append(class_instance)
                logger.info("imported subscriber {}".format(class_object))


    def register_handlers(self):
        for elem in self.sub:
            self.handlers.append(elem.consume)


    def init_animation(self):
        import random
        from random import randint

        PAUSE_DURATION = 0.2

        # calculate random order 
        btn_list = []
        for x in range (0,9):
            for y in range(0,9):
                btn_list.append((x,y))

        for color in range(1,4):
            random.shuffle(btn_list)
            for elem in btn_list:
                green = (color & 2) >> 1
                red = color & 1
                # first digit and second digit [0|1, 1|0, 1|1, (0|0)]
                self.lp.lightButton(elem, green, red)
                time.sleep(0.003)

            # for brightness in range(1,4):
            #     for x in range(0,8):
            #         for y in range(0,8):
            #             self.lp.lightButton((x,y), green * brightness, red * brightness)
            #     time.sleep(0.05)

            time.sleep(PAUSE_DURATION)

        for i in range(0,400):
            self.lp.lightButton((randint(0,7), randint(0,7)), randint(0,3), randint(0,3))
            time.sleep(0.003)

        for elem in btn_list:
            self.lp.lightButton(elem, 0, 0)
            time.sleep(0.003)

        time.sleep(1)

    def loop(self):
        logger.info("event loop running")

        while True:
            try:
                buttonEvent = self.lp.receive()
                if buttonEvent is not None:

                    for func in self.handlers:
                        func(buttonEvent)

                else:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                for elem in self.sub:
                    elem.close()

                self.lp.close()
                sys.exit(0)
            except Exception as e:
                logger.error(e)
                raise


if __name__ == "__main__":
    Connector().loop()