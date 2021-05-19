import asyncio
from . import auth_server
from .Spotify import Spotify

server = auth_server.auth()

Spotify.auth()

asyncio.run(server)
