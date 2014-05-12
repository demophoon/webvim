from datetime import timedelta
import commands

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from webvim.assets.websocket import create_session


def is_alive(session_id):
    session_id = session_id[:12]
    sessions = commands.getstatusoutput(
        "docker ps | grep ago | awk '{print $1}'"
    )[1].split("\n")
    return session_id in sessions


@view_config(route_name='home')
def home(request):
    session_id = request.cookies.get("session_id")
    if not session_id or not is_alive(session_id):
        session_id = create_session()
        request.response.set_cookie(
            "session_id",
            value=session_id,
            max_age=timedelta(seconds=1800),
        )
    return HTTPFound("/%s" % session_id, headers = request.response.headers)


@view_config(route_name='terminal', renderer='templates/terminal.pt')
def terminal(request):
    session_id = request.matchdict.get("session_id")
    if not is_alive(session_id):
        raise HTTPFound("/")
    return {'session_id': session_id}
