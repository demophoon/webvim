from sockjs.tornado import SockJSRouter
from tornado import web, ioloop

from assets.websocket import TerminalClient


class EntrypointHandler(web.RequestHandler):

    def get(self):
        if not TerminalClient.is_alive(self.get_cookie("term")):
            self.clear_cookie("term")
            self.set_cookie("term", TerminalClient.create_session())
        self.redirect("/static/index.html")


if __name__ == '__main__':
    TerminalRouter = SockJSRouter(TerminalClient, '/terminal')

    app = web.Application(TerminalRouter.urls, static_path="./static")
    app.add_handlers(r".*", [
        (r"/$", EntrypointHandler),
    ])
    app.listen(9090)
    ioloop.IOLoop.instance().start()
