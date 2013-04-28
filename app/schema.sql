	-- schema.sql

create table Ratings (
    user_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    rating INTEGER,
    time INTEGER
);
create table Users (
    user_id INTEGER PRIMARY KEY,
    zip_code INTEGER,
    email VARCHAR(128),
    password VARCHAR(128),
);

create table Movies (
    movie_id INTEGER PRIMARY KEY,
	movie_title VARCHAR(128),
	genre VARCHAR(256)
);
