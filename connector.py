from launchpad import Launchpad, ButtonEvent
import subscriber

import pkgutil, sys
import time
import imp, os


class Subscriber(object):

    def consume(self):
        pass

    def close(self):
        pass


class Connector(object):

    def __init__(self):
        self.sub = []
        self.handlers = []

        self.load_all_modules_from_dir("subscriber")
        self.register_handlers()

        self.lp = Launchpad()
        self.lp.reset()


    def load_all_modules_from_dir(self, dirname):
        for importer, package_name, _ in pkgutil.iter_modules([dirname]):
            full_package_name = '%s.%s' % (dirname, package_name)
            if full_package_name not in sys.modules:
                module = importer.find_module(package_name).load_module(full_package_name)
                
                class_object = getattr(module, str(module.__name__).split('.')[-1].title())
                class_instance = class_object()
                self.sub.append(class_instance)


    def register_handlers(self):
        for elem in self.sub:
            self.handlers.append(elem.consume)


    def loop(self):
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


    def start(self):
        self.loop()

if __name__ == "__main__":
    Connector().start()