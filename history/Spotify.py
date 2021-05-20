from .auth_server import SpotifyAuth
import requests
from .common import *
import pandas as pd

def ensure_auth(f):
    def _ensure(*args, **kwargs):
        SpotifyAuth.refresh()
        return f(*args, **kwargs)
    return _ensure

class Spotify:
    @staticmethod
    def auth():
        print("Authorizing, you will be notified when it's authorized")
        SpotifyAuth.start_auth(Spotify.auth_complete)

    @staticmethod
    def auth_complete():
        print("Authorized")
        Spotify.get_recent()

    @staticmethod
    @ensure_auth
    def get(endpoint, params):
        r = requests.get(
            endpoint,
            params=params,
            headers={
                "Authorization": "Bearer " + SpotifyAuth.ACCESS_TOKEN
            }
        )
        if r.status_code != 200:
            r.raise_for_status()
        return r.json()

    @staticmethod
    def get_recent(limit=50):
        """
        return schema:
        {
            "items": [
                {
                    "played_at": ...,
                    "track": {
                        "name": ...,
                        "duration_ms": ...,
                        "ablum": {
                            "name": ...,
                            "artists": [
                                {
                                    "name": ...,
                                },
                            ],
                        },
                    },
                },
            ],
        }
        """
        assert 1 <= limit <= 50
        RECENT_ENDPOINT = "me/player/recently-played"
        res = Spotify.get(
            f"{SPOTIFY_ENDPOINT}/{RECENT_ENDPOINT}",
            {
                "limit": limit
            }
        )
        return res

    @staticmethod
    def recent_to_df(recent):
        """
        convert output from `get_recent()` to df

        schema:
        played_at song artist album duration_ms
        ...       ...  ...    ...   ...
        """
        df = pd.DataFrame(columns=[
            "played_at",
            "song",
            "artist",
            "album",
            "duration_ms",
        ])
        for item in recent["items"]:
            df = df.append({
                "played_at": item["played_at"],
                "song": item["track"]["name"],
                "artist": item["track"]["album"]["artists"][0]["name"],
                "album": item["track"]["album"]["name"],
                "duration_ms": item["track"]["duration_ms"],
            }, ignore_index=True)
        return df
