import time

from pyramid_sockjs.session import Session

import termio

command = "docker run -i -t demophoon/vim_base %s"
command %= "timelimit -pq -T 600 -S 9 vim -Z ./README.md"


class TerminalClient(Session):

    def on_open(self):
        self.ready = False
        self.mp = termio.Multiplex(command)
        self.mp.spawn()
        while not self.mp.isalive():
            time.sleep(.1)
        self.mp.resize(cols=120, rows=40)
        self.send_new_data()
        pass

    def on_message(self, message):
        if message[0] == "0":
            self.mp.write(unicode(message[1:]))
        if message[0] == "1":
            rows = message[1:].split(",")[0]
            cols = message[1:].split(",")[1]
            self.mp.resize(int(cols), int(rows))
        self.send_new_data()

    def on_close(self):
        if self.mp.isalive():
            self.mp.write(u"\u001B\u001B:q!\u000A")
            self.mp.terminate()

    def send_new_data(self):
        if self.mp.isalive():
            self.send(self.mp.read())
        else:
            self.close()
