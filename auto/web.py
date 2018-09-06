from flask import Flask
from flask import jsonify
import os
import threading
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


app = Flask(__name__)


@app.route('/')
def get_json():
    data = {'name': 'xiaoming', 'age': 18}
    return jsonify(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
