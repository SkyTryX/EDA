CREATE TABLE IF NOT EXISTS donnee(
    mail TEXT PRIMARY KEY,
    pseudo TEXT NOT NULL UNIQUE,
    mdp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stat(
    pseudo TEXT PRIMARY KEY,
    win INTEGER NOT NULL,
    elo TEXT NOT NULL,
    FOREIGN KEY (pseudo)
    REFERENCES donnee(pseudo)
)
