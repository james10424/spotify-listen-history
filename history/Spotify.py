from .auth_server import SpotifyAuth
import requests
from .common import *
import pandas as pd
from datetime import datetime
import sqlalchemy as sql

db = sql.create_engine("sqlite:///history.db")

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
    def get_recent(*, limit=50, before=None, after=None):
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
        assert (before is not None and after is None) or\
               (after is not None and before is None) or\
               (before is None and after is None)
        RECENT_ENDPOINT = "me/player/recently-played"
        time_arg = {}
        if before is not None:
            time_arg = {"before": before}
        if after is not None:
            time_arg = {"after": after}
        res = Spotify.get(
            f"{SPOTIFY_ENDPOINT}/{RECENT_ENDPOINT}",
            {
                "limit": limit,
                **time_arg
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

    @staticmethod
    def str_to_time(spotify_time):
        return datetime.strptime(spotify_time, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def str_to_timestamp(spotify_time):
        return int(Spotify.str_to_time(spotify_time).timestamp())

    @staticmethod
    def latest_history():
        query = """
        SELECT * FROM history ORDER BY played_at_utc DESC LIMIT 1
        """
        return pd.read_sql(query, db).iloc[0]

    @staticmethod
    def oldest_history():
        query = """
        SELECT * FROM history ORDER BY played_at_utc LIMIT 1
        """
        return pd.read_sql(query, db).iloc[0]
