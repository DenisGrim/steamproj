CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE game_tags (
    game_id INT REFERENCES games(id),
    tag_id INT REFERENCES tags(id),
    PRIMARY KEY (game_id, tag_id)
);
COPY tags(name) FROM '/docker-entrypoint-initdb.d/tags.txt';
