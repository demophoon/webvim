import os
import sys
import ConfigParser

from sockjs.tornado import SockJSRouter
from tornado import web, ioloop

from assets.websocket import TerminalClient


class EntrypointHandler(web.RequestHandler):

    def get(self):
        term = self.get_cookie("term")
        if term and not TerminalClient.is_alive(term):
            self.clear_cookie("term")
            self.set_cookie("term", TerminalClient.create_session())
        elif not term:
            self.set_cookie("term", TerminalClient.create_session())
        self.render("templates/terminal.html")


def main():
    # CLI Argument parser
    args = sys.argv[1:]
    if len(args) >= 1:
        config_path = args
    else:
        config_path = ["production.ini"]

    base_path = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join(base_path, 'conf', 'defaults.ini')))
    config.read(config_path)

    # Read configurations
    port = int(config.get('main', 'port'))
    docker_container = config.get('commands', 'container')
    init_command = config.get('commands', 'init')
    connect_command = config.get('commands', 'connect')
    list_command = config.get('commands', 'list')

    # Set settings on TerminalClient object
    tc = TerminalClient
    tc.docker_container = docker_container
    if docker_container:
        tc.init_command = init_command % docker_container
        tc.connect_command = connect_command
        tc.list_command = list_command
    else:
        tc.connect_command = connect_command

    # Setup Tornado Routes
    TerminalRouter = SockJSRouter(tc, '/terminal')
    app = web.Application(
        TerminalRouter.urls,
        static_path=os.path.join(base_path, 'static'))
    app.add_handlers(r".*", [
        (r"/$", EntrypointHandler),
    ])

    # Start the server
    print "Running Webterm on port %d" % port
    app.listen(port)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
