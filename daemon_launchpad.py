import daemon

from connector import *

with daemon.DaemonContext():
    connector.start()