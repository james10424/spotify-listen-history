import requests
from .common import *
from base64 import b64encode
from datetime import datetime, timedelta
import webbrowser

TOKEN_ENDPOINT = f"{SPOTIFY_AUTH_ENDPOINT}/api/token"

"""
auth documentation: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
"""
class SpotifyAuth:
    ACCESS_TOKEN = None
    REFRESH_TOKEN = None
    GRANT_TIME = None
    EXPIRES_IN = None
    AUTH = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    CALLBACK = None

    @staticmethod
    def start_auth(callback):
        """
        get the auth code from Spotify
        step 1 of the auth process
        """
        SpotifyAuth.CALLBACK = callback
        webbrowser.open(LOCAL_AUTH_ENDPOINT)

    @staticmethod
    def exchange_tokens(code):
        """
        exchange the temp code for access and refresh token
        step 2 of the auth process

        return access_token, refresh_token, expire_in
        """
        r = requests.post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            headers={
                "Authorization": "Basic " + SpotifyAuth.AUTH
            }
        )
        if r.status_code != 200:
            r.raise_for_status()
        res = r.json()
        return res["access_token"], res["refresh_token"], res["expires_in"]

    @staticmethod
    def authorize(code):
        SpotifyAuth.ACCESS_TOKEN, SpotifyAuth.REFRESH_TOKEN, expires_in =\
            SpotifyAuth.exchange_tokens(code)
        print("exchanged tokens")
        SpotifyAuth.GRANT_TIME = datetime.today()
        SpotifyAuth.EXPIRES_IN = timedelta(seconds=expires_in)

        if SpotifyAuth.CALLBACK:
            SpotifyAuth.CALLBACK()

    @staticmethod
    def refresh():
        assert SpotifyAuth.REFRESH_TOKEN is not None
        if datetime.today() < SpotifyAuth.GRANT_TIME + SpotifyAuth.EXPIRES_IN:
            # did not expire
            return

        r = requests.post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "refresh_token",
                "refresh_token": SpotifyAuth.REFRESH_TOKEN,
            },
            headers={
                "Authorization": "Basic " + SpotifyAuth.AUTH
            }
        )
        if r.status_code != 200:
            r.raise_for_status()

        res = r.json()
        SpotifyAuth.ACCESS_TOKEN = res["access_token"]
        expires_in = res["expires_in"]
        SpotifyAuth.EXPIRE_IN = timedelta(seconds=expires_in)
        SpotifyAuth.GRANT_TIME = datetime.today()
