CREATE TABLE bands (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE shows (
    id SERIAL PRIMARY KEY,
    name TEXT,
    date DATE,
    visible BOOLEAN DEFAULT TRUE,
    venue_id INTEGER REFERENCES venues,
    band_id INTEGER REFERENCES bands
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE venues (
    id SERIAL PRIMARY KEY,
    name TEXT,
    address TEXT,
    contact TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE setlist (
    id SERIAL PRIMARY KEY,
    visible BOOLEAN DEFAULT TRUE,
    show_id INTEGER REFERENCES shows,
    song_id INTEGER REFERENCES songs
);
