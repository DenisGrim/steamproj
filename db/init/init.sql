CREATE EXTENSION vector;

CREATE TABLE games (
    id INT PRIMARY KEY,
    name TEXT, -- TEXT NOT NULL, --TODO add names/titles...
    embedding vector(768)
);

CREATE TABLE reviews (
    game_id INT, -- INT REFERENCES games(id), -- this is a TODO
    user_id BIGINT NOT NULL, -- user_id == steam_id
    review TEXT,
    does_recommend INT NOT NULL,
    funny INT,
    helpful INT,
    weight DECIMAL,
    playtime_at_review INT, -- in hours I think
    review_length INT
);

