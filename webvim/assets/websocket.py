import time
import base64
import commands

from sockjs.tornado import SockJSConnection

import termio


class TerminalClient(SockJSConnection):

    init_command = "docker run --net='none' -dit demophoon/webvim"
    connect_command = "docker attach %s"
    list_command = "docker ps -q --no-trunc"

    @classmethod
    def list_containers(self):
        return commands.getstatusoutput(self.list_command)[1].split("\n")

    @classmethod
    def is_alive(self, session_id):
        return any([x.startswith(session_id) for x in self.list_containers()])

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
        SockJSConnection.__init__(self, *args, **kwargs)

    # Required Functions

    def on_open(self, info):
        self.session_id = info.get_cookie("term").value
        if self.session_id == "sandbox":
            self.session_id = self.create_session()
        self.last_update = time.time()
        if not self.is_alive(self.session_id):
            self.close()
            return
        self.mp = termio.Multiplex(self.connect_command % self.session_id)
        self.mp.add_callback(
            self.mp.CALLBACK_UPDATE,
            self.send_new_data,
            'ws_update')
        self.mp.add_callback(
            self.mp.CALLBACK_EXIT,
            self.close,
            'ws_close')
        self.mp.spawn()
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
            print "Resized"
            items = message[1:].split(",")
            cols = items[0]
            rows = items[1]
            time.sleep(.1)
            self.mp.resize(int(rows), int(cols), ctrl_l=False)
            print "Expected: %s" % (items, )
            print "Actual:   %s" % ((self.mp.term.rows, self.mp.term.cols), )

    def on_close(self):
        pass

    def send_new_data(self, stream=None):
        if not self.mp.isalive():
            self.close()
            return
        current_time = time.time()
        if stream:
            output = base64.b64encode(stream)
            self.send(output)
            self.last_update = current_time
        idle_time = current_time - self.last_update
        if idle_time > 600:
            self.close()
