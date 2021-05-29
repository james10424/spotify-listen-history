DROP TABLE IF EXISTS history;

CREATE TABLE history (
    timestamp DATE,
    song TEXT,
    artist TEXT,
    album TEXT,
    duration_ms INTEGER
);
