import daemon
import os

from connector import Connector

logfile = open('lpd_logfile', 'w+')
errfile = open('lpd_errfile', 'w+')

context = daemon.DaemonContext()
context.stdout = logfile
context.stderr = errfile

context.working_directory = os.path.dirname(os.path.realpath(__file__)) # script file directory
                                                                        # or working directory: os.getcwd()

def start():
    conn = Connector()
    conn.loop()

with context:
    start()