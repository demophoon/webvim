import time
import threading

from pyramid_sockjs.session import Session

import termio

command = "docker run -i -t demophoon/vim_base %s"
command %= "timelimit -q -t 1800 -S 9 vim -Z ./README.md && exit"


class TerminalClient(Session):

    def on_open(self):
        self.last_update = time.time()
        self.mp = termio.Multiplex(command)
        self.mp.spawn()
        self.timer = threading.Thread(target=self.send_new_data)
        while not self.mp.isalive():
            time.sleep(.1)
        self.mp.resize(cols=120, rows=40)
        self.timer.start()
        pass

    def on_message(self, message):
        self.last_update = time.time()
        if not self.mp.isalive():
            self.close()
        if message[0] == "0":
            self.mp.write(unicode(message[1:]))
        if message[0] == "1":
            rows = message[1:].split(",")[0]
            cols = message[1:].split(",")[1]
            self.mp.resize(int(cols), int(rows))

    def on_close(self):
        if self.mp.isalive():
            self.mp.writeline(u"\u001B\u001B:q!")
        self.mp.terminate()

    def send_new_data(self):
        while self.mp.isalive():
            output = None
            try:
                output = self.mp.read()
            except Exception, e:
                pass
            current_time = time.time()
            if output:
                self.send(output)
                self.last_update = current_time
            idle_time = current_time - self.last_update
            if idle_time > 600:
                break
            elif idle_time > 15:
                time.sleep(1)
            else:
                time.sleep(.1)
        self.mp.terminate()
        self.close()
