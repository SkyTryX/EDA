CREATE TABLE IF NOT EXISTS donnee(
    uuid TEXT PRIMARY KEY,
    mail TEXT NOT NULL UNIQUE,
    pseudo TEXT NOT NULL UNIQUE,
    mdp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stats(
    uuid TEXT PRIMARY KEY,
    win INTEGER NOT NULL,
    elo INTEGER NOT NULL,
    FOREIGN KEY (uuid)
    REFERENCES donnee(uuid)
)
