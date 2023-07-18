DROP TABLE IF EXISTS live_weight;

CREATE TABLE live_weight(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [time] TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    [id_number] INTEGER NOT NULL,
    [farm] STRING NOT NULL,
    [category] STRING NOT NULL,
    [weight] INTEGER NOT NULL
);