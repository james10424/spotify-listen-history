import os

SERVER_PORT = 8080
SPOTIFY_AUTH_ENDPOINT = "https://accounts.spotify.com"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1"
LOCAL_ENDPOINT = f"http://localhost:{SERVER_PORT}"
REDIRECT_URI = f"{LOCAL_ENDPOINT}/redirect"
LOCAL_AUTH_ENDPOINT = f"{LOCAL_ENDPOINT}/"
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
CLIENT_ID = os.environ["CLIENT_ID"]
