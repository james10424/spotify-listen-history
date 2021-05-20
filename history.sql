DROP TABLE IF EXISTS history;

CREATE TABLE history (
    played_at_utc DATE PRIMARY KEY,
    song TEXT,
    artist TEXT,
    album TEXT,
    duration_ms INTEGER
);
