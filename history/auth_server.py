from .common import *
from aiohttp import web
import urllib.parse
from .SpotifyAuth import SpotifyAuth

SCOPES = ["user-read-recently-played"]
AUTH_URL = f"{SPOTIFY_AUTH_ENDPOINT}/authorize"

class AuthCodeReceiver(Exception):
    def __init__(self, code):
        super()
        self.code = code

async def handle_auth(_):
    """
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    redirect to spotify auth
    """
    raise web.HTTPFound(AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "scope": " ".join(SCOPES),
        "response_type": "code",
        "redirect_uri": REDIRECT_URI
    }))

async def handle_code(req):
    print("received auth code")
    code = req.query["code"]
    SpotifyAuth.authorize(code)
    return web.Response(text="Authroized, you can close this window now")

def start_server():
    """
    starts the auth server, waiting for
    """
    app = web.Application()
    app.add_routes([
        web.get("/", handle_auth),
        web.get("/redirect", handle_code),
    ])
    return web._run_app(app, port=SERVER_PORT)

async def auth():
    server = start_server()
    try:
        await server
        print("close")
    except AuthCodeReceiver as a:
        return a.code
