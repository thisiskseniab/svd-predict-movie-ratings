	-- schema.sql
create table Users (
    user_id INTEGER PRIMARY KEY,
    index INTEGER,
    email VARCHAR(128),
    password VARCHAR(128),
    age INTEGER,
    zip_code INTEGER
);

create table Movies (
    movie_id INTEGER PRIMARY KEY,
    index Integer,
    title VARCHAR(64),
    genre VARCHAR(256)

);

create table Ratings (
    user_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    rating INTEGER,
    timestamp INTEGER
);
