import os
import threading
import time
from multiprocessing import Process


class FlaskServer(object):
    def start_server(self):
        t = RunServer('')
        p = Process(target=t.start())
        p.start()

    def stop_server(self):
        os.system('')


class RunServer(threading.Thread):
    def __init__(self, cmd):
        super(RunServer, self).__init__()
        self.cmd = cmd

    def run(self):
        os.system(self.cmd)
