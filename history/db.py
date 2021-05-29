import sqlalchemy as sql
from datetime import datetime

LATEST_TIMESTAMP_QUERY = """
SELECT MAX(timestamp) FROM history
"""
OLDEST_TIMESTAMP_QUERY = """
SELECT MIN(timestamp) FROM history
"""

db = sql.create_engine("sqlite:///history.db")

def insert(df):
    """
    bulk insert the entire df into `history`

    refer to `history.sql` for schema
    """
    return df.to_sql("history", con=db, if_exists="append", index=False)

def get_latest_timestamp():
    res = db.execute(LATEST_TIMESTAMP_QUERY)
    t, = res.fetchone()
    return t or 0

def get_oldest_timestamp():
    res = db.execute(OLDEST_TIMESTAMP_QUERY)
    t, = res.fetchone()
    return t or int(datetime.now().timestamp())
