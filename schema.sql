CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE shows (
    id SERIAL PRIMARY KEY,
    name TEXT,
    date DATE,
    venue_id INTEGER REFERENCES venues,
    band_id INTEGER REFERENCES bands
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    contact TEXT
);

CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE setlist (
    id SERIAL PRIMARY KEY,
    show_id INTEGER REFERENCES shows,
    song_id INTEGER REFERENCES songs
);
