import daemon

from rest import *

with daemon.DaemonContext():
    rest.start()