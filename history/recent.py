from pylast import User, LastFMNetwork
from .common import LF_API_KEY
from .db import *
import pandas as pd

def get_duration(track):
    """
    gets duration of a LastFM track
    """
    return track.get_duration()

def to_row(row):
    """
    convert a row of recent track to df row
    """
    track = row.track
    duration_ms = get_duration(track)
    return int(row.timestamp), track.title, track.artist.name, row.album, duration_ms

def to_df(recent):
    """
    convert result from `get_recent_tracks` to df

    will query duration of each track first
    """
    return pd.DataFrame(
        map(to_row, recent),
        columns=["timestamp", "song", "artist", "album", "duration_ms"]
    )

def get_recent(username, *, limit=200, start=None, before=None):
    """
    get `limit` amount of recent tracks of `username` from `start`
    """
    network = LastFMNetwork(api_key=LF_API_KEY)
    user = User(username, network)

    # no duration information
    recent = user.get_recent_tracks(
        limit=limit,
        time_from=start,
        time_to=before,
        stream=True,
    )

    return to_df(recent)

def get_recent_db(username, limit=200, add=False):
    """
    get the most recent ones based on database information

    add: add to database?
    """
    start = get_latest_timestamp()
    res = get_recent(username, limit=limit, start=start)
    if add:
        insert(res)
    return res

def get_older_db(username, limit=200, add=False):
    """
    get the oldest ones based on database information

    add: add to database?
    """
    before = get_oldest_timestamp()
    res = get_recent(username, limit=limit, before=before)
    if add:
        insert(res)
    return res
