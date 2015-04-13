import time
import base64
import commands

from sockjs.tornado import SockJSConnection

import terminal
import termio


class TerminalClient(SockJSConnection):

    clients = set()

    init_command = None
    connect_command = None
    list_command = None

    @classmethod
    def list_containers(self):
        return commands.getstatusoutput(self.list_command)[1].split("\n")

    @classmethod
    def is_alive(self, session_id):
        if not session_id:
            return False
        if self.list_command:
            return any([x.startswith(session_id) for x in self.list_containers()])
        else:
            return True

    @classmethod
    def create_session(self):
        status = commands.getstatusoutput(self.init_command)
        if status[0] == 0:
            container_id = status[1]
            while not self.is_alive(container_id):
                time.sleep(.1)
            return container_id
        return None

    def __init__(self, *args, **kwargs):
        self.rows = 24
        self.cols = 80
        SockJSConnection.__init__(self, *args, **kwargs)

    # Required Functions

    def resize_check(self):
        if self.mp.term.rows != self.rows or self.mp.term.cols != self.cols:
            self.mp.resize(self.rows, self.cols)

    def on_open(self, info):
        self.session_id = info.get_cookie("term").value
        if self.session_id == "sandbox":
            self.session_id = self.create_session()
        self.last_update = time.time()
        if not self.is_alive(self.session_id):
            self.close()
            return
        try:
            connecting_command = self.connect_command % self.session_id
        except TypeError:
            connecting_command = self.connect_command
        self.mp = termio.Multiplex(connecting_command)
        self.mp.add_callback(
            self.mp.CALLBACK_UPDATE,
            self.send_new_data,
            'ws_update')
        self.mp.add_callback(
            self.mp.CALLBACK_EXIT,
            self.close,
            'ws_close')

        self.mp.spawn()

        self.mp.term.add_callback(terminal.CALLBACK_CHANGED, self.resize_check)

        while not self.mp.isalive():
            time.sleep(.1)
        pass

    def on_message(self, message):
        self.last_update = time.time()
        if not self.mp.isalive():
            self.close()
        if message[0] == "0":
            self.mp.write(unicode(message[1:]))
        if message[0] == "1":
            items = message[1:].split(",")
            self.cols = int(items[0])
            self.rows = int(items[1])
            self.mp.resize(self.rows, self.cols)

    def on_close(self):
        if not self.list_command:
            self.mp.terminate()
        pass

    def send_new_data(self, stream=None):
        if not self.mp.isalive():
            self.close()
            return
        current_time = time.time()
        if stream:
            try:
                msg = unicode(stream)
                self.send("0" + msg)
            except UnicodeDecodeError:
                msg = base64.b64encode(stream)
                self.send("1" + msg)
        self.last_update = current_time
        idle_time = current_time - self.last_update
        if idle_time > 600:
            self.close()
