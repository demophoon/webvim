import gevent
from gevent import monkey, Greenlet
monkey.patch_all()

import time
import commands
from datetime import timedelta

from pyramid_sockjs.session import Session

import termio

init_command = "sudo docker run --user='untrust' "
init_command += "--workdir='/home/untrust' "
init_command += "--net='none' "
init_command += "-dit demophoon/vim_base %s"
init_command %= "vim ./README.md"
connect_command = "sudo docker attach %s"


def create_session():
    status = commands.getstatusoutput(init_command)
    if status[0] == 0:
        return status[1][:12]
    return None


def is_alive(session_id):
    sessions = commands.getstatusoutput(
        "sudo docker ps | grep ago | awk '{print $1}'"
    )[1].split("\n")
    return session_id in sessions


class TerminalClient(Session):

    def on_open(self):
        self.session_id = self.request.matchdict.get("session_id")
        if self.session_id == "sandbox":
            self.session_id = create_session()
            self.request.response.set_cookie(
                "session_id",
                value=self.session_id,
                max_age=timedelta(seconds=1800),
            )
        self.last_update = time.time()
        self.mp = termio.Multiplex(connect_command % self.session_id)
        self.mp.spawn()
        while not self.mp.isalive():
            time.sleep(.1)
        self.mp.resize(cols=120, rows=40, ctrl_l=False)
        self.timer = Greenlet.spawn(self.send_new_data)
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
            self.mp.resize(int(cols), int(rows), ctrl_l=False)

    def on_close(self):
        pass

    def send_new_data(self):
        while self.mp.isalive():
            output = None
            try:
                output = self.mp.read()
            except Exception:
                pass
            current_time = time.time()
            if output:
                self.send(output)
                self.last_update = current_time
            idle_time = current_time - self.last_update
            if idle_time > 600:
                break
            elif idle_time > 15:
                gevent.sleep(1)
            else:
                gevent.sleep(.1)
        self.close()
